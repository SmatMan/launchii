import appsearch as app
import json

searchterm = input('Search: ').lower()

index = {}

with open("index.json", "r") as f:
    index = json.load(f)

for i in index:
    if searchterm in str(i):
        print(i)