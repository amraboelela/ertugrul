# Ertugrul Language Learning Project - Claude Instructions

## Project Overview
This is a Python-based language learning toolkit that processes Resurrection Ertugrul TV series to create educational content for learning Turkish, Arabic, and other languages.

## Key Technologies
- **Python 3**: Core processing scripts
- **FFmpeg**: Video and audio processing
- **Google Translate API**: Language translation
- **gTTS**: Text-to-speech generation
- **youtube-dl**: Video downloading
- **HandBrake**: Video encoding

## Project Structure
- `build/`: Generated learning materials (VTT, TTML, dictionaries)
- `*.py`: Python processing scripts
- Shell scripts: `build.sh`, `clean`, `combine`, etc.
- `ertugrul.xcodeproj/`: Xcode project for organization

## Development Guidelines

### Code Standards
- Follow existing Python style in the codebase
- Use simple, functional programming approach
- Maintain compatibility with existing shell scripts
- Keep scripts focused on single responsibilities

### File Handling
- Never delete or modify files in `build/` directory without explicit request
- Always backup important generated files before processing
- Respect the existing file naming conventions (e.g., `ertugrul-1-01-en.vtt`)

### Language Processing
- Support primary languages: Turkish (tr), Arabic (ar), English (en)
- Use Google Translate API for translations
- Maintain dictionaries in `build/dictionary-*.txt` format
- Follow subtitle format standards (VTT, TTML, SRT)

### Video/Audio Processing
- Use FFmpeg for all media operations
- Preserve original quality when possible
- Follow naming conventions for episodes: `ertugrul-{season}-{episode}-{lang}`
- Handle multiple seasons with proper zero-padding

### Dependencies
- Do not automatically install packages - ask user first
- Respect the manual installation process described in README
- Use existing dependency management approach

### Testing and Validation
- Test with small episode ranges first
- Validate subtitle format consistency
- Check translation quality for common phrases
- Ensure generated dictionaries are properly formatted

## Common Tasks

### Building Episodes
```bash
# Single episode
./build.sh 1 1 en tr

# Episode range
python3 build.py ertugrul 1 3 8 en tr
```

### Cleaning Output
```bash
./clean 1 1 en tr
```

### Individual Processing
- `subtitles.py`: Extract and process subtitles
- `translate.py`: Language translation
- `dictionary.py`: Generate learning dictionaries
- `audio2video.py`: Audio/video conversion

## Important Notes
- Created by Amr Aboelela
- Educational purpose: Language learning through TV series
- Respect copyright and fair use guidelines
- Focus on subtitle processing and translation workflows