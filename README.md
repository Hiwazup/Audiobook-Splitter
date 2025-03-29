# Audiobook Splitter

This Python script splits an audiobook (in `.m4b` format) into multiple MP3 files, with each MP3 file corresponding to a
chapter in the audiobook. The script uses `ffmpeg` to process the audiobook file and `ffprobe` to extract metadata such
as chapters and album information.

## Requirements

Before using this script, you need to have the following installed:

- Python 3.x
- `ffmpeg` and `ffprobe` (part of the FFmpeg suite)
- `argparse`, `json`, and `os` (standard Python libraries)

To install FFmpeg, you can follow the instructions on the [FFmpeg website](https://ffmpeg.org/download.html).

## How to Use

### Command-Line Arguments

- `--input`: The path to the input `.m4b` audiobook file.
- `--output`: The path to the output directory where the MP3 files will be saved.

### Example Usage

 ```bash
 python splitter.py --input path/to/audiobook.m4b --output path/to/output/directory
 ```

This command will:

1. Read the `.m4b` file specified in `--input`.
2. Extract chapter information and other metadata using `ffprobe`.
3. Split the audiobook into MP3 files, one for each chapter, in the directory specified by `--output`.
4. Set the track number, album name, and chapter title as metadata for each MP3 file.

### Example Command

 ```bash
 python splitter.py --input "/path/to/audiobook.m4b" --output "/path/to/output"
 ```

### Directory Structure

The script will create a directory based on the album name and place the MP3 files in that directory. For example, if
the album name is "Great Audiobook," the output directory might look like:

 ```
 /path/to/output/Great Audiobook/
     ├── Chapter 1.mp3
     ├── Chapter 2.mp3
     ├── Chapter 3.mp3
     └── ...
 ```

## How It Works

1. **Metadata Extraction**: The script uses `ffprobe` to gather information about the chapters and album metadata from
   the `.m4b` file.
2. **Splitting the Audiobook**: Using `ffmpeg`, the script extracts individual chapters based on start and end times and
   saves them as MP3 files.
3. **Metadata Update**: The script updates the MP3 files' metadata to reflect the correct track number, album name, and
   chapter title.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.