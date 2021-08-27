from launchii.api import Launchii
from launchii.colours import *


class Cli:
    def __init__(self, launchii: Launchii) -> None:
        self.launchii = launchii

    def start(self):

        searchterm = input(cyan("Search: ")).lower()  # get search term

        while True:
            results = self.launchii.search(searchterm)  # search index for term

            if len(results) == 0:  # if no results
                print("No results found.")
                break
            else:
                # print every item from results with a number in front from 1-n, maximum 10
                for i, result in enumerate(results):
                    print(str(i + 1) + ". " + yellow(str(result.describe())) + "\n")
                # ask user to select result and get index
                option = int(input(cyan("Select result or start new search: "))) - 1
                # check if option is a number
                try:
                    result = results[option]
                    # ask user if they want to open the app, if yes, open app using os.system("open")
                    shouldOpen = input(
                        f"Type {yellow('y')} to open {green(result.describe())}, or {yellow('n')} to quit: "
                    )

                    if shouldOpen == "y":
                        result.execute()
                        break
                    else:
                        break
                except ValueError:
                    searchterm = option
