from pathlib import Path


class VideoRelatedFileProvider:
    def get(self, path: str) -> list[str]:

        file_types = ("mp4", "mkv", "avi", "mov", "mpeg", "mpg", "divx", "xvid", "srt")

        path_obj = Path(path)
        files = [
            str(file) for file in path_obj.rglob("*") if file.suffix[1:] in file_types
        ]

        return files
