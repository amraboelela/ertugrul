#!/usr/bin/env python3
"""
Subtitle Generator using Whisper for Ertugrul Language Learning Project

For episodes where YouTube subtitles are unavailable, this script:
1. Downloads the video from YouTube
2. Uses VAD (Voice Activity Detection) + Whisper Large to generate subtitles
3. Creates both Turkish and English VTT files
4. Converts to JSON format

IMPORTANT COPYRIGHT NOTICE:
This tool is for EDUCATIONAL and RESEARCH purposes only. Users must:
1. Only download content they have legal rights to access
2. Comply with YouTube's Terms of Service
3. Respect copyright laws in their jurisdiction
4. Consider this for personal study/research only

Usage: ./generate_subtitles.py <dataset> <episode>
       ./generate_subtitles.py ertugrul 16

Requirements:
    pip install openai-whisper yt-dlp torch

Created by Amr Aboelela
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Try to import Whisper
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

# Import VTT to JSON conversion function
try:
    from vtt_to_json import convert_vtt_to_json
except ImportError:
    convert_vtt_to_json = None

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

    # Output filename
    video_file = output_path / f"{episode:03d}.mp4"

    # Check if already downloaded
    if video_file.exists():
        print(f"   ✓ Video already exists: {video_file.name}")
        return video_file

    # Try different cookie sources
    cookie_options = [
        ["--cookies-from-browser", "chrome"],
        ["--cookies-from-browser", "safari"],
        ["--cookies-from-browser", "firefox"],
        []  # No cookies as fallback
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

            result = subprocess.run(cmd, capture_output=True, text=True)

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

    # Check if already extracted
    if audio_file.exists():
        print(f"   ✓ Audio already exists: {audio_file.name}")
        return True

    try:
        cmd = [
            "ffmpeg",
            "-i", str(video_file),
            "-vn",  # No video
            "-acodec", "pcm_s16le",  # PCM 16-bit for Whisper
            "-ar", "16000",  # 16kHz sample rate
            "-ac", "1",  # Mono
            str(audio_file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if audio_file.exists():
            print(f"   ✅ Extracted: {audio_file.name}")
            return True
        else:
            print(f"   ❌ Failed to extract audio")
            return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def transcribe_with_whisper(audio_file, language, episode, output_dir):
    """
    Transcribe audio using Whisper Large model

    Args:
        audio_file (Path): Input audio file
        language (str): Language code ("tr" for Turkish, "en" for English)
        episode (int): Episode number
        output_dir (Path): Output directory for VTT files

    Returns:
        Path: Path to VTT file, or None if failed
    """
    if not WHISPER_AVAILABLE:
        print(f"   ❌ Whisper not installed. Install with: pip install openai-whisper")
        return None

    lang_name = "Turkish" if language == "tr" else "English"
    print(f"\n🤖 Transcribing audio to {lang_name} using Whisper Large...")
    print(f"   ⚠️  This may take 10-30 minutes depending on episode length")

    # Output VTT file
    vtt_file = output_dir / f"{episode:03d}-{language}.vtt"

    # Check if already transcribed
    if vtt_file.exists():
        print(f"   ✓ VTT already exists: {vtt_file.name}")
        return vtt_file

    try:
        # Load Whisper large model
        print(f"   📦 Loading Whisper large model (first time may take a while)...")
        model = whisper.load_model("large")

        # Transcribe with language-specific settings
        whisper_lang = "tr" if language == "tr" else "en"

        print(f"   🎙️  Transcribing... (this will take several minutes)")
        result = model.transcribe(
            str(audio_file),
            language=whisper_lang,
            task="transcribe" if language == "tr" else "translate",  # Translate to English for en
            verbose=False,
            word_timestamps=True  # Better timing accuracy
        )

        # Write VTT file
        print(f"   💾 Writing VTT file...")
        write_vtt(result, vtt_file)

        print(f"   ✅ Created: {vtt_file.name}")
        return vtt_file

    except Exception as e:
        print(f"   ❌ Transcription failed: {e}")
        return None

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

            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{text}\n\n")

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

def main():
    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  ./generate_subtitles.py <dataset> <episode>")
        print("\nExamples:")
        print("  ./generate_subtitles.py ertugrul 16")
        print("\nNote: Generates subtitles using Whisper for episodes without YouTube subtitles")
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
    possible_video_paths = [
        Path(f"../{dataset}/videos"),
        Path(f"{dataset}/videos"),
    ]

    video_dir = None
    for path in possible_video_paths:
        if path.parent.exists():
            video_dir = path
            break

    if video_dir is None:
        video_dir = Path(f"../{dataset}/videos")

    video_dir.mkdir(parents=True, exist_ok=True)

    # Audio directory
    audio_dir = video_dir / "audio"
    audio_dir.mkdir(exist_ok=True)

    # Subtitles temp directory
    possible_temp_paths = [
        Path(f"../{dataset}/subtitles/temp"),
        Path(f"{dataset}/subtitles/temp"),
    ]

    temp_dir = None
    for path in possible_temp_paths:
        if path.parent.exists():
            temp_dir = path
            break

    if temp_dir is None:
        temp_dir = Path(f"../{dataset}/subtitles/temp")

    temp_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Download video
    video_file = download_video(youtube_id, video_dir, episode)
    if not video_file:
        sys.exit(1)

    # Step 2: Extract audio
    audio_file = audio_dir / f"{episode:03d}.wav"
    if not extract_audio(video_file, audio_file):
        sys.exit(1)

    # Step 3: Transcribe to Turkish
    tr_vtt = transcribe_with_whisper(audio_file, "tr", episode, temp_dir)
    if not tr_vtt:
        print(f"\n❌ Failed to generate Turkish subtitles")
        sys.exit(1)

    # Step 4: Transcribe/translate to English
    en_vtt = transcribe_with_whisper(audio_file, "en", episode, temp_dir)
    if not en_vtt:
        print(f"\n❌ Failed to generate English subtitles")
        sys.exit(1)

    # Step 5: Convert to JSON
    if convert_vtt_to_json:
        print(f"\n📄 Converting to JSON format...")

        # Find main subtitles directory
        possible_main_paths = [
            Path(f"../{dataset}/subtitles"),
            Path(f"{dataset}/subtitles"),
        ]

        main_dir = None
        for path in possible_main_paths:
            if path.exists():
                main_dir = path
                break

        if main_dir:
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
    print(f"   Turkish: {tr_vtt}")
    print(f"   English: {en_vtt}")
    print(f"\n💡 You can now watch the video with English subtitles!")

if __name__ == "__main__":
    main()
