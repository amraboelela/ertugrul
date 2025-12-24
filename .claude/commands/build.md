Build Ertugrul language learning content. Usage:

/build [season] [episode_start] [episode_end] [source_lang] [target_lang]

Examples:
- /build 1 1 1 en tr (Build episode 1 season 1, English to Turkish)
- /build 1 1 5 en ar (Build episodes 1-5 season 1, English to Arabic)
- /build 2 10 15 en tr (Build episodes 10-15 season 2, English to Turkish)

This command will:
1. Check prerequisites (ffmpeg, dependencies)
2. Download required video content if needed
3. Extract and process subtitles
4. Translate content using Google Translate API
5. Generate learning materials and dictionaries
6. Clean and format output files

The build process creates VTT subtitle files, TTML format files, and language-specific dictionaries in the build/ directory.