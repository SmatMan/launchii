import json
import os
from launchii.colours import *

def main(searcher=None):
    with open("index.json", "r") as f: # load index
        index = json.load(f)

    searchterm = input(cyan('Search: ')).lower() # get search term


    while True:
        results = searcher.searchIndex(index, searchterm) # search index for term

        if len(results) == 0: # if no results
            print('No results found.')
            break
        else:
            # print every item from results with a number in front from 1-n, maximum 10
            for i, item in enumerate(results):
                print(str(i+1) + '. ' + yellow(str(item)) + '\n')
            # ask user to select result and get index
            option = input(cyan('Select result or start new search: '))
            # check if option is a number
            try:
                option = int(option)
                result = results[list(results.keys())[option-1]]
                # ask user if they want to open the app, if yes, open app using os.system("open")
                shouldOpen = input(f"Type {yellow('y')} to open {green(str(list(results.keys())[option-1]))}, or {yellow('n')} to quit: ")
                
                if shouldOpen == 'y':
                    os.system("open " + result)
                    break
                else:
                    break
            except ValueError:
                searchterm = option

        
        
