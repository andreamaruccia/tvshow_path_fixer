import os
import re
from typing import List
from show import Show


class ShowManager:
    def __init__(self, shows: List[Show]):
        self.shows = shows

    def get_desired_destination(self, path: str) -> str:
        """
        Determine the destination path for a given file based on its name and the list of shows.

        Args:
            path (str): The file path to determine the destination for.

        Returns:
            str: The destination path if a match is found; otherwise, an empty string.
        """
        normalized_path = re.sub(r"[ .-]", "", path).lower()

        results = []
        for show in self.shows:
            if show.name in normalized_path:
                file_name = os.path.basename(path)
                # Replace 'sXXeYY' with 'XXxYY' in the file name
                file_name = re.sub(
                    r"s(\d+)e(\d+)", r"\1x\2", file_name, flags=re.IGNORECASE
                )
                results.append(os.path.join(show.dest_path, file_name))

        if len(results) == 0:
            return ""
        if len(results) > 1:
            return ""
        return results[0]
