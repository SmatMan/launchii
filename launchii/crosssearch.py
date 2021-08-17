class BaseSearch:
    def searchIndex(self, index, searchterm) -> dict:
        results = {}
        for i in index:  # iterate over index
            if searchterm in index[i].lower():  # if search term is in index
                # append i to results as key and index[i] as value
                results[i] = index[i]
        return results

    def getPath(self, index, term) -> str:
        path = index[term]
        return path
