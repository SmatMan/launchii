from types import resolve_bases
import macappsearch as app
import json
import os

with open("index.json", "r") as f: # load index
    index = json.load(f)

searchterm = input('Search: ').lower() # get search term


while True:
    results = app.searchIndex(index, searchterm) # search index for term

    if len(results) == 0: # if no results
        print('No results found.')
        break
    else:
        # print every item from results with a number in front from 1-n, maximum 10
        for i, item in enumerate(results):
            print(str(i+1) + '. ' + item)
        # ask user to select result and get index
        option = int(input('Select result: '))
        # get result from index
        result = results[list(results.keys())[option-1]]
        
        # ask user if they want to open the app, if yes, open app using os.system("open")
        shouldOpen = input(f"Type y to open {list(results.keys())[option-1]}, otherwise, start a new search by searching something else.: ")
        
        if shouldOpen == 'y':
            os.system("open " + result)
            break
        else:
            searchterm = shouldOpen