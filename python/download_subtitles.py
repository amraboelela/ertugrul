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

# Import VTT to JSON conversion function
from vtt_to_json import convert_vtt_to_json

# Import translation function
try:
    from translate_subtitles import translate_vtt_file
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False

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

    Downloads manual subtitles, auto-generated subtitles, or auto-translated subtitles.
    For English, this includes YouTube's auto-translate feature which can translate
    Turkish (or other available languages) to English.

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

    lang_name = "English (may be auto-translated)" if language == "en" else "Turkish"
    print(f"   📥 Downloading {lang_name} subtitles...")

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
            # For English: Try to download any English subtitle variant
            # This includes auto-translated versions
            if language == "en":
                cmd = [
                    "yt-dlp",
                    "--write-auto-sub",
                    "--sub-langs", "en.*",        # Match any English variant using regex
                    "--sub-format", "vtt",
                    "--skip-download",
                    "--output", str(build_dir / temp_prefix),
                    "--user-agent", "Mozilla/5.0",
                    "--sleep-requests", "1",
                ] + cookie_option + [url]
            else:
                cmd = [
                    "yt-dlp",
                    "--write-sub",
                    "--write-auto-sub",
                    "--sub-langs", language,
                    "--sub-format", "vtt",
                    "--skip-download",
                    "--output", str(build_dir / temp_prefix),
                    "--user-agent", "Mozilla/5.0",
                    "--sleep-requests", "1",
                ] + cookie_option + [url]

            result = subprocess.run(cmd, capture_output=True, text=True)

            # Check if subtitle file was downloaded
            # yt-dlp creates files like: 001.en.vtt (auto-translated), 001.tr.vtt
            downloaded_files = list(build_dir.glob(f"{temp_prefix}*.vtt"))

            if downloaded_files:
                # Rename to our standard format
                # Prefer en-TR variant over plain en for better alignment
                target_file = None

                if language == "en":
                    # First try to find en-tr variant (better alignment)
                    for downloaded_file in downloaded_files:
                        if "en-tr" in str(downloaded_file).lower():
                            target_file = downloaded_file
                            break

                    # Fallback to any en file
                    if not target_file:
                        for downloaded_file in downloaded_files:
                            if "en" in str(downloaded_file).lower():
                                target_file = downloaded_file
                                break
                else:
                    # For Turkish, just find the tr file
                    for downloaded_file in downloaded_files:
                        if language in str(downloaded_file):
                            target_file = downloaded_file
                            break

                if target_file:
                    target_file.rename(output_file)

                    # Clean up yt-dlp temporary files with dot notation (e.g., 006.en.vtt)
                    # Keep our renamed files with dash notation (e.g., 006-en.vtt)
                    for leftover_file in downloaded_files:
                        # Only delete files with dots before the language code (yt-dlp format)
                        if leftover_file != target_file and '.' in leftover_file.stem and leftover_file.exists():
                            leftover_file.unlink()

                    # Report success
                    if language == "en":
                        print(f"   ✓ {language.upper()}: Downloaded (auto-translated from Turkish)")
                    else:
                        print(f"   ✓ {language.upper()}: Downloaded successfully")
                    success = True
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

