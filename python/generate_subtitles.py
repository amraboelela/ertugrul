#!/usr/bin/env python3
"""
Subtitle Generator using VAD + Whisper for Ertugrul Language Learning Project

For episodes where YouTube subtitles are unavailable, this script:
1. Downloads the video from YouTube
2. Extracts audio from video
3. Uses VAD (Voice Activity Detection) to segment speech
4. Uses Whisper Large (from Hugging Face) to transcribe segments
5. Creates both Turkish and English VTT files
6. Converts to JSON format

IMPORTANT COPYRIGHT NOTICE:
This tool is for EDUCATIONAL and RESEARCH purposes only. Users must:
1. Only download content they have legal rights to access
2. Comply with YouTube's Terms of Service
3. Respect copyright laws in their jurisdiction
4. Consider this for personal study/research only

Usage: ./generate_subtitles.py <dataset> <episode>
       ./generate_subtitles.py ertugrul 16

Requirements:
    pip install transformers torch torchaudio yt-dlp

Created by Amr Aboelela
"""

import sys
import os

# Auto-caffeinate to prevent sleep during processing (macOS only)
if sys.platform == 'darwin' and 'CAFFEINATED' not in os.environ:
    try:
        print("🔋 Restarting with caffeinate to prevent sleep during processing...")
        os.environ['CAFFEINATED'] = '1'
        os.execvp('caffeinate', ['caffeinate', '-i', sys.executable] + sys.argv)
    except Exception as e:
        print(f"⚠️  Could not start caffeinate: {e}")
        pass

import json
import torch
import torchaudio
import shutil
from pathlib import Path

# Try to import Hugging Face transformers
try:
    from transformers import WhisperProcessor, WhisperForConditionalGeneration
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

# Import VTT to JSON conversion function
try:
    from vtt_to_json import convert_vtt_to_json
except ImportError:
    convert_vtt_to_json = None

# Import utility functions
from common.utils import (
    load_audio_segment,
    write_vtt,
    load_vad_model,
    download_video,
    extract_audio,
    find_path
)
from common.vad_utils import detect_speech_segments_streaming


def get_speech_timestamps(audio_file, vad_model, vad_utils):
    """
    Use Silero VAD to detect speech segments in audio with proper parameters

    Args:
        audio_file (Path): Input audio file (16kHz mono WAV)
        vad_model: Pre-loaded VAD model
        vad_utils: Pre-loaded VAD utilities

    Returns:
        list: List of speech segments as (start_time, end_time) tuples in seconds
    """
    print(f"\n🎯 Detecting speech segments using VAD...")

    try:
        (get_speech_timestamps_func, _, read_audio, _, _) = vad_utils

        # Read audio file
        wav = read_audio(str(audio_file), sampling_rate=16000)

        # Get speech timestamps with proper parameters (matching Turkish2English)
        speech_timestamps = get_speech_timestamps_func(
            wav,
            vad_model,
            sampling_rate=16000,
            threshold=0.45,                    # Lower threshold for better detection
            min_speech_duration_ms=700,        # 0.7 seconds minimum
            min_silence_duration_ms=500,       # 0.5 seconds silence between segments
            window_size_samples=512,
            speech_pad_ms=30
        )

        # Convert from samples to seconds
        segments = []
        for ts in speech_timestamps:
            start = ts['start'] / 16000.0
            end = ts['end'] / 16000.0
            duration = end - start

            # Split segments longer than 15 seconds
            if duration > 15.0:
                current_start = start
                while current_start < end:
                    current_end = min(current_start + 14.9, end)
                    segments.append((current_start, current_end))
                    current_start = current_end
            else:
                segments.append((start, end))

        print(f"   ✅ Detected {len(segments)} speech segments")
        return segments

    except Exception as e:
        print(f"   ⚠️  VAD failed: {e}")
        print(f"   ℹ️  Falling back to full audio transcription")
        return None


def transcribe_with_whisper(audio_file, start_time, end_time, language, whisper_model, whisper_processor):
    """
    Transcribe audio segment with Whisper using Hugging Face

    Args:
        audio_file (Path): Input audio file
        start_time (float): Start time in seconds
        end_time (float): End time in seconds
        language (str): Language code ("tr" or "en")
        whisper_model: Pre-loaded Whisper model
        whisper_processor: Pre-loaded Whisper processor

    Returns:
        str: Transcribed text
    """
    # Load audio segment
    audio_array = load_audio_segment(audio_file, start_time, end_time)

    # Process audio
    input_features = whisper_processor(audio_array, sampling_rate=16000, return_tensors="pt").input_features

    # Set language and task
    whisper_lang = "turkish" if language == "tr" else "english"
    task = "transcribe" if language == "tr" else "translate"

    # Generate transcription
    forced_decoder_ids = whisper_processor.get_decoder_prompt_ids(language=whisper_lang, task=task)
    generated_ids = whisper_model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
    text = whisper_processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()

    return text

