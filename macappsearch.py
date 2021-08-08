import os
from collections import OrderedDict
import getpass
import json
from glob import glob

path=["/Applications", "/System/Applications", f"/Users/{getpass.getuser()}/Applications"]
rawFileList = {}

def createIndex(path=path):
    # For every filepath in path, find all the folders (no subdirectories) ending in .app and add them to the dict rawFileList
    for i in path:
        files = glob(f"{i}/*/")
        for file in files:
            if ".app" in file:
            # Append every filepath along with the os.path.basename(path) to the dict rawFileList reverse. make sure the trailing slash and ".app" is removed before os.path.basename(path) is appended
                rawFileList[os.path.basename(file[:-5])] = file[:-1]

    # Create an ordered dict with the key being the name of the app and the value being the filepath
    index = OrderedDict()
    for key, value in rawFileList.items():
        index[key] = value
    return index


def saveIndex(output="index.json"):
    index = createIndex()
    with open(output, "w") as f:
        f.write(json.dumps(index, indent=4))

def searchIndex(index, searchterm):
    results = {}
    for i in index: # iterate over index
        if searchterm in index[i].lower(): # if search term is in index
            # append i to results as key and index[i] as value
            results[i] = index[i]
    return results

def getPath(index, term):
    path = index[term]
    return path

def getIcon(path):
    for i in glob(f"{path}/Contents/Resources/*.icns"):
        icon = i
    return icon