import argparse
import subprocess
import json
import os


def run_cli_command(command: str) -> dict:
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return {"command": command, "output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        print(f'Command Failed. Command: {command}, Output: {e.output.strip()}, Error: {e.stderr.strip()}')
        exit(1)


def split_audiobook(input_file: str, base_dir: str):
    chapters, tags = extract_audiobook_metadata(input_file)
    album_name = tags.get('title')
    output_dir = create_output_directory(base_dir, album_name)
    number_of_tracks = len(chapters)
    for track_number, chapter in enumerate(chapters, start=1):
        chapter_name = chapter.get('tags').get('title')
        start_time = chapter.get('start_time')
        end_time = chapter.get('end_time')
        file_name = f'{chapter_name}.mp3'
        print(f'Creating "{file_name}" in directory {output_dir}')
        run_cli_command(
            f'ffmpeg -y -accurate_seek -ss {start_time} -to {end_time} -i "{input_file}" -c:a libmp3lame -b:a 192k'
            f' -metadata track={track_number}/{number_of_tracks} '
            f' -metadata album="{album_name}" '
            f' -metadata title="{chapter_name}" '
            f' "{output_dir}/{file_name}"')


def create_output_directory(base_dir, album_name):
    output_dir = f'{base_dir}/{album_name}'
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def extract_audiobook_metadata(input_file):
    response = run_cli_command(f'ffprobe -v quiet -print_format json -show_format -show_chapters "{input_file}"')
    response_json = json.loads(response.get('output'))
    chapters = response_json.get('chapters')
    chapters_filtered = [chapter for chapter in chapters if 'chapter' in str.lower(chapter.get('tags').get('title'))]
    tags = response_json.get('format').get('tags')
    return chapters_filtered, tags


def main():
    parser = argparse.ArgumentParser(description="Audiobook tool which converts an m4b file to multiple mp3 files (one per chapter)")
    parser.add_argument("--input", type=str, help="Input audiobook.")
    parser.add_argument("--output", type=str, help="Output directory for processed files.")
    args = parser.parse_args()

    split_audiobook(args.input, args.output)


if __name__ == "__main__":
    main()
