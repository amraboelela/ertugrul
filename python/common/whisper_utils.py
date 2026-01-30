#!/usr/bin/env python3
"""
Whisper transcription utilities for Ertugrul Language Learning Project

Created by Amr Aboelela
"""

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

from .utils import load_audio_segment, write_vtt


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


def transcribe_segments_with_whisper(audio_file, segments, language, episode, output_dir, whisper_model, whisper_processor, episode_dir=None, audio_segments_dir=None):
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
        episode_dir (Path): Optional episode directory to save VTT files and progress
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
                    # Save with ~ suffix to indicate partial (to episode directory)
                    if episode_dir:
                        partial_vtt = episode_dir / f"{episode:03d}-{language}~.vtt"
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

        # Also copy to episode directory if provided
        if episode_dir:
            episode_vtt = episode_dir / vtt_file.name
            shutil.copy2(vtt_file, episode_vtt)
            print(f"   📋 Copied to: {episode_vtt}")

        return vtt_file

    except Exception as e:
        print(f"   ❌ Transcription failed: {e}")
        import traceback
        traceback.print_exc()
        return None
