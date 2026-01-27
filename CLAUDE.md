# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python toolkit for creating language learning materials from Resurrection Ertugrul TV series. Processes video subtitles, translates them between languages (Turkish, Arabic, English), and generates interactive learning content with synchronized video clips.

## Project Structure

```
ertugrul/
├── scripts/              # Legacy shell and Python scripts
│   ├── build.py         # Main build orchestrator
│   ├── build.sh         # Convenience wrapper for building
│   ├── buildEpisode     # Episode build pipeline script
│   ├── clean.py         # Clean multiple episodes
│   ├── clean            # Convenience wrapper for cleaning
│   ├── cleanEpisode     # Clean single episode
│   ├── translate.py     # Language translation
│   ├── dictionary.py    # Dictionary builder
│   ├── cut.py           # Video segmentation
│   ├── combine.py       # Video concatenation
│   ├── subtitles.py     # Dual-language subtitle generation
│   └── ...              # Other processing scripts
├── python/              # Modern Python tools
│   ├── download_subtitles.py  # VTT subtitle downloader (uses yt-dlp)
│   └── README.md        # Python tools documentation
├── ertugrul/            # Dataset directory (matches Turkish2English structure)
│   ├── episodes.json        # YouTube IDs for all 150 episodes
│   ├── subtitles/           # Downloaded VTT subtitle files
│   │   └── {episode}-{lang}.vtt   # Episode subtitles (001-en.vtt, 001-tr.vtt, etc.)
│   └── whisper_subtitles/   # Whisper-generated episode transcripts
│       └── *.json           # Episode files (001.json, 002.json, etc.)
├── build/               # Generated learning materials
├── CLAUDE.md            # This file
└── README.md            # User documentation
```

## Key Technologies

- **Python 3**: Core processing scripts
- **FFmpeg**: Video/audio cutting, filtering, concatenation
- **Google Translate API**: Translation (requires `translation_key.py` with API key)
- **gTTS**: Text-to-speech generation
- **youtube-dl**: Video downloading
- **HandBrake**: Subtitle burning into video

## Core Architecture

### Processing Pipeline

The system follows a multi-stage pipeline orchestrated by `scripts/buildEpisode` shell script:

1. **Download & Extract** (`scripts/download`): Downloads episode video and audio
2. **Translation** (`scripts/translate.py`): Converts English VTT subtitles to target language using Google Translate API
3. **Dictionary Building** (`scripts/dictionary.py`): Extracts vocabulary from subtitles, translates words to English, maintains sorted dictionary files
4. **Video Cutting** (`scripts/cut.py`): Splits video/audio into segments based on subtitle timestamps with duration filtering
5. **Frame Processing** (`scripts/video2frames.py`, `scripts/editFrames.py`, `scripts/frames2video.py`): Extracts frames, processes them, regenerates video
6. **Combination** (`scripts/combine.py`): Concatenates segments into batches of 100, then merges batches into final video
7. **Subtitle Generation** (`scripts/subtitleWords.py`, `scripts/subtitles.py`): Creates dual-language subtitles with timing synchronization
8. **Subtitle Burning** (HandBrake): Burns SRT subtitles into video with white target language text and yellow English translations

### File Naming Convention

All files follow the pattern: `{title}-{season}-{episode}-{language}.{ext}`
- Example: `ertugrul-1-01-tr.vtt` (season 1, episode 01, Turkish subtitles)
- Season 2+ uses 3-digit episode numbers: `ertugrul-2-001-tr.vtt`
- Episode segments: `ertugrul-1-01-001-tr.mp4` (episode with segment number)

### Directory Structure

```
build/
├── ertugrul-{s}-{ep}-{lang}.vtt     # Subtitle files (VTT/TTML)
├── ertugrul-{s}-{ep}-{lang}.mp4     # Source video/audio
├── ertugrul-{s}-{ep}/               # Episode working directory
│   └── ertugrul-{s}-{ep}-{seg}-{lang}-{stage}.mp4  # Segmented clips
├── ertugrul-{s}-{ep}-{stage}.mp4    # Intermediate batch files
├── ertugrul-{s}-{ep}.srt            # Dual-language subtitles
├── dictionary-{lang}.txt            # Language dictionaries (word: meaning)
└── durationsLimit-{lang}.txt        # Per-episode duration thresholds

text/
└── {episode}.json                   # Structured episode transcripts with segments
```

### Duration Filtering

The `durationLimit.py` module provides critical filtering logic:
- **Lower Limit**: Per-episode thresholds in `durationsLimit-{lang}.txt` filter out too-short segments
- **Upper Limit**: Language-specific max duration (22s for Turkish, unlimited for Arabic)
- **Timestamp Adjustment**: Arabic subtitles require time-shifting offsets (60-120s depending on episode) to sync with video

### Subtitle Processing Flow

