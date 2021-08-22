from launchii.colours import *


def main(searcher, runner):

    searchterm = input(cyan("Search: ")).lower()  # get search term

    while True:
        results = searcher.search(searchterm)  # search index for term

        if len(results) == 0:  # if no results
            print("No results found.")
            break
        else:
            # print every item from results with a number in front from 1-n, maximum 10
            for i, result in enumerate(results):
                print(str(i + 1) + ". " + yellow(str(result.name)) + "\n")
            # ask user to select result and get index
            option = int(input(cyan("Select result or start new search: "))) - 1
            # check if option is a number
            try:
                result = results[option]
                # ask user if they want to open the app, if yes, open app using os.system("open")
                shouldOpen = input(
                    f"Type {yellow('y')} to open {green(result.name)}, or {yellow('n')} to quit: "
                )

                if shouldOpen == "y":
                    runner.do(result)
                    break
                else:
                    break
            except ValueError:
                searchterm = option