def count_vtt_segments(vtt_path):
    """
    Count the number of subtitle segments in a VTT file

    Args:
        vtt_path (Path): Path to VTT file

    Returns:
        int: Number of subtitle segments
    """
    if not vtt_path.exists():
        return 0

    try:
        with open(vtt_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Count timestamp lines (segments have format: HH:MM:SS.mmm --> HH:MM:SS.mmm)
        import re
        segments = re.findall(r'\d{2}:\d{2}:\d{2}\.\d{3}\s+-->\s+\d{2}:\d{2}:\d{2}\.\d{3}', content)
        return len(segments)
    except:
        return 0

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
    # Create output directory in dataset/subtitles/temp
    # Try both from project root and from python/ directory
    possible_paths = [
        Path(f"../{dataset}/subtitles/temp"),  # From python/ directory
        Path(f"{dataset}/subtitles/temp"),     # From project root
    ]

    build_dir = None
    for path in possible_paths:
        # Check if parent dataset directory exists
        if path.parent.parent.exists():
            build_dir = path
            break

    if build_dir is None:
        # Default to project root if neither exists
        build_dir = Path(f"../{dataset}/subtitles/temp")

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

    # If English download failed but Turkish succeeded, try AI translation as fallback
    if not results["en"] and results["tr"] and TRANSLATOR_AVAILABLE:
        tr_vtt = build_dir / f"{episode:03d}-tr.vtt"
        en_vtt = build_dir / f"{episode:03d}-en.vtt"

        # Check for incomplete previous translation and clean up
        if en_vtt.exists():
            tr_count = count_vtt_segments(tr_vtt)
            en_count = count_vtt_segments(en_vtt)

            if en_count < tr_count:
                print(f"   🧹 Detected incomplete translation ({en_count}/{tr_count} segments)")
                print(f"   🗑️  Cleaning up partial files...")

                # Delete partial English VTT
                en_vtt.unlink()
                print(f"      Deleted: {en_vtt.name}")

                # Delete partial JSON files (with ~ suffix)
                possible_paths_main = [
                    Path(f"../{dataset}/subtitles"),  # From python/ directory
                    Path(f"{dataset}/subtitles"),     # From project root
                ]

                for main_path in possible_paths_main:
                    if main_path.exists():
                        # Delete partial JSON with ~ suffix
                        partial_json = main_path / f"{episode:03d}~.json"
                        if partial_json.exists():
                            partial_json.unlink()
                            print(f"      Deleted: {partial_json.name}")

                        # Delete final JSON if it exists
                        final_json = main_path / f"{episode:03d}.json"
                        if final_json.exists():
                            final_json.unlink()
                            print(f"      Deleted: {final_json.name}")
                        break

                print(f"   ✅ Ready to restart translation from scratch")

        print(f"   🤖 YouTube auto-translate not available, using AI translation...")
        if translate_vtt_file(tr_vtt, en_vtt):
            results["en"] = True

    return results

def process_episode(dataset, episode, episodes_data):
    """
    Process a single episode: download and convert to JSON

    Args:
        dataset (str): Dataset name
        episode (int): Episode number
        episodes_data (dict): Episodes data from JSON

    Returns:
        bool: True if successful, False otherwise
    """
    # Check if JSON already exists
    possible_paths_main = [
        Path(f"../{dataset}/subtitles"),  # From python/ directory
        Path(f"{dataset}/subtitles"),     # From project root
    ]

    main_dir = None
    for path in possible_paths_main:
        if path.exists():
            main_dir = path
            break

    if main_dir:
        output_json = main_dir / f"{episode:03d}.json"
        if output_json.exists():
            print(f"⏭️  Episode {episode:03d} already exists, skipping...")
            return True

    youtube_id = get_youtube_id(episodes_data, episode)
    if not youtube_id:
        print(f"❌ No YouTube ID found for Episode {episode}")
        return False

    print(f"🎯 Using YouTube ID: {youtube_id}")

    # Download subtitles
    results = download_episode_subtitles(episode, youtube_id, dataset)

    # Show summary
    print(f"\n📊 Download Summary for Episode {episode:03d}:")
    if results["en"]:
        print(f"   ✅ English subtitles: {dataset}/subtitles/temp/{episode:03d}-en.vtt")
    else:
        print(f"   ❌ English subtitles: Not available")

    if results["tr"]:
        print(f"   ✅ Turkish subtitles: {dataset}/subtitles/temp/{episode:03d}-tr.vtt")
    else:
        print(f"   ❌ Turkish subtitles: Not available")

    # Convert to JSON if both subtitles are available
    if results["en"] and results["tr"]:
        # Find subtitle directory
        possible_paths_temp = [
            Path(f"../{dataset}/subtitles/temp"),  # From python/ directory
            Path(f"{dataset}/subtitles/temp"),     # From project root
        ]
        possible_paths_main = [
            Path(f"../{dataset}/subtitles"),  # From python/ directory
            Path(f"{dataset}/subtitles"),     # From project root
        ]

        temp_dir = None
        for path in possible_paths_temp:
            if path.exists():
                temp_dir = path
                break

        main_dir = None
        for path in possible_paths_main:
            if path.exists():
                main_dir = path
                break

        if temp_dir and main_dir:
            tr_vtt = temp_dir / f"{episode:03d}-tr.vtt"
            en_vtt = temp_dir / f"{episode:03d}-en.vtt"
            output_json = main_dir / f"{episode:03d}.json"

            try:
                convert_vtt_to_json(tr_vtt, en_vtt, output_json)
                print(f"   ✅ JSON format: {dataset}/subtitles/{episode:03d}.json")
            except Exception as e:
                print(f"   ⚠️  JSON conversion failed: {e}")
                return False

    if results["en"] or results["tr"]:
        print(f"\n🎉 Episode {episode:03d} completed!")
        return True
    else:
        print(f"\n❌ Failed to download any subtitles for Episode {episode:03d}")
        return False

def main():
    print("📥 Subtitle Downloader for Ertugrul Language Learning")
    print("=" * 60)
    print("⚠️  IMPORTANT: Only download content you have legal rights to access")
    print("⚠️  This tool is for educational and research purposes only")
    print("=" * 60)

    if len(sys.argv) < 2:
        print("\nUsage:")
        print("  ./download_subtitles.py <dataset>                    # Download ALL episodes")
        print("  ./download_subtitles.py <dataset> <episode>          # Download specific episode")
        print("\nExamples:")
        print("  ./download_subtitles.py ertugrul                     # Download all 150 episodes")
        print("  ./download_subtitles.py ertugrul 3                   # Download Episode 3 only")
        print("\nNote: Downloads both English (en) and Turkish (tr) subtitles")
        sys.exit(1)

    dataset = sys.argv[1]

    # Currently only supports ertugrul dataset
    if dataset != "ertugrul":
        print(f"❌ Unsupported dataset: {dataset}")
        print("Supported datasets: ertugrul")
        sys.exit(1)

    # Load episodes data from JSON
    episodes_data = load_episodes_json(dataset)
    if not episodes_data:
        sys.exit(1)

    # Check if specific episode or all episodes
    if len(sys.argv) >= 3:
        # Single episode mode
        try:
            episode = int(sys.argv[2])
        except ValueError:
            print("❌ Episode must be a number")
            sys.exit(1)

        success = process_episode(dataset, episode, episodes_data)
        if not success:
            sys.exit(1)
    else:
        # Batch mode - process all episodes
        print(f"\n🚀 Batch Mode: Processing ALL episodes from {dataset}/episodes.json")

        # Get all episode numbers from JSON
        if "episodes" not in episodes_data:
            print("❌ No episodes found in episodes.json")
            sys.exit(1)

        episode_numbers = sorted([int(ep) for ep in episodes_data["episodes"].keys()])
        total_episodes = len(episode_numbers)

        print(f"📋 Found {total_episodes} episodes to process (Episodes {episode_numbers[0]}-{episode_numbers[-1]})")
        print()

        # Process each episode
        success_count = 0
        failed_episodes = []

        for i, episode in enumerate(episode_numbers, 1):
            print(f"\n{'='*60}")
            print(f"Processing Episode {episode:03d} ({i}/{total_episodes})")
            print(f"{'='*60}")

            success = process_episode(dataset, episode, episodes_data)
            if success:
                success_count += 1
            else:
                failed_episodes.append(episode)

        # Final summary
        print(f"\n{'='*60}")
        print(f"🏁 BATCH PROCESSING COMPLETE")
        print(f"{'='*60}")
        print(f"✅ Successful: {success_count}/{total_episodes} episodes")
        if failed_episodes:
            print(f"❌ Failed: {len(failed_episodes)} episodes")
            print(f"   Failed episodes: {', '.join(map(str, failed_episodes))}")
        else:
            print(f"🎉 All episodes processed successfully!")
        print(f"{'='*60}")

if __name__ == "__main__":
    main()
