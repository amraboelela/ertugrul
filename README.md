# Ertugrul Language Learning Tools

A comprehensive Python toolkit for creating language learning materials from the Resurrection Ertugrul TV series. This project processes video subtitles, translates them, and generates interactive language learning content for Turkish, Arabic, and other languages.

## Features

- **Subtitle Extraction**: Extract subtitles from Ertugrul episodes in multiple formats (VTT, TTML, SRT)
- **Language Translation**: Translate subtitles between English, Turkish, Arabic, and other languages using Google Translate API
- **Audio Processing**: Extract and process audio from video episodes
- **Video Processing**: Frame extraction, video cutting, and video generation with ffmpeg
- **Dictionary Generation**: Build comprehensive dictionaries from processed subtitles
- **Text-to-Speech**: Generate audio pronunciations using gTTS
- **Cleaning Tools**: Clean and format subtitle files for optimal learning

## Project Structure

```
ertugrul/
├── build/                  # Generated learning materials
│   ├── ertugrul-*.vtt     # Subtitle files
│   ├── ertugrul-*.ttml    # TTML subtitle files
│   └── dictionary-*.txt   # Language dictionaries
├── *.py                   # Python processing scripts
├── build.sh               # Main build script
├── clean                  # Cleaning utilities
├── combine                # Video combination tools
└── download               # Video download utilities
```

## Prerequisites

### System Dependencies

```bash
# Install Homebrew (macOS)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

# Install media processing tools
brew install ffmpeg
brew install handbrake

# Install youtube-dl for video downloads
sudo mkdir -p /usr/local/bin
sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
sudo chmod a+rx /usr/local/bin/youtube-dl
```

### Python Dependencies

```bash
# Install Python packages
sudo pip3 install requests
sudo pip3 install gTTS
sudo easy_install -U requests
```

### Google Translate API Setup

Create a `translation_key.py` file with your Google Translate API key:

```python
key = "<PUT THE KEY FROM YOUR GOOGLE TRANSLATE API ACCOUNT>"
```

## Installation

### Option 1: Using Homebrew (Recommended)

```bash
brew install ffmpeg
brew install handbrake
pip3 install -r requirements.txt
```

### Option 2: Building FFmpeg from Source

For the latest FFmpeg features, build from source:

```bash
cd resources
git clone https://git.ffmpeg.org/ffmpeg.git ffmpeg
cd ffmpeg
./configure --prefix=/usr/local --enable-gpl --enable-nonfree --enable-libass \
--enable-libfdk-aac --enable-libfreetype --enable-libmp3lame \
--enable-libtheora --enable-libvorbis --enable-libvpx --enable-libx264 \
--enable-libx265 --enable-libopus --enable-libxvid --samples=fate-suite/
make
sudo make install
```

## Usage

### Turkish Language Learning

Build and process episodes for Turkish language learning:

```bash
# Build episode 1 season 1, translate from English to Turkish
./build.sh 1 1 en tr

# Clean and format the generated files
./clean 1 1 en tr
```

**Example Output Title:** Learn Turkish from Ertugrul Subtitles, 1 - 1

**Learning Features:**
- Listen to Turkish conversation from Resurrection Ertugrul TV series
- See English translations of subtitles
- Access comprehensive Turkish dictionary: [dictionary-tr.txt](build/dictionary-tr.txt)

### Arabic Language Learning

Build and process episodes for Arabic language learning:

```bash
# Build episode 1 season 1, translate from English to Arabic
./build.sh 1 1 en ar

# Clean and format the generated files
./clean 1 1 en ar
```

**Example Output Title:** Learn Arabic from Ertugrul Subtitles, 1 - 1

**Learning Features:**
- Listen to Arabic conversation from Resurrection Ertugrul TV series
- See English translations of subtitles
- Access comprehensive Arabic dictionary: [dictionary-ar.txt](build/dictionary-ar.txt)

### Advanced Usage

#### Processing Multiple Episodes

```bash
# Process episodes 1-5 of season 1
./build.sh 1 5 en tr

# Process specific episode range
python3 build.py ertugrul 1 3 8 en tr  # Episodes 3-8 of season 1
```

#### Individual Script Usage

```bash
# Extract and translate subtitles
python3 subtitles.py episode_file source_lang target_lang

# Generate dictionary from subtitles
python3 dictionary.py language_code

# Convert video formats
python3 audio2video.py input_file output_file

# Cut video segments
python3 cut.py input_file start_time end_time output_file
```

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `build.py` | Main build orchestrator |
| `subtitles.py` | Subtitle extraction and processing |
| `translate.py` | Language translation using Google API |
| `dictionary.py` | Dictionary generation from subtitles |
| `audio2video.py` | Audio to video conversion |
| `cut.py` | Video cutting and segmentation |
| `clean.py` | File cleaning and formatting |
| `combine.py` | Video file combination |
| `ttml2srt.py` | TTML to SRT subtitle conversion |

## Supported Languages

- **Turkish (tr)**: Primary focus language with comprehensive dictionary
- **Arabic (ar)**: Full support with dictionary generation
- **English (en)**: Source language for translations
- **Other languages**: Supported through Google Translate API

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with a sample episode
5. Submit a pull request

## License

See [LICENSE](LICENSE) file for details.

## Acknowledgments

- Resurrection Ertugrul TV Series for providing educational content
- Google Translate API for translation services
- FFmpeg for video processing capabilities
- gTTS for text-to-speech functionality

Created by Amr Aboelela
