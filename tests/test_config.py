import pytest
import yaml
from pathlib import Path
from config import Config
from show import Show


# Test Fixtures
@pytest.fixture
def valid_config_path(tmp_path):
    config_content = """
    shows:
      - name: "theleftovers"
        dest_path: "/mnt/h/Video/Serie/The Leftovers"
      - name: "barry"
        dest_path: "/mnt/h/Video/Serie/Barry"
    source: "/mnt/h/Video/Source"
    garbage_files:
        - "abc.txt"
    """
    path = tmp_path / "valid_config.yaml"
    path.write_text(config_content)
    return path


@pytest.fixture
def invalid_config_path(tmp_path):
    config_content = """
    shows:
      - name: "theleftovers"
        dest_path: "/mnt/h/Video/Serie/The Leftovers"
      - name: "barry"
        dest_path: "/mnt/h/Video/Serie/Barry"
    source: "/mnt/h/Video/Source"
    garbage_files:
        - "abc.txt"
    invalid_key: "value"
    """
    path = tmp_path / "invalid_config.yaml"
    path.write_text(config_content)
    return path


@pytest.fixture
def invalid_config_missing_attribute_path(tmp_path):
    config_content = """
    shows:
      - name: "theleftovers"
        dest_path: "/mnt/h/Video/Serie/The Leftovers"
      - name: "barry"
        dest_path: "/mnt/h/Video/Serie/Barry"
    garbage_files:
        - "abc.txt"
    """
    path = tmp_path / "invalid_config_missing_attribute.yaml"
    path.write_text(config_content)
    return path


@pytest.fixture
def missing_config_path(tmp_path):
    return tmp_path / "missing_config.yaml"


# Tests
def test_valid_config(valid_config_path):
    config = Config(valid_config_path)
    assert len(config.shows) == 2
    assert config.shows[0].name == "theleftovers"
    assert config.shows[1].dest_path == "/mnt/h/Video/Serie/Barry"
    assert config.source == "/mnt/h/Video/Source"
    assert config.garbage_files == ["abc.txt"]


def test_invalid_yaml(invalid_config_path):
    with pytest.raises(ValueError, match=f"Unsupported keys found in YAML file"):
        Config(invalid_config_path)


def test_invalid_yaml_missing_attribute(invalid_config_missing_attribute_path):
    with pytest.raises(ValueError, match=f"Missing required keys in YAML file"):
        Config(invalid_config_missing_attribute_path)


def test_file_not_found(missing_config_path):
    with pytest.raises(
        FileNotFoundError, match=f"Configuration file not found: {missing_config_path}"
    ):
        Config(missing_config_path)