def transcribe_segments_with_whisper(audio_file, segments, language, episode, output_dir, whisper_model, whisper_processor, videos_dir=None, audio_segments_dir=None):
    """
    Transcribe audio segments using Whisper Large model from Hugging Face

    Args:
        audio_file (Path): Input audio file
        segments (list): List of (start, end) tuples in seconds, or None for full audio
        language (str): Language code ("tr" for Turkish, "en" for English)
        episode (int): Episode number
        output_dir (Path): Output directory for VTT files
        whisper_model: Pre-loaded Whisper model (reused)
        whisper_processor: Pre-loaded Whisper processor (reused)
        videos_dir (Path): Optional additional directory to save VTT files
        audio_segments_dir (Path): Optional directory to save audio segment files

    Returns:
        Path: Path to VTT file, or None if failed
    """
    if not WHISPER_AVAILABLE:
        print(f"   ❌ Whisper not installed. Install with: pip install transformers torch")
        return None

    lang_name = "Turkish" if language == "tr" else "English"
    print(f"\n🤖 Transcribing audio to {lang_name} using Whisper Large...")

    # Output VTT file
    vtt_file = output_dir / f"{episode:03d}-{language}.vtt"

    # Check if already transcribed
    if vtt_file.exists():
        print(f"   ✓ VTT already exists: {vtt_file.name}")
        return vtt_file

    try:
        all_segments = []

        if segments:
            print(f"   🎙️  Transcribing {len(segments)} speech segments...")
            if audio_segments_dir and language == "tr":
                print(f"   💾 Saving audio segments to: {audio_segments_dir}/")
            # Transcribe each VAD segment
            for i, (start, end) in enumerate(segments, 1):
                # Only print progress every 100 segments to reduce verbosity
                if i % 100 == 0 or i == 1 or i == len(segments):
                    print(f"      Progress: {i}/{len(segments)} segments ({i*100//len(segments)}%)")

                # Load audio segment
                audio_array = load_audio_segment(audio_file, start, end)

                # Save audio segment if directory provided and this is Turkish transcription
                if audio_segments_dir and language == "tr":
                    segment_file = audio_segments_dir / f"segment_{i:04d}.wav"
                    segment_tensor = torch.from_numpy(audio_array).unsqueeze(0)
                    torchaudio.save(str(segment_file), segment_tensor, 16000)

                # Transcribe segment
                transcription = transcribe_with_whisper(audio_file, start, end, language, whisper_model, whisper_processor)

                if transcription.strip():
                    all_segments.append({
                        'start': start,
                        'end': end,
                        'text': transcription.strip()
                    })

                # Save progress every 100 segments
                if i % 100 == 0:
                    print(f"      💾 Saving progress: {len(all_segments)} transcriptions...")
                    # Save with ~ suffix to indicate partial (to videos directory)
                    partial_vtt = videos_dir / f"{episode:03d}-{language}~.vtt"
                    write_vtt({'segments': all_segments}, partial_vtt)


        else:
            # Transcribe full audio without VAD segmentation
            print(f"   🎙️  Transcribing full audio (this will take 10-30 minutes)...")

            # Load full audio
            waveform, sample_rate = torchaudio.load(str(audio_file))
            if waveform.shape[0] > 1:
                waveform = torch.mean(waveform, dim=0, keepdim=True)
            audio_array = waveform.squeeze().numpy()

            # Process in chunks (30 second chunks)
            chunk_length = 30 * 16000  # 30 seconds at 16kHz
            import numpy as np
            num_chunks = int(np.ceil(len(audio_array) / chunk_length))

            for i in range(num_chunks):
                start_sample = i * chunk_length
                end_sample = min((i + 1) * chunk_length, len(audio_array))
                chunk = audio_array[start_sample:end_sample]

                start_time = start_sample / 16000
                end_time = end_sample / 16000

                # Only print progress every 10 chunks to reduce verbosity
                if i % 10 == 0 or i == 0 or i == num_chunks - 1:
                    print(f"      Progress: Chunk {i+1}/{num_chunks} ({(i+1)*100//num_chunks}%)")

                # Process audio chunk
                input_features = whisper_processor(chunk, sampling_rate=16000, return_tensors="pt").input_features

                # Set language and task
                whisper_lang = "turkish" if language == "tr" else "english"
                task = "transcribe" if language == "tr" else "translate"

                # Generate transcription
                forced_decoder_ids = whisper_processor.get_decoder_prompt_ids(language=whisper_lang, task=task)
                generated_ids = whisper_model.generate(input_features, forced_decoder_ids=forced_decoder_ids)
                transcription = whisper_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

                if transcription.strip():
                    all_segments.append({
                        'start': start_time,
                        'end': end_time,
                        'text': transcription.strip()
                    })

        # Write VTT file
        print(f"   💾 Writing VTT file with {len(all_segments)} segments...")
        write_vtt({'segments': all_segments}, vtt_file)

        print(f"   ✅ Created: {vtt_file.name}")

        # Also copy to videos directory if provided
        if videos_dir:
            videos_vtt = videos_dir / vtt_file.name
            shutil.copy2(vtt_file, videos_vtt)
            print(f"   📋 Copied to: {videos_vtt}")

        return vtt_file

    except Exception as e:
        print(f"   ❌ Transcription failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  ./generate_subtitles.py <dataset> <episode>")
        print("\nExamples:")
        print("  ./generate_subtitles.py ertugrul 16")
        print("\nNote: Generates subtitles using VAD + Whisper for episodes without YouTube subtitles")
        sys.exit(1)

    dataset = sys.argv[1]

    try:
        episode = int(sys.argv[2])
    except ValueError:
        print("❌ Episode must be a number")
        sys.exit(1)

    # Load episodes data to get YouTube ID
    possible_paths = [
        f"{dataset}/episodes.json",
        f"../{dataset}/episodes.json",
    ]

    episodes_data = None
    for json_file in possible_paths:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                episodes_data = json.load(f)
                break
        except FileNotFoundError:
            continue

    if not episodes_data:
        print("❌ episodes.json not found")
        sys.exit(1)

    # Get YouTube ID
    episode_str = str(episode)
    if episode_str not in episodes_data.get("episodes", {}):
        print(f"❌ Episode {episode} not found in episodes.json")
        sys.exit(1)

    youtube_id = episodes_data["episodes"][episode_str]
    if not youtube_id:
        print(f"❌ No YouTube ID for episode {episode}")
        sys.exit(1)

    print(f"🎬 Generating Subtitles for Episode {episode:03d}")
    print(f"=" * 60)
    print(f"⚠️  IMPORTANT: Only process content you have legal rights to access")
    print(f"⚠️  This tool is for educational and research purposes only")
    print(f"=" * 60)
    print(f"\n🔗 YouTube ID: {youtube_id}")

    # Setup directories
    video_dir = find_path([
        Path(f"../{dataset}/videos"),
        Path(f"{dataset}/videos"),
    ])
    video_dir.mkdir(parents=True, exist_ok=True)

    audio_dir = video_dir / "audio"
    audio_dir.mkdir(exist_ok=True)

    temp_dir = find_path([
        Path(f"../{dataset}/subtitles/temp"),
        Path(f"{dataset}/subtitles/temp"),
    ])
    temp_dir.mkdir(parents=True, exist_ok=True)

    videos_dir = find_path([
        Path(f"../{dataset}/videos"),
        Path(f"{dataset}/videos"),
    ])
    videos_dir.mkdir(parents=True, exist_ok=True)

    audio_segments_dir = videos_dir / "audio" / f"{episode:03d}"

    # Check for partial/incomplete processing and clean up
    tr_vtt_temp = temp_dir / f"{episode:03d}-tr.vtt"
    en_vtt_temp = temp_dir / f"{episode:03d}-en.vtt"
    tr_vtt_videos = videos_dir / f"{episode:03d}-tr.vtt"
    en_vtt_videos = videos_dir / f"{episode:03d}-en.vtt"
    tr_vtt_partial = videos_dir / f"{episode:03d}-tr~.vtt"
    en_vtt_partial = videos_dir / f"{episode:03d}-en~.vtt"

    # If audio segments exist but VTT files don't, it's partial - delete everything
    has_audio_segments = audio_segments_dir.exists() and len(list(audio_segments_dir.glob("segment_*.wav"))) > 0
    has_vtt_files = (tr_vtt_temp.exists() and en_vtt_temp.exists()) or (tr_vtt_videos.exists() and en_vtt_videos.exists())

    if has_audio_segments and not has_vtt_files:
        num_segments = len(list(audio_segments_dir.glob("segment_*.wav")))
        print(f"\n⚠️  Episode {episode:03d} has partial data")
        print(f"   Found: {num_segments} audio segments without complete VTT files")
        print(f"   Deleting incomplete data and starting fresh...")

        # Delete audio segments directory
        if audio_segments_dir.exists():
            shutil.rmtree(audio_segments_dir)
            print(f"   🗑️  Deleted: {num_segments} audio segments from {audio_segments_dir}")

        # Delete any partial VTT files (including ~ suffix)
        deleted_vtts = []
        for vtt_file in [tr_vtt_temp, en_vtt_temp, tr_vtt_videos, en_vtt_videos, tr_vtt_partial, en_vtt_partial]:
            if vtt_file.exists():
                vtt_file.unlink()
                deleted_vtts.append(vtt_file.name)

        if deleted_vtts:
            print(f"   🗑️  Deleted partial VTT files: {', '.join(deleted_vtts)}")

        print(f"   ✅ Ready to start from scratch\n")
    elif tr_vtt_temp.exists() and en_vtt_temp.exists():
        print(f"\n⏭️  Episode {episode:03d} already fully processed, skipping...")
        print(f"   Turkish VTT: {tr_vtt_temp}")
        print(f"   English VTT: {en_vtt_temp}")
        if tr_vtt_videos.exists():
            print(f"   VTT copies in videos directory exist")
        sys.exit(0)

    # Create audio segments directory
    audio_segments_dir.mkdir(parents=True, exist_ok=True)

    # Load VAD model once (cached by torch.hub)
    print(f"\n🔍 Loading VAD model...")
    vad_model, vad_utils = load_vad_model()
    print(f"✓ VAD model loaded (cached for reuse)")

    # Load Whisper model once (cached by Hugging Face)
    print(f"\n🤖 Loading Whisper large-v3 model from Hugging Face...")
    whisper_processor = WhisperProcessor.from_pretrained("openai/whisper-large-v3")
    whisper_model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v3")
    print(f"✓ Whisper model loaded (cached for reuse)")

    # Step 1: Download video
    video_file = download_video(youtube_id, video_dir, episode)
    if not video_file:
        sys.exit(1)

    # Step 2: Extract audio
    audio_file = audio_dir / f"{episode:03d}.wav"
    if not extract_audio(video_file, audio_file):
        sys.exit(1)

    # Step 3: Detect speech segments using VAD
    speech_segments = get_speech_timestamps(audio_file, vad_model, vad_utils)

    # Step 4: Transcribe to Turkish
    tr_vtt = transcribe_segments_with_whisper(audio_file, speech_segments, "tr", episode, temp_dir, whisper_model, whisper_processor, videos_dir, audio_segments_dir)
    if not tr_vtt:
        print(f"\n❌ Failed to generate Turkish subtitles")
        sys.exit(1)

    # Step 5: Transcribe/translate to English
    en_vtt = transcribe_segments_with_whisper(audio_file, speech_segments, "en", episode, temp_dir, whisper_model, whisper_processor, videos_dir)
    if not en_vtt:
        print(f"\n❌ Failed to generate English subtitles")
        sys.exit(1)

    # Step 6: Convert to JSON
    if convert_vtt_to_json:
        print(f"\n📄 Converting to JSON format...")
        main_dir = find_path([
            Path(f"../{dataset}/subtitles"),
            Path(f"{dataset}/subtitles"),
        ])

        if main_dir.exists():
            output_json = main_dir / f"{episode:03d}.json"
            try:
                convert_vtt_to_json(tr_vtt, en_vtt, output_json)
                print(f"   ✅ Created: {output_json.name}")
            except Exception as e:
                print(f"   ⚠️  JSON conversion failed: {e}")

    print(f"\n{'=' * 60}")
    print(f"🎉 Episode {episode:03d} completed!")
    print(f"{'=' * 60}")
    print(f"📁 Files created:")
    print(f"   Video:   {video_file}")
    print(f"   Turkish VTT: {tr_vtt}")
    print(f"   English VTT: {en_vtt}")
    if videos_dir:
        print(f"   VTT copies: {videos_dir}/{episode:03d}-{{tr,en}}.vtt")
    if speech_segments:
        print(f"   Audio segments: {audio_segments_dir}/ ({len(speech_segments)} segments)")
    print(f"\n💡 You can now watch the video with subtitles!")

if __name__ == "__main__":
    main()
