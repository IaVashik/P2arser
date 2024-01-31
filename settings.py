import json

class ConfigManager:
    def __init__(self, config_path: str):
        self.config = self._read_config(config_path)

    def _read_config(self, path: str):
        with open(path, 'r') as file:
            return json.load(file)

    def get(self, idx, default_value = None):
            return self.config.get(idx, default_value)
    
    def __getitem__(self, idx):
        return self.get(idx)