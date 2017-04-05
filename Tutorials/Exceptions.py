import sys

while True:
    try:
        number = int(input("What's you favorite number?:\n"))
        print(18/number)
        errorFlag = False
        break
    except ValueError:
        error = sys.exc_info()[0]
        print(error)
        print("You didn't enter a number!")
        errorFlag = True
    if not errorFlag :
        print("All is good!")
