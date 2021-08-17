import json


class BaseSearch:

    index: dict[str, str] = {}

    def __init__(self):
        with open("index.json", "r") as f:  # load index
            self.index = json.load(f)

    def search(self, search_term) -> dict:
        results = {}
        for i in self.index:  # iterate over index
            if search_term in self.index[i].lower():  # if search term is in index
                # append i to results as key and index[i] as value
                results[i] = self.index[i]
        return results

    def get_path(self, term) -> str:
        path = self.index[term]
        return path
