import json

from pathlib import Path


class ConfigHelper:
    def __init__(self, file_path: str = "./data/config/main.json", initial_data={}):
        self.path = Path(file_path)
        if not self.path.exists():
            with self.path.open('w') as f:
                json.dump(initial_data, f)
                self.data = initial_data
        else:
            with self.path.open() as f:
                self.data = json.load(f)

    def read(self) -> object:
        return self.data

    def write(self, data):
        self.data = data
        with self.path.open('w') as f:
            json.dump(data, f)