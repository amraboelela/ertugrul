#!/usr/bin/env python3
"""
Common utility functions for Ertugrul Language Learning Project

Created by Amr Aboelela
"""

import subprocess
import torch
import torchaudio
from pathlib import Path


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


def download_video(youtube_id, output_path, episode):
    """
    Download video from YouTube

    Args:
        youtube_id (str): YouTube video ID
        output_path (Path): Output directory path
        episode (int): Episode number

    Returns:
        Path: Path to downloaded video file, or None if failed
    """
    print(f"\n📥 Downloading video from YouTube...")
    url = f"https://www.youtube.com/watch?v={youtube_id}"
    video_file = output_path / f"{episode:03d}.mp4"

    if video_file.exists():
        print(f"   ✓ Video already exists: {video_file.name}")
        return video_file

    cookie_options = [
        ["--cookies-from-browser", "chrome"],
        ["--cookies-from-browser", "safari"],
        ["--cookies-from-browser", "firefox"],
        []
    ]

    for cookie_option in cookie_options:
        try:
            cmd = [
                "yt-dlp",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "--merge-output-format", "mp4",
                "-o", str(video_file),
                "--user-agent", "Mozilla/5.0",
            ] + cookie_option + [url]

            subprocess.run(cmd, capture_output=True, text=True)

            if video_file.exists():
                print(f"   ✅ Downloaded: {video_file.name}")
                return video_file

        except subprocess.CalledProcessError:
            continue

    print(f"   ❌ Failed to download video")
    return None


def extract_audio(video_file, audio_file):
    """
    Extract audio from video using ffmpeg

    Args:
        video_file (Path): Input video file
        audio_file (Path): Output audio file

    Returns:
        bool: True if successful
    """
    print(f"\n🔊 Extracting audio from video...")

    if audio_file.exists():
        print(f"   ✓ Audio already exists: {audio_file.name}")
        return True

    try:
        cmd = [
            "ffmpeg",
            "-i", str(video_file),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(audio_file)
        ]

        subprocess.run(cmd, capture_output=True, text=True)

        if audio_file.exists():
            print(f"   ✅ Extracted: {audio_file.name}")
            return True
        else:
            print(f"   ❌ Failed to extract audio")
            return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def find_path(possible_paths):
    """
    Find first existing path from a list of possible paths

    Args:
        possible_paths (list): List of Path objects to try

    Returns:
        Path: First existing path, or last path if none exist
    """
    for path in possible_paths:
        if path.parent.exists():
            return path
    return possible_paths[-1]

