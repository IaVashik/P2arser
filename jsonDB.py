import json
# haha, junk code

class DatabaseTable:
    def __init__(self, name) -> None:
        self.path = "jsonDb/" + name # ! AUTO-CRETE FOLDER
        self.data = self._load_data(self.path)
    
    def _load_data(self, DB_FILE):
        try:
            with open(DB_FILE, 'r') as file:
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
        return self.data.get(str(key), None)


cache = {}

class JsonDatabase:
    def __init__(self) -> None:
        self.path = "jsonDb/"
    
        
    def load_table(self, name):
        if name in cache:
            return cache[name]
        
        tb = DatabaseTable(name)
        cache[name] = tb
        return tb
    
    
    def create_table(self, name):
        return DatabaseTable(name)