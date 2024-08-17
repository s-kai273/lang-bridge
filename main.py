import argparse
import os
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment

def list_files_in_dir(directory):
    """
    List all files in a given directory.

    Parameters:
        directory (str): The directory to list files from.

    Returns:
        list: A list of file paths.
    """
    try:
        return [
            os.path.join(directory, f) for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        return []

def text_to_speech(text, lang="en"):
    """
    Convert a given text to speech using gTTS.

    Parameters:
        text (str): The text to convert.
        lang (str): The language for the text-to-speech conversion.

    Returns:
        AudioSegment: An AudioSegment containing the spoken text.
    """
    tts = gTTS(text, lang=lang)
    buffer = BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    return AudioSegment.from_file(buffer, format="mp3")

def generate_audio_file(input_path, output_path, silence_duration):
    """
    Generate an audio file from a text file, with silence between lines.

    Parameters:
        input_path (str): The path to the input text file.
        output_path (str): The path to the output audio file.
        silence_duration (int): Duration of silence between lines (in milliseconds).
    """
    silent_segment = AudioSegment.silent(duration=silence_duration)
    combined_audio = AudioSegment.silent(duration=1)[:0]  # Start with an empty audio segment

    try:
        with open(input_path, "r", encoding="utf-8") as file:
            for line in file:
                text = line.strip()
                if not text:
                    continue
                combined_audio += text_to_speech(text) + silent_segment
    except Exception as e:
        print(f"Error processing file '{input_path}': {e}")
        return
    
    try:
        combined_audio.export(output_path, format="mp3")
        print(f"Audio file generated: {output_path}")
    except Exception as e:
        print(f"Error exporting audio file '{output_path}': {e}")

def main():
    """
    Main function to parse arguments and generate audio files.
    """
    parser = argparse.ArgumentParser(description="Generate audio files from input directory texts to output directory")
    parser.add_argument("-i", "--input_dir", type=str, required=True, help="Input directory containing text files")
    parser.add_argument("-o", "--output_dir", type=str, required=True, help="Output directory for generated audio files")
    parser.add_argument("--silence_duration", type=int, default=2000, help="Silence duration between text line (default: 2000)")
    args = parser.parse_args()
    
    input_files = list_files_in_dir(args.input_dir)
    if not input_files:
        print("No files to process.")
        return

    os.makedirs(args.output_dir, exist_ok=True)

    for input_path in input_files:
        input_file_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(args.output_dir, f"{input_file_name}.mp3")
        generate_audio_file(input_path, output_path, args.silence_duration)
    
if __name__ == "__main__":
    main()
