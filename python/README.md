# Python Scripts for Ertugrul Language Learning

Modern Python tools for downloading and processing Ertugrul content for language learning.

## Scripts

### download_subtitles.py

Downloads VTT subtitle files from YouTube for language learning.

**Features:**
- Downloads both English and Turkish subtitles automatically
- Reads YouTube IDs from `ertugrul/episodes.json`
- Follows project naming conventions
- Uses yt-dlp with fallback cookie options

**Usage:**

```bash
# Download using episodes.json
python3 python/download_subtitles.py ertugrul 3
```

**Requirements:**

```bash
pip install yt-dlp
```

**Output:**
- Files are saved to `ertugrul/subtitles/{episode}-{lang}.vtt`
- Episode numbers are absolute (1-150)
  - Episode 1 → `ertugrul/subtitles/001-en.vtt`, `ertugrul/subtitles/001-tr.vtt`
  - Episode 77 → `ertugrul/subtitles/077-en.vtt`, `ertugrul/subtitles/077-tr.vtt`
  - Episode 100 → `ertugrul/subtitles/100-en.vtt`, `ertugrul/subtitles/100-tr.vtt`

**Supported Languages:**
- `en` - English (automatically downloaded)
- `tr` - Turkish (automatically downloaded)

## Directory Structure

```
python/
├── download_subtitles.py   # VTT subtitle downloader
└── README.md               # This file
```

## Notes

- YouTube IDs are stored in `ertugrul/episodes.json`
- All scripts are designed for educational and research purposes only
- Users must have legal rights to access the content

Created by Amr Aboelela
