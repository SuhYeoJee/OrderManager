import json
import os

class JsonManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}
        self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        else: # 파일 없을때 동작
            self._save()

    def _save(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def auto_save(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self._save()
            return result
        return wrapper

