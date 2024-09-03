import os
import glob
import fnmatch
from pathlib import Path
from typing import List

class FolderCleaner:
    def __init__(self, path: str):
        self._path = path

    def clean_empty_folders(self, dryrun: bool = False) -> None:
        for root, dirs, files in os.walk(self._path, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):  # Check if the directory is empty
                    if dryrun:
                        print(f"Would remove empty folder: {dir_path}")
                    else:
                        os.rmdir(dir_path)
                        print(f"Removed empty folder: {dir_path}")

    def clean_garbage_files(self, dryrun: bool = False, garbage_files: List[str] = []) -> None:
        for file in glob.glob(f"{self._path}/**/*", recursive=True):
            if any(fnmatch.fnmatch(Path(file).name, pattern) for pattern in garbage_files):
                if dryrun:
                    print(f"Would remove garbage file: {file}")
                else:
                    os.remove(file)
                    print(f"Removed garbage file: {file}")
