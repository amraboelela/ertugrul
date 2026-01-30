"""
VAD (Voice Activity Detection) utilities using Silero VAD
"""
import torch
import torchaudio

# Cache VAD utils globally to avoid reloading from torch.hub
_vad_utils_cache = None


def _get_vad_utils():
    """Load VAD utils once and cache them"""
    global _vad_utils_cache
    if _vad_utils_cache is None:
        _vad_utils_cache = torch.hub.load(
            repo_or_dir='snakers4/silero-vad',
            model='silero_vad',
            force_reload=False,
            onnx=False,
            trust_repo=True
        )[1]
    return _vad_utils_cache


def detect_speech_segments_streaming(audio_path, vad_model, device,
                                     increment_seconds=0.5,
                                     min_speech_duration=0.7,
                                     min_silence_duration=0.5,
                                     threshold=0.45,
                                     max_segment_duration=None):
    """Detect speech segments using streaming/incremental approach.

    Simulates real-time audio buffering where audio arrives incrementally.
    This matches the behavior of the iOS app where audio is buffered and
    processed in chunks.

    **Generator function** - yields segments as they're detected for pipeline processing.

    Algorithm:
    1. Start with accumulation buffer at position 0
    2. Add increment_seconds to buffer (0-1s, 0-2s, 0-3s, ...)
    3. Run VAD on accumulated chunk:
       - 0 segments: keep accumulating (no speech yet)
       - 1 segment: keep accumulating (segment not complete)
       - 2+ segments: first segment is complete!
         - **Yield** the complete first segment immediately
         - Reset buffer to start of second segment
    4. Repeat until end of audio
    5. If max_segment_duration is set, split long segments into smaller pieces

    Args:
        audio_path: Path to audio file (16kHz mono recommended)
        vad_model: Loaded VAD model
        device: torch device
        increment_seconds: Seconds to add each iteration (simulates streaming)
        min_speech_duration: Minimum duration for speech segments (seconds)
        min_silence_duration: Minimum silence duration between segments (seconds)
        threshold: Speech probability threshold (0.0-1.0, lower = more sensitive)
        max_segment_duration: Maximum segment duration in seconds (splits longer segments if set)

    Yields:
        Tuples of (start_time, end_time, 'speech') as segments are detected
    """
    # Load audio
    waveform, sample_rate = torchaudio.load(str(audio_path))

    # Ensure mono
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    # Resample to 16kHz if needed (VAD expects 16kHz)
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(sample_rate, 16000)
        waveform = resampler(waveform)
        sample_rate = 16000

    # Get VAD utils (cached)
    (get_speech_timestamps, _, read_audio, _, _) = _get_vad_utils()

    total_duration = waveform.shape[1] / sample_rate
    buffer_start = 0.0

    # Move full waveform to CPU once
    waveform_cpu = waveform.squeeze(0).cpu()

    while buffer_start < total_duration:
        buffer_end = buffer_start + increment_seconds
        num_segments = 0

        # Accumulate audio incrementally
        while buffer_end <= total_duration:
            # Extract accumulated chunk
            start_sample = int(buffer_start * sample_rate)
            end_sample = int(buffer_end * sample_rate)
            chunk = waveform_cpu[start_sample:end_sample]

            # Run VAD on accumulated chunk
            vad_segments = get_speech_timestamps(
                chunk,
                vad_model,
                sampling_rate=sample_rate,
                min_speech_duration_ms=int(min_speech_duration * 1000),
                min_silence_duration_ms=int(min_silence_duration * 1000),
                threshold=threshold,
                return_seconds=False
            )

            num_segments = len(vad_segments)

            if num_segments == 0:
                # No speech yet, keep accumulating
                buffer_end += increment_seconds

            elif num_segments == 1:
                # One segment found but not complete yet, keep accumulating
                buffer_end += increment_seconds

            else:  # num_segments >= 2
                # First segment is complete!
                # Convert first segment end from samples to seconds (relative to chunk)
                first_seg_end_samples = vad_segments[0]['end']
                first_seg_end_seconds = first_seg_end_samples / sample_rate

                # Calculate absolute position in full audio
                segment_end = buffer_start + first_seg_end_seconds

                # Split long segments if max_segment_duration is set
                if max_segment_duration and (segment_end - buffer_start) > (max_segment_duration - 0.1):
                    # Split into smaller pieces
                    split_threshold = max_segment_duration - 0.1
                    current_start = buffer_start
                    while current_start < segment_end:
                        current_end = min(current_start + split_threshold, segment_end)
                        yield (current_start, current_end, 'speech')
                        current_start = current_end
                else:
                    # Yield the complete segment immediately for processing
                    yield (buffer_start, segment_end, 'speech')

                # Reset buffer to start of second segment
                buffer_start = segment_end
                break

        # Handle end of file - if we have 1 segment at EOF, it's complete
        if buffer_end > total_duration:
            if num_segments == 1:
                # Split long segments if max_segment_duration is set
                if max_segment_duration and (total_duration - buffer_start) > (max_segment_duration - 0.1):
                    split_threshold = max_segment_duration - 0.1
                    current_start = buffer_start
                    while current_start < total_duration:
                        current_end = min(current_start + split_threshold, total_duration)
                        yield (current_start, current_end, 'speech')
                        current_start = current_end
                else:
                    yield (buffer_start, total_duration, 'speech')
            break
