#!/usr/bin/env python3
"""
VTT to JSON Converter for Ertugrul Language Learning Project

Converts VTT subtitle files (Turkish + English) into JSON format
matching the whisper_subtitles structure.

Usage: ./vtt_to_json.py <dataset> <episode>
       ./vtt_to_json.py ertugrul 1

Created by Amr Aboelela
"""

import os
import sys
import json
import re
from pathlib import Path

def parse_vtt(vtt_file):
    """
    Parse a VTT file and extract subtitle entries

    Args:
        vtt_file (Path): Path to VTT file

    Returns:
        list: List of dicts with 'start', 'end', 'text' keys
    """
    subtitles = []

    with open(vtt_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by double newlines to get subtitle blocks
    blocks = re.split(r'\n\n+', content)

    for block in blocks:
        lines = block.strip().split('\n')

        # Skip empty blocks and header
        if not lines or lines[0].startswith('WEBVTT') or lines[0].startswith('Kind:') or lines[0].startswith('Language:'):
            continue

        # Find timestamp line (format: 00:00:19.656 --> 00:00:23.242)
        timestamp_line = None
        text_lines = []

        for i, line in enumerate(lines):
            if '-->' in line:
                timestamp_line = line
                # Everything after timestamp is subtitle text
                text_lines = lines[i+1:]
                break

        if timestamp_line:
            # Parse timestamps
            match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}\.\d{3})', timestamp_line)
            if match:
                start_time = match.group(1)
                end_time = match.group(2)

                # Join text lines and clean
                text = '\n'.join(text_lines).strip()

                if text:  # Only add if there's actual text
                    subtitles.append({
                        'start': start_time,
                        'end': end_time,
                        'text': text
                    })

    return subtitles

def clean_subtitle_text(text):
    """
    Clean subtitle text by removing formatting and excess whitespace

    Args:
        text (str): Raw subtitle text

    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    return text

def timestamp_to_hms(timestamp):
    """
    Convert VTT timestamp from HH:MM:SS.mmm to HH:MM:SS format

    Args:
        timestamp (str): Timestamp in format "HH:MM:SS.mmm"

    Returns:
        str: Timestamp in format "HH:MM:SS"
    """
    # Remove milliseconds (everything after the dot)
    return timestamp.split('.')[0]

def convert_vtt_to_json(tr_vtt, en_vtt, output_json):
    """
    Convert Turkish and English VTT files to JSON format

    Args:
        tr_vtt (Path): Turkish VTT file path
        en_vtt (Path): English VTT file path
        output_json (Path): Output JSON file path

    Returns:
        bool: True if successful
    """
    print(f"📖 Reading Turkish subtitles: {tr_vtt.name}")
    tr_subs = parse_vtt(tr_vtt)

    print(f"📖 Reading English subtitles: {en_vtt.name}")
    en_subs = parse_vtt(en_vtt)

    print(f"   Turkish: {len(tr_subs)} entries")
    print(f"   English: {len(en_subs)} entries")

    # Align subtitles by matching timestamps
    # Assuming they have the same structure (which they should from YouTube)
    segments = []

    # Use the minimum length to avoid index errors
    min_len = min(len(tr_subs), len(en_subs))

    # Match Turkish subtitles with English by timestamp overlap
    for i, tr_sub in enumerate(tr_subs):
        tr_text = clean_subtitle_text(tr_sub['text'])

        # Find matching English subtitle by timestamp
        en_text = ""
        tr_start = tr_sub['start']
        tr_end = tr_sub['end']

        # Find English subtitle that overlaps with this Turkish subtitle
        for en_sub in en_subs:
            # Check if there's any time overlap
            if en_sub['start'] <= tr_end and en_sub['end'] >= tr_start:
                en_text = clean_subtitle_text(en_sub['text'])
                break

        # Only add if we have Turkish text
        if tr_text:
            segments.append({
                "time": timestamp_to_hms(tr_start),
                "text": tr_text,
                "english": en_text if en_text else ""
            })

    # Write JSON output
    print(f"💾 Writing JSON: {output_json.name}")
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    print(f"✅ Created {len(segments)} segments")
    return True

def main():
    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  ./vtt_to_json.py <dataset> <episode>")
        print("\nExamples:")
        print("  ./vtt_to_json.py ertugrul 1")
        sys.exit(1)

    dataset = sys.argv[1]

    try:
        episode = int(sys.argv[2])
    except ValueError:
        print("❌ Episode must be a number")
        sys.exit(1)

    # Find subtitle files
    # Try both from project root and from python/ directory
    possible_paths_temp = [
        Path(f"../{dataset}/subtitles/temp"),  # From python/ directory
        Path(f"{dataset}/subtitles/temp"),     # From project root
    ]

    temp_dir = None
    for path in possible_paths_temp:
        if path.exists():
            temp_dir = path
            break

    if temp_dir is None:
        print(f"❌ Subtitles temp directory not found: {dataset}/subtitles/temp")
        sys.exit(1)

    # Find output directory (parent of temp)
    possible_paths_main = [
        Path(f"../{dataset}/subtitles"),  # From python/ directory
        Path(f"{dataset}/subtitles"),     # From project root
    ]

    main_dir = None
    for path in possible_paths_main:
        if path.exists():
            main_dir = path
            break

    if main_dir is None:
        print(f"❌ Subtitles directory not found: {dataset}/subtitles")
        sys.exit(1)

    # Input files (from temp directory)
    tr_vtt = temp_dir / f"{episode:03d}-tr.vtt"
    en_vtt = temp_dir / f"{episode:03d}-en.vtt"

    # Output file (main subtitles directory)
    output_json = main_dir / f"{episode:03d}.json"

    # Check if input files exist
    if not tr_vtt.exists():
        print(f"❌ Turkish VTT not found: {tr_vtt}")
        sys.exit(1)

    if not en_vtt.exists():
        print(f"❌ English VTT not found: {en_vtt}")
        sys.exit(1)

    print(f"🔄 Converting Episode {episode:03d} VTT → JSON")
    print(f"   Turkish:  {tr_vtt}")
    print(f"   English:  {en_vtt}")
    print(f"   Output:   {output_json}")
    print()

    # Convert
    success = convert_vtt_to_json(tr_vtt, en_vtt, output_json)

    if success:
        print(f"\n🎉 Successfully created {output_json}")
    else:
        print(f"\n❌ Failed to convert episode {episode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
