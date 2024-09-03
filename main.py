import shutil
from colorama import init, Fore, Style

from config import Config
from video_related_file_provider import VideoRelatedFileProvider
from folder_cleaner import FolderCleaner
from show_manager import ShowManager

if __name__ == "__main__":
    init()  # Initialize colorama

    config = Config(path="config.yml")
    show_manager = ShowManager(shows=config.shows)
    files = VideoRelatedFileProvider().get(path=config.source)
    dry_run = True

    for file in files:
        destination = show_manager.get_desired_destination(file)
        if destination == "":
            print(
                Fore.LIGHTBLACK_EX
                + f"Could not find a destination for {file}"
                + Style.RESET_ALL
            )
            continue
        if dry_run:
            print(
                Fore.LIGHTYELLOW_EX
                + f"Would move {file} to {destination}"
                + Style.RESET_ALL
            )
        else:
            shutil.move(file, show_manager.get_desired_destination(file))
            print(Fore.GREEN + f"Moved {file} to {destination}" + Style.RESET_ALL)

    cleaner = FolderCleaner(config.source)
    cleaner.clean_garbage_files(dryrun=dry_run, garbage_files=config.garbage_files)
    cleaner.clean_empty_folders(dryrun=dry_run)