`scripts/subtitles.py` performs complex dual-language synchronization:
1. Reads source English VTT and target language VTT
2. Parses timestamps and groups lines into paragraphs based on duration thresholds
3. Matches English paragraphs to target language paragraphs by timestamp proximity
4. Generates SRT with target language (white) and English translation (yellow) on separate lines
5. Calculates timing from actual video segment durations using `ffprobe`

### Video Concatenation Strategy

`scripts/combine.py` uses two-stage concatenation to handle FFmpeg limitations:
1. **Stage 1**: Concatenate segments into batches of 100 clips (prevents FFmpeg input limit errors)
   - Creates: `ertugrul-1-01-01-c.mp4`, `ertugrul-1-01-02-c.mp4`, etc.
2. **Stage 2**: Concatenate all batches into final video
   - Creates: `ertugrul-1-01-c.mp4`

## Common Commands

### Modern Python Tools (Recommended)

```bash
# Download English and Turkish subtitles for Episode 3
python3 python/download_subtitles.py ertugrul 3
```

**Note:**
- Episode numbers are absolute (1-150), not season-based
- Both English and Turkish subtitles are downloaded automatically
- English subtitles support YouTube's auto-translate feature
  - Downloads native English, auto-generated English, or auto-translated English from Turkish
- Downloaded files use simple format: `001-en.vtt`, `001-tr.vtt`, `100-en.vtt`, etc.
- YouTube IDs must be in `ertugrul/episodes.json`

### Legacy Build Scripts

### Build Episodes

```bash
# Build single episode (season 1, episode 1, English→Turkish)
scripts/build.sh 1 1 en tr

# Build episode range (season 1, episodes 3-8, English→Arabic)
python3 scripts/build.py ertugrul 1 3 8 en ar

# Build directly with buildEpisode
scripts/buildEpisode ertugrul-1-01 en tr
```

### Clean Episodes

```bash
# Remove all generated files for an episode
scripts/clean 1 1 en tr

# Clean specific episode
scripts/cleanEpisode ertugrul-1-01 en tr
```

### Individual Processing Steps

```bash
# Extract/download subtitles for Turkish
scripts/download ertugrul tr

# Translate subtitles
python scripts/translate.py build/ertugrul-1-01-en.vtt ar > build/ertugrul-1-01-ar.vtt

# Build dictionary
python3 scripts/dictionary.py ertugrul-1-01 tr

# Cut video into segments
python scripts/cut.py ertugrul-1-01 tr

# Combine segments
python scripts/combine.py ertugrul-1-01 tr c

# Generate dual-language subtitles
python3 scripts/subtitles.py ertugrul-1-01 tr c
```

## Important Development Notes

### API Key Management
- Never commit `translation_key.py` (gitignored)
- File format: `key = "YOUR_GOOGLE_TRANSLATE_API_KEY"`

### File Handling Rules
- Never modify files in `build/` without explicit request
- Never delete `dictionary-*.txt` files (cumulative vocabulary)
- Never delete `durationsLimit-*.txt` files (episode-specific thresholds)
- Respect existing file naming conventions strictly

### Language-Specific Behavior
- **Turkish (tr)**: Uses TTML source files converted to VTT, requires `scripts/ttml2srt.py` conversion
- **Arabic (ar)**: Translated from English VTT, requires timestamp shifting via `scripts/durationLimit.py`
- **English (en)**: Source language, VTT format

### Processing Characteristics
- Volume amplification: All audio clips amplified 4.5x (`-filter:a volume=4.5`)
- Subtitle colors: White for target language, yellow for English
- Frame processing modifies individual frames before video regeneration

### Dataset Files
- `ertugrul/` directory contains episode data (matches Turkish2English structure)
- `ertugrul/episodes.json` contains YouTube IDs for all 150 episodes (Seasons 1-4)
  - Season 1: Episodes 1-76
  - Season 2: Episodes 77-99
  - Season 3: Episodes 100-126
  - Season 4: Episodes 127-150
- `ertugrul/whisper_subtitles/*.json` files contain Whisper-generated transcripts
  - Format: Array of objects with `seg_id`, `text`, `english` fields
  - Used for reference but not directly in processing pipeline

## Episode Numbering

The project uses two numbering systems:
1. **Absolute numbering** (1-150): Used in `ertugrul/episodes.json` for YouTube IDs and downloaded subtitles
   - Downloaded subtitle files: `001-en.vtt`, `077-tr.vtt`, `100-en.vtt`
2. **Season-based numbering** (e.g., S1E01): Used in legacy build files (`ertugrul-1-01-en.vtt`)
   - Build output files: `ertugrul-1-01-en.vtt`, `ertugrul-2-001-tr.vtt`

The `python/download_subtitles.py` script uses simple absolute numbering (001, 002, etc.) for downloaded files.

Created by Amr Aboelela

## Rules
- Do not run download_subtitles.py by yourself
