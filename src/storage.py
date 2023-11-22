import json


class Storage:
    """Save and read dictionaries from a file"""

    def __init__(self, filename) -> None:
        self._filename = filename
        self._data = None

    def _read(self) -> dict:
        """Return data from file or empty dict if file is not found"""
        if self._data is None:
            try:
                with open(self._filename, "r") as file:
                    file_content = file.read()
                self._data = json.loads(file_content)
            except FileNotFoundError:
                self._data = dict()
        return self._data

    def _write(self) -> None:
        """Write data to file, will overwrite existing file"""
        json_data = json.dumps(self._data, indent=2)
        with open(self._filename, "w") as file:
            file.write(json_data)

    def read_object(self, key) -> dict:
        """Return dict at key or None if key is not found"""
        data = self._read()
        return data.get(key, None)

    def save_object(self, key, data: dict) -> None:
        """Save dict at the specified key"""
        self._data = self._read()
        self._data[key] = data
        self._write()
