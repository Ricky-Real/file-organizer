# File Organizer

A simple command-line file organizer written in Python.

The program sorts files into categories based on their file extensions and places them into an `output` directory.

## Features

- Organizes files by file type
- Optional recursive sorting
- Dry-run mode
- Creates category directories automatically
- Keeps the output directory separate from the input
- Removes empty source directories after recursive sorting
- Handles duplicate filenames by adding a number suffix
- Uses only Python's standard library

## Categories

The organizer currently supports:

- Documents
- Text
- Spreadsheets
- Presentations
- Images
- Audio
- Videos
- Archives
- Disk Images
- Code
- Executables

Unknown file types are left untouched.

## Requirements

- Python 3.9 or newer
- No external Python packages are required

## Usage

### Basic sorting

```bash
python3 organizer.py ~/Downloads
```

### Recursive sorting
```bash
python3 organizer.py ~/Downloads --recursive
```

### Dry run
```bash
python3 organizer.py ~/Downloads --recursive
```
### Recursive dry run
```bash
python3 organizer.py ~/Downloads --recursive --dry-run
```

### Short options
```bash
python3 organizer.py ~/Downloads -r
```
```bash
python3 organizer.py ~/Downloads -dr
```
## Example

### Running
```bash
python3 organizer.py ~/Downloads -r
```

### Before
```
Downloads/
├── photo.jpg
├── document.pdf
├── song.mp3
└── projects/
    ├── script.py
    └── archive.zip
```
### After
```
Downloads/
└── output/
    ├── Documents/
    │   └── document.pdf
    ├── Images/
    │   └── photo.jpg
    ├── Audio/
    │   └── song.mp3
    ├── Archives/
    │   └── archive.zip
    └── Code/
        └── script.py
```
## Safety

Use `--dry-run` before organizing an unfamilliar directory.
The dry run only displays the files that would be organized. **It does not move or delete anything.**

## License
The MIT License (MIT). Please see [License File](LICENSE) for more information.