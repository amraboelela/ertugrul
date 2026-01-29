#!/usr/bin/env python3
"""
Common utility functions for Ertugrul Language Learning Project

Created by Amr Aboelela
"""

import torch
import torchaudio


def format_timestamp(seconds):
    """
    Format seconds to VTT timestamp format (HH:MM:SS.mmm)

    Args:
        seconds (float): Time in seconds

    Returns:
        str: Formatted timestamp
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


def format_time(seconds):
    """
    Format seconds to readable time format (HH:MM:SS)

    Args:
        seconds (float): Time in seconds

    Returns:
        str: Formatted time
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def load_audio_segment(audio_file, start_time, end_time):
    """
    Load a segment of audio file

    Args:
        audio_file (Path): Input audio file
        start_time (float): Start time in seconds
        end_time (float): End time in seconds

    Returns:
        numpy.ndarray: Audio samples
    """
    waveform, sample_rate = torchaudio.load(str(audio_file))

    # Convert to mono if stereo
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    # Calculate sample indices
    start_sample = int(start_time * sample_rate)
    end_sample = int(end_time * sample_rate)

    # Extract segment
    segment = waveform[:, start_sample:end_sample]

    # Convert to numpy and flatten
    return segment.squeeze().numpy()


def write_vtt(whisper_result, output_file):
    """
    Write Whisper transcription result to VTT format

    Args:
        whisper_result: Whisper transcription result
        output_file (Path): Output VTT file path
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write VTT header
        f.write("WEBVTT\n\n")

        # Write each segment
        for segment in whisper_result['segments']:
            start_time = format_timestamp(segment['start'])
            end_time = format_timestamp(segment['end'])
            text = segment['text'].strip()

            if text:  # Only write non-empty segments
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{text}\n\n")


def load_vad_model():
    """Load Silero VAD model (cached by torch.hub)

    Returns:
        tuple: (vad_model, vad_utils)
    """
    model, utils = torch.hub.load(
        repo_or_dir='snakers4/silero-vad',
        model='silero_vad',
        force_reload=False,
        onnx=False
    )
    return model, utils
