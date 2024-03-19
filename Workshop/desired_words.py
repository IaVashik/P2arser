class DesiredWords:
    def __init__(self, words = set) -> None:
        self.words = words
        
    def update(self, new_words: list[str]):
        self.words = new_words
        
    def __getitem__(self, idx):
        return self.words[idx]