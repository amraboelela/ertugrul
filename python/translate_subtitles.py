#!/usr/bin/env python3
"""
Subtitle Translator for Ertugrul Language Learning Project

Translates Turkish VTT subtitle files to English using NLLB (Meta's AI model).
Used as fallback when YouTube doesn't provide auto-translated English subtitles.

Usage: ./translate_subtitles.py <dataset> <episode>
       ./translate_subtitles.py ertugrul 36

Created by Amr Aboelela
"""

import os
import sys
from pathlib import Path

# Try to import NLLB translation library
try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False

# Global model cache
_model = None
_tokenizer = None

def get_translator():
    """
    Load NLLB model (cached after first load)

    Returns:
        tuple: (model, tokenizer) or (None, None) if unavailable
    """
    global _model, _tokenizer

    if not TRANSLATOR_AVAILABLE:
        return None, None

    if _model is None:
        print("📦 Loading NLLB translation model (this may take a moment on first run)...")
        try:
            # Use smaller distilled model for faster performance
            model_name = "facebook/nllb-200-distilled-600M"
            _tokenizer = AutoTokenizer.from_pretrained(model_name)
            _model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            return None, None

    return _model, _tokenizer

def translate_text(text, model, tokenizer):
    """
    Translate Turkish text to English using NLLB

    Args:
        text (str): Turkish text to translate
        model: NLLB model
        tokenizer: NLLB tokenizer

    Returns:
        str: Translated English text
    """
    try:
        # NLLB language codes: tur_Latn (Turkish), eng_Latn (English)
        tokenizer.src_lang = "tur_Latn"
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

        # Get the token ID for English target language
        eng_token_id = tokenizer.convert_tokens_to_ids("eng_Latn")

        # Generate translation
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=eng_token_id,
            max_length=512
        )

        # Decode the translation
        translation = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
        return translation

    except Exception as e:
        print(f"   ⚠️  Translation error: {e}")
        return text  # Return original if translation fails

def translate_vtt_file(tr_vtt_path, en_vtt_path):
    """
    Translate Turkish VTT file to English using AI translation

    Args:
        tr_vtt_path (Path): Turkish VTT file path
        en_vtt_path (Path): Output English VTT file path

    Returns:
        bool: True if successful
    """
    if not TRANSLATOR_AVAILABLE:
        print("❌ transformers library not installed")
        print("   Install with: pip install transformers")
        return False

    print(f"🤖 Translating Turkish → English using AI...")
    print(f"   Input:  {tr_vtt_path}")
    print(f"   Output: {en_vtt_path}")

    try:
        # Load NLLB model
        model, tokenizer = get_translator()
        if model is None or tokenizer is None:
            print("❌ Failed to load translation model")
            return False

        # Import JSON conversion for partial saves
        try:
            from vtt_to_json import convert_vtt_to_json
        except ImportError:
            convert_vtt_to_json = None

        # Read Turkish VTT
        with open(tr_vtt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        translated_lines = []
        in_subtitle_block = False
        subtitle_text = []
        block_count = 0

        # Open output file for writing as we go
        with open(en_vtt_path, 'w', encoding='utf-8') as out_file:
            for line in lines:
                # Copy header lines as-is
                if line.startswith('WEBVTT') or line.startswith('Kind:'):
                    translated_lines.append(line)
                    out_file.write(line)
                    continue

                if line.startswith('Language:'):
                    lang_line = 'Language: en-TR\n'
                    translated_lines.append(lang_line)
                    out_file.write(lang_line)
                    continue

                # Timestamp lines
                if '-->' in line:
                    translated_lines.append(line)
                    out_file.write(line)
                    in_subtitle_block = True
                    subtitle_text = []
                    continue

                # Empty line marks end of subtitle block
                if line.strip() == '' and in_subtitle_block:
                    # Translate accumulated subtitle text
                    if subtitle_text:
                        text_to_translate = '\n'.join(subtitle_text)
                        translated_text = translate_text(text_to_translate, model, tokenizer)
                        translated_line = translated_text + '\n'
                        translated_lines.append(translated_line)
                        out_file.write(translated_line)
                        block_count += 1

                        # Progress update and partial save every 100 segments
                        if block_count % 100 == 0:
                            print(f"   Translated {block_count} segments...")
                            out_file.flush()  # Flush to disk

                            # Save partial JSON if converter available
                            if convert_vtt_to_json:
                                # Determine output JSON path with ~ suffix
                                json_path = en_vtt_path.parent.parent / f"{en_vtt_path.stem.split('-')[0]}~.json"
                                try:
                                    # Suppress output during partial save
                                    import sys
                                    import io
                                    old_stdout = sys.stdout
                                    sys.stdout = io.StringIO()
                                    convert_vtt_to_json(tr_vtt_path, en_vtt_path, json_path)
                                    sys.stdout = old_stdout
                                except:
                                    sys.stdout = old_stdout  # Restore on error
                                    pass  # Ignore errors during partial save

                    translated_lines.append('\n')
                    out_file.write('\n')
                    in_subtitle_block = False
                    subtitle_text = []
                    continue

                # Accumulate subtitle text
                if in_subtitle_block:
                    subtitle_text.append(line.strip())
                else:
                    translated_lines.append(line)
                    out_file.write(line)

        print(f"✅ Translation complete! Translated {block_count} segments")

        # Clean up temporary partial JSON file
        json_path = en_vtt_path.parent.parent / f"{en_vtt_path.stem.split('-')[0]}~.json"
        if json_path.exists():
            json_path.unlink()
            print(f"🧹 Cleaned up temporary file: {json_path.name}")

        return True

    except Exception as e:
        print(f"❌ Translation failed: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  ./translate_subtitles.py <dataset> <episode>")
        print("\nExamples:")
        print("  ./translate_subtitles.py ertugrul 36")
        print("\nNote: Translates Turkish VTT to English using AI when YouTube auto-translate is unavailable")
        sys.exit(1)

    dataset = sys.argv[1]

    try:
        episode = int(sys.argv[2])
    except ValueError:
        print("❌ Episode must be a number")
        sys.exit(1)

    # Find Turkish VTT file
    possible_paths = [
        Path(f"../{dataset}/subtitles/temp"),  # From python/ directory
        Path(f"{dataset}/subtitles/temp"),     # From project root
    ]

    temp_dir = None
    for path in possible_paths:
        if path.exists():
            temp_dir = path
            break

    if temp_dir is None:
        print(f"❌ Subtitles directory not found: {dataset}/subtitles/temp")
        sys.exit(1)

    tr_vtt = temp_dir / f"{episode:03d}-tr.vtt"
    en_vtt = temp_dir / f"{episode:03d}-en.vtt"

    # Check if Turkish VTT exists
    if not tr_vtt.exists():
        print(f"❌ Turkish VTT not found: {tr_vtt}")
        print(f"   Please download Turkish subtitles first using download_subtitles.py")
        sys.exit(1)

    # Check if English already exists
    if en_vtt.exists():
        print(f"⚠️  English VTT already exists: {en_vtt}")
        response = input("   Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("   Skipping translation")
            sys.exit(0)

    print(f"📝 Translating Episode {episode:03d}")
    print(f"{'='*60}\n")

    success = translate_vtt_file(tr_vtt, en_vtt)

    if success:
        print(f"\n{'='*60}")
        print(f"🎉 Episode {episode:03d} translated successfully!")
        print(f"   Output: {en_vtt}")
    else:
        print(f"\n❌ Translation failed for Episode {episode:03d}")
        sys.exit(1)

if __name__ == "__main__":
    main()
