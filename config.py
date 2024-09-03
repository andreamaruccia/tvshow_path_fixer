import yaml
from typing import List, Dict, Any
from show import Show


class Config:
    def __init__(self, path: str):
        self._path = path
        self._shows: List[Show] = []
        self._source: str = ""
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from YAML file and initialize attributes."""
        data = self._read_yaml()
        self._validate_keys(data)
        self._shows = [Show(**item) for item in data.get("shows", [])]
        self._source = data.get("source", "")
        self._garbage_files = [item for item in data.get("garbage_files", [])]

    def _read_yaml(self) -> Dict[str, Any]:
        """Read and parse the YAML file."""
        try:
            with open(self._path, "r") as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self._path}")
        except yaml.YAMLError as exc:
            raise ValueError(f"Error parsing YAML file: {exc}")

    def _validate_keys(self, data: Dict[str, Any]) -> None:
        """Validate the keys in the YAML data."""
        valid_keys = {"shows", "source", "garbage_files"}
        actual_keys = set(data.keys())

        # Check for unsupported keys
        unsupported_keys = actual_keys - valid_keys
        if unsupported_keys:
            raise ValueError(
                f"Unsupported keys found in YAML file: {', '.join(unsupported_keys)}"
            )

        # Check for missing required keys
        missing_keys = valid_keys - actual_keys
        if missing_keys:
            raise ValueError(
                f"Missing required keys in YAML file: {', '.join(missing_keys)}"
            )

    @property
    def shows(self) -> List[Show]:
        """Return the list of Show objects."""
        return self._shows

    @property
    def source(self) -> str:
        """Return the source string."""
        return self._source

    @property
    def garbage_files(self) -> List[str]:
        """Return the garbage files."""
        return self._garbage_files
