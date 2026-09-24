import argparse
from pathlib import Path


CATEGORIES = {
    "Documents": {".pdf", ".doc", ".docx", ".odt", ".rtf", ".pages", ".tex", ".epub", ".mobi"},
    "Text": {".txt", ".md", ".csv", ".log", ".nfo", ".rst"},
    "Spreadsheets": {".xls", ".xlsx", ".xlsm", ".ods", ".numbers"},
    "Presentations": {".ppt", ".pptx", ".odp", ".key"},
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp", ".tiff", ".tif", ".ico", ".heic", ".heif", ".avif", ".raw"},
    "Audio": {".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac", ".wma", ".opus", ".aiff"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv", ".wmv", ".m4v", ".mpeg", ".mpg", ".3gp"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".zst", ".tgz", "tbz2"},
    "Disk Images": {".iso", ".img", ".cue", ".dmg", ".vdi", ".vmdk", ".vhd", ".vhdx"},
    "Code": {".py", ".js", ".ts", ".java", ".c", ".cpp", ".h", ".hpp", ".rs", ".go", ".sh"},
    "Executables": {".exe", ".msi", ".deb", ".rpm", ".appimage", ".run"},

}


EXTENSION_MAP = {extension: category for category, extensions in CATEGORIES.items() for extension in extensions}

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Organize files into folders based on their file type."
    )

    parser.add_argument(
        "folder",
        type=Path,
        help="Folder containing the files to organize.",
    )

    parser.add_argument(
        "-dr",
        "--dry-run",
        action="store_true",
        help="Show what would be organized without moving or deleting anything.",
    )

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Also organize files inside subdirectories.",
    )

    return parser.parse_args()


def collect_files(folder, out_location, recursive):
    files = []

    for item in folder.iterdir():

        if item == out_location:
            continue

        if item.is_dir():
            if recursive:
                files.extend(collect_files(item, out_location, recursive))
            continue

        category = EXTENSION_MAP.get(item.suffix.lower())

        if category:
            files.append((item, category))

    return files


def print_dry_run(files):
    grouped = {category: [] for category in CATEGORIES}

    for file, category in files:
        grouped[category].append(file)

    for category, category_files in grouped.items():

        print("=" * 27)
        print(category)
        print("=" * 27)

        for file in category_files:
            print(file)

        print()


def get_unique_destination(destination):

    if not destination.exists():
        return destination

    counter = 1

    while True:
        candidate = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")

        if not candidate.exists():
            return candidate

        counter += 1


def move_files(files, out_location):

    for file, category in files:

        category_folder = out_location / category

        category_folder.mkdir(parents=True, exist_ok=True)

        destination = get_unique_destination(category_folder / file.name)

        file.rename(destination)


def remove_empty_folders(folder, out_location):

    folders = sorted(folder.rglob("*"), key=lambda path: len(path.parts), reverse=True)

    for item in folders:
        if item.is_dir() and item != out_location:
            try:
                item.rmdir()
            except OSError:
                pass


def main():

    args = parse_arguments()
    folder = args.folder.expanduser().resolve()
    out_location = folder / "output"

    if not folder.is_dir():
        raise SystemExit(f"Error: '{folder}' is not a directory.")

    files = collect_files(folder, out_location, args.recursive)

    if args.dry_run:
        print_dry_run(files)
        return

    out_location.mkdir(exist_ok=True)

    move_files(files, out_location)

    if args.recursive:
        remove_empty_folders(folder, out_location)

    print(f"Organized {len(files)} file(s) into '{out_location}'.")

if __name__ == "__main__":
    main()