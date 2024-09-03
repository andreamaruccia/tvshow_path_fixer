import pytest
import tempfile
import shutil
from pathlib import Path
from video_related_file_provider import VideoRelatedFileProvider


@pytest.fixture
def temp_dir():
    """Fixture to create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


class TestFileManager:
    @pytest.fixture
    def file_provider(self):
        """Fixture to create an instance of FileManager."""
        return VideoRelatedFileProvider()

    def test_find_video_files(self, temp_dir, file_provider):
        """Test that the FileManager finds video files correctly."""
        # Create test files
        valid_files = ["test1.mp4", "test2.mkv", "test3.avi", "test4.txt"]
        for file_name in valid_files:
            (temp_dir / file_name).touch()

        # Run the method and assert results
        video_files = file_provider.get(str(temp_dir))
        expected_files = {
            str(temp_dir / file_name)
            for file_name in valid_files
            if file_name.endswith((".mp4", ".mkv", ".avi"))
        }
        assert set(video_files) == expected_files

    def test_empty_directory(self, file_provider):
        """Test that the FileManager handles an empty directory gracefully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            video_files = file_provider.get(temp_dir)
            assert video_files == []

    def test_no_matching_files(self, temp_dir, file_provider):
        """Test that the FileManager returns an empty list if no files match the types."""
        (temp_dir / "document.txt").touch()  # Create a non-matching file

        video_files = file_provider.get(str(temp_dir))
        assert video_files == []

    def test_invalid_path(self, file_provider):
        """Test that the FileManager handles invalid paths."""
        invalid_path = str(Path(tempfile.mkdtemp()) / "invalid_dir")
        # Ensure the path does not exist
        if Path(invalid_path).exists():
            shutil.rmtree(invalid_path)

        video_files = file_provider.get(invalid_path)
        assert video_files == []
