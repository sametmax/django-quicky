from .names import names as default_names
import random

class NameGenerator(object):
    def __init__(self, names=default_names):
        self._names = {i : name.strip() for i, name in enumerate(names)}
        self._total_names = len(self._names)
        self._used_indices = set()
    def __call__(self):
        index = random.randrange(self._total_names)
        name = self._names[index]
        if index not in self._used_indices:
            self._used_indices.add(index)
            return name
    def __iter__(self):
        while True:
            yield self()
