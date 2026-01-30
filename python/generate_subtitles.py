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
    load_vad_model,
    download_video,
    extract_audio,
    find_path
)
from common.vad_utils import get_speech_timestamps
from common.whisper_utils import transcribe_segments_with_whisper


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

    # Episode-specific directory for videos and VTT files
    episode_dir = video_dir / f"{episode:03d}"
    episode_dir.mkdir(parents=True, exist_ok=True)

    # Audio directory within episode
    audio_dir = episode_dir / "audio"
    audio_dir.mkdir(exist_ok=True)

    temp_dir = find_path([
        Path(f"../{dataset}/subtitles/temp"),
        Path(f"{dataset}/subtitles/temp"),
    ])
    temp_dir.mkdir(parents=True, exist_ok=True)

    audio_segments_dir = audio_dir / "segments"

    # Check for partial/incomplete processing and clean up
    tr_vtt_temp = temp_dir / f"{episode:03d}-tr.vtt"
    en_vtt_temp = temp_dir / f"{episode:03d}-en.vtt"
    tr_vtt_episode = episode_dir / f"{episode:03d}-tr.vtt"
    en_vtt_episode = episode_dir / f"{episode:03d}-en.vtt"
    tr_vtt_partial = episode_dir / f"{episode:03d}-tr~.vtt"
    en_vtt_partial = episode_dir / f"{episode:03d}-en~.vtt"

    # If audio segments exist but VTT files don't, it's partial - delete everything
    has_audio_segments = audio_segments_dir.exists() and len(list(audio_segments_dir.glob("segment_*.wav"))) > 0
    has_vtt_files = (tr_vtt_temp.exists() and en_vtt_temp.exists()) or (tr_vtt_episode.exists() and en_vtt_episode.exists())

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
        for vtt_file in [tr_vtt_temp, en_vtt_temp, tr_vtt_episode, en_vtt_episode, tr_vtt_partial, en_vtt_partial]:
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
        if tr_vtt_episode.exists():
            print(f"   VTT copies in episode directory exist")
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
    video_file = download_video(youtube_id, episode_dir, episode)
    if not video_file:
        sys.exit(1)

    # Step 2: Extract audio
    audio_file = audio_dir / f"{episode:03d}.wav"
    if not extract_audio(video_file, audio_file):
        sys.exit(1)

    # Step 3: Detect speech segments using VAD
    speech_segments = get_speech_timestamps(audio_file, vad_model, vad_utils)

    # Step 4: Transcribe to Turkish
    tr_vtt = transcribe_segments_with_whisper(audio_file, speech_segments, "tr", episode, temp_dir, whisper_model, whisper_processor, episode_dir, audio_segments_dir)
    if not tr_vtt:
        print(f"\n❌ Failed to generate Turkish subtitles")
        sys.exit(1)

    # Step 5: Transcribe/translate to English
    en_vtt = transcribe_segments_with_whisper(audio_file, speech_segments, "en", episode, temp_dir, whisper_model, whisper_processor, episode_dir)
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

    # Cleanup: Delete partial VTT files with ~ suffix
    print(f"\n🧹 Cleaning up temporary files...")
    deleted_count = 0
    for partial_vtt in [tr_vtt_partial, en_vtt_partial]:
        if partial_vtt.exists():
            partial_vtt.unlink()
            deleted_count += 1
            print(f"   🗑️  Deleted: {partial_vtt.name}")

    # Delete old shared audio directory if it exists (legacy from old structure)
    old_audio_dir = video_dir / "audio"
    if old_audio_dir.exists() and old_audio_dir.is_dir():
        # Only delete if it's empty or contains episode-specific WAV files
        old_audio_files = list(old_audio_dir.glob(f"{episode:03d}.wav"))
        if old_audio_files:
            for old_file in old_audio_files:
                old_file.unlink()
                deleted_count += 1
                print(f"   🗑️  Deleted: {old_file}")
            # Try to remove the directory if empty
            try:
                old_audio_dir.rmdir()
                print(f"   🗑️  Deleted empty directory: {old_audio_dir}")
            except OSError:
                pass  # Directory not empty, keep it

    if deleted_count > 0:
        print(f"   ✅ Cleaned up {deleted_count} temporary file(s)")

    print(f"\n{'=' * 60}")
    print(f"🎉 Episode {episode:03d} completed!")
    print(f"{'=' * 60}")
    print(f"📁 Files created:")
    print(f"   Video:   {video_file}")
    print(f"   Audio:   {audio_file}")
    print(f"   Turkish VTT: {tr_vtt}")
    print(f"   English VTT: {en_vtt}")
    if episode_dir:
        print(f"   Episode directory: {episode_dir}/")
        print(f"     - {episode:03d}.mp4 (video)")
        print(f"     - {episode:03d}-tr.vtt (Turkish subtitles)")
        print(f"     - {episode:03d}-en.vtt (English subtitles)")
        print(f"     - audio/{episode:03d}.wav (full audio)")
        if speech_segments:
            print(f"     - audio/segments/ ({len(speech_segments)} segments)")
    print(f"\n💡 You can now watch the video with subtitles!")

if __name__ == "__main__":
    main()
