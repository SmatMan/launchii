from types import resolve_bases
import macappsearch as app
import json

with open("index.json", "r") as f: # load index
    index = json.load(f)

searchterm = input('Search: ').lower() # get search term

results = {}

for i in index: # iterate over index
    if searchterm in index[i].lower(): # if search term is in index
        # append i to results as key and index[i] as value
        results[i] = index[i]

if len(results) == 0: # if no results
    print('No results found.')
else:
    for i in results:
        print(i + ': ' + results[i]) # print results)