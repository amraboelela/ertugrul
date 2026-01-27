#!/usr/bin/env python3
"""
Subtitle Downloader for Ertugrul Language Learning Project

IMPORTANT COPYRIGHT NOTICE:
This tool is for EDUCATIONAL and RESEARCH purposes only. Users must:
1. Only download content they have legal rights to access
2. Comply with YouTube's Terms of Service
3. Respect copyright laws in their jurisdiction
4. Consider this for personal study/research only

Downloads VTT subtitle files for language learning:
- English subtitles (source language)
- Turkish subtitles (target language)

Usage: ./download_subtitles.py <dataset> <episode>
       ./download_subtitles.py ertugrul 3              # Download Episode 3 from JSON

Created by Amr Aboelela
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def load_episodes_json(dataset="ertugrul"):
    """
    Load episode YouTube IDs from JSON file

    Args:
        dataset (str): Dataset name (default: "ertugrul")

    Returns:
        dict: Episodes data or None if file not found
    """
    # Try multiple paths to find episodes.json
    possible_paths = [
        f"{dataset}/episodes.json",    # From project root
        f"../{dataset}/episodes.json", # From python/ directory
    ]

    for json_file in possible_paths:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            continue
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in episodes file: {e}")
            return None

    print(f"❌ Episodes file not found. Tried:")
    for path in possible_paths:
        print(f"   - {path}")
    return None

def get_youtube_id(episodes_data, episode):
    """
    Get YouTube ID for a specific episode

    Args:
        episodes_data (dict): Episodes data from JSON
        episode (int): Episode number (1-150)

    Returns:
        str: YouTube ID or None if not found
    """
    if not episodes_data:
        return None

    episode_str = str(episode)

    if "episodes" in episodes_data:
        if episode_str in episodes_data["episodes"]:
            youtube_id = episodes_data["episodes"][episode_str]
            return youtube_id if youtube_id else None

    return None

def episode_to_filename(episode):
    """
    Convert episode number to filename format

    Args:
        episode (int): Episode number (1-150)

    Returns:
        str: Filename prefix (e.g., "ertugrul-1-01" or "ertugrul-2-001")
    """
    # Season 1: Episodes 1-76
    # Season 2: Episodes 77-99
    # Season 3: Episodes 100-126
    # Season 4: Episodes 127-150

    if episode <= 76:
        season = 1
        ep_in_season = episode
        return f"ertugrul-{season}-{ep_in_season:02d}"
    elif episode <= 99:
        season = 2
        ep_in_season = episode - 76
        return f"ertugrul-{season}-{ep_in_season:03d}"
    elif episode <= 126:
        season = 3
        ep_in_season = episode - 99
        return f"ertugrul-{season}-{ep_in_season:03d}"
    elif episode <= 150:
        season = 4
        ep_in_season = episode - 126
        return f"ertugrul-{season}-{ep_in_season:03d}"
    else:
        return f"ertugrul-{episode:03d}"

def download_subtitle(episode, language, youtube_id, build_dir):
    """
    Download VTT subtitle for a specific language

    Args:
        episode (int): Episode number (1-150)
        language (str): Language code (en, tr)
        youtube_id (str): YouTube video ID
        build_dir (Path): Build directory path

    Returns:
        bool: True if successful, False otherwise
    """
    # Simple filename format: 001-en.vtt
    output_file = build_dir / f"{episode:03d}-{language}.vtt"

    # Check if already exists
    if output_file.exists():
        print(f"   ✓ {language.upper()}: Already exists")
        return True

    print(f"   📥 Downloading {language.upper()} subtitles...")

    # Construct YouTube URL
    url = f"https://www.youtube.com/watch?v={youtube_id}"

    # Try different cookie sources in order
    cookie_options = [
        ["--cookies-from-browser", "chrome"],
        ["--cookies-from-browser", "safari"],
        ["--cookies-from-browser", "firefox"],
        []  # No cookies as fallback
    ]

    success = False
    temp_prefix = f"{episode:03d}"

    for cookie_option in cookie_options:
        try:
            cmd = [
                "yt-dlp",
                "--write-sub",
                "--write-auto-sub",
                "--sub-lang", language,
                "--sub-format", "vtt",
                "--skip-download",
                "--output", str(build_dir / temp_prefix),
                "--user-agent", "Mozilla/5.0",
                "--sleep-requests", "1",
            ] + cookie_option + [url]

            result = subprocess.run(cmd, check=True, capture_output=True, text=True)

            # Check if subtitle file was downloaded
            # yt-dlp creates files like: 001.lang.vtt
            downloaded_files = list(build_dir.glob(f"{temp_prefix}*.vtt"))

            if downloaded_files:
                # Rename to our standard format
                for downloaded_file in downloaded_files:
                    if language in str(downloaded_file):
                        downloaded_file.rename(output_file)
                        print(f"   ✓ {language.upper()}: Downloaded successfully")
                        success = True
                        break

                if success:
                    break

        except subprocess.CalledProcessError as e:
            if cookie_option:
                cookie_name = cookie_option[1]
                if not success:
                    continue
            else:
                continue

    if not success:
        print(f"   ⚠️  {language.upper()}: Not available")
        return False

    return True

def download_episode_subtitles(episode, youtube_id, dataset="ertugrul"):
    """
    Download both English and Turkish subtitles for an episode

    Args:
        episode (int): Episode number (1-150)
        youtube_id (str): YouTube video ID
        dataset (str): Dataset name (default: "ertugrul")

    Returns:
        dict: Results for each language
    """
    # Create output directory in dataset/subtitles
    # Try both from project root and from python/ directory
    possible_paths = [
        Path(f"../{dataset}/subtitles"),  # From python/ directory
        Path(f"{dataset}/subtitles"),     # From project root
    ]

    build_dir = None
    for path in possible_paths:
        # Check if parent dataset directory exists
        if path.parent.exists():
            build_dir = path
            break

    if build_dir is None:
        # Default to project root if neither exists
        build_dir = Path(f"../{dataset}/subtitles")

    build_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🎬 Processing Ertugrul Episode {episode}")
    print(f"   Output: {episode:03d}-{{en,tr}}.vtt")
    print(f"🔗 Source URL: https://www.youtube.com/watch?v={youtube_id}")

    # Try to check if yt-dlp is installed
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ yt-dlp not found. Please install with: pip install yt-dlp")
        return {"en": False, "tr": False}

    # Download both languages
    results = {}
    results["en"] = download_subtitle(episode, "en", youtube_id, build_dir)
    results["tr"] = download_subtitle(episode, "tr", youtube_id, build_dir)

    return results

def main():
    print("📥 Subtitle Downloader for Ertugrul Language Learning")
    print("=" * 60)
    print("⚠️  IMPORTANT: Only download content you have legal rights to access")
    print("⚠️  This tool is for educational and research purposes only")
    print("=" * 60)

    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  ./download_subtitles.py <dataset> <episode>          # Download from episodes.json")
        print("\nExamples:")
        print("  ./download_subtitles.py ertugrul 3                   # Download Episode 3 from JSON")
        print("\nNote: Downloads both English (en) and Turkish (tr) subtitles")
        sys.exit(1)

    dataset = sys.argv[1]

    # Currently only supports ertugrul dataset
    if dataset != "ertugrul":
        print(f"❌ Unsupported dataset: {dataset}")
        print("Supported datasets: ertugrul")
        sys.exit(1)

    try:
        episode = int(sys.argv[2])
    except (ValueError, IndexError):
        print("❌ Episode must be a number")
        sys.exit(1)

    # Load episodes data from JSON
    episodes_data = load_episodes_json(dataset)
    if not episodes_data:
        sys.exit(1)

    youtube_id = get_youtube_id(episodes_data, episode)
    if not youtube_id:
        print(f"❌ No YouTube ID found for Episode {episode}")
        print(f"   Please add it to {dataset}/episodes.json")
        sys.exit(1)

    print(f"🎯 Using YouTube ID from episodes.json: {youtube_id}")

    # Download subtitles
    results = download_episode_subtitles(episode, youtube_id, dataset)

    # Show summary
    print(f"\n📊 Download Summary for Episode {episode:03d}:")
    if results["en"]:
        print(f"   ✅ English subtitles: {dataset}/subtitles/{episode:03d}-en.vtt")
    else:
        print(f"   ❌ English subtitles: Not available")

    if results["tr"]:
        print(f"   ✅ Turkish subtitles: {dataset}/subtitles/{episode:03d}-tr.vtt")
    else:
        print(f"   ❌ Turkish subtitles: Not available")

    if results["en"] or results["tr"]:
        print(f"\n🎉 Episode {episode:03d} completed!")
    else:
        print(f"\n❌ Failed to download any subtitles for Episode {episode:03d}")
        sys.exit(1)

if __name__ == "__main__":
    main()
