import os
import pytest
from folder_cleaner import FolderCleaner


@pytest.fixture
def setup_test_environment(tmp_path):
    # Create a temporary directory structure
    base_dir = tmp_path / "test_dir"
    base_dir.mkdir()

    # Create empty directories
    empty_dir1 = base_dir / "empty_dir1"
    empty_dir1.mkdir()
    empty_dir2 = base_dir / "empty_dir2"
    empty_dir2.mkdir()

    # Create non-empty directory
    non_empty_dir = base_dir / "non_empty_dir"
    non_empty_dir.mkdir()
    (non_empty_dir / "file.txt").write_text("This is a test file.")

    return base_dir


class TestFolderCleaner:
    def test_clean_empty_folders(self, setup_test_environment):
        cleaner = FolderCleaner(setup_test_environment)
        cleaner.clean_empty_folders()

        # Check that empty directories are removed
        assert not (setup_test_environment / "empty_dir1").exists()
        assert not (setup_test_environment / "empty_dir2").exists()

        # Check that non-empty directory still exists
        assert (setup_test_environment / "non_empty_dir").exists()

    def test_non_empty_folders_not_removed(self, setup_test_environment):
        cleaner = FolderCleaner(setup_test_environment)
        cleaner.clean_empty_folders()

        # Check that non-empty directory still exists
        assert (setup_test_environment / "non_empty_dir").exists()
        assert (setup_test_environment / "non_empty_dir" / "file.txt").exists()
