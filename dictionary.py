# dictionary.py
import json

class Dictionary:
    def __init__(self):
        self._dict = {}

    def add(self, key, value):
        self._dict[key] = value

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def remove(self, key):
        if key in self._dict:
            del self._dict[key]

    def contains(self, key):
        return key in self._dict

    def keys(self):
        return list(self._dict.keys())

    def values(self):
        return list(self._dict.values())

    def items(self):
        return list(self._dict.items())

    def clear(self):
        self._dict.clear()

    def __len__(self):
        return len(self._dict)

    def __str__(self):
        return str(self._dict)

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump(self._dict, f)

    def load(self, filename):
        try:
            with open(filename, 'r') as f:
                self._dict = json.load(f)
        except FileNotFoundError:
            self._dict = {}
