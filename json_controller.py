import json

class JsonManager:
    def __init__(self, path) -> None:
        self.path = path
        self.data = self._load_data(path)
    
    def _load_data(self, path):
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def update(self):
        with open(self.path, 'w') as file:
            json.dump(self.data, file)
            
    def add(self, key, value):
        self.data[str(key)] = value
        self.update()
        
    def get(self, key):
        return self.data.get(key, None)
    
    def __getitem__(self, idx):
        return self.get(idx)
    
    

class ConfigManager(JsonManager):
    pass


class UserData(object):
    def __new__(cls) -> object:
        if not hasattr(cls, 'instance'):
            cls.instance = super(UserData, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        self.json = JsonManager("users_info")
        self.data = self.json.data
        
    def save_change(self):
        self.json.update()
        
    def get_unique_words(self):
        all_words = set()
        for value in self.data.values():
            all_words.update(value)
        
        return all_words
    
    def get(self, key):
        return self.data.get(str(key), None)
    
    def __getitem__(self, idx):
        return self.get(idx)