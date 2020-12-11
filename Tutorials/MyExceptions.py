import sys

while True:
    try:
        number = int(input("What's you favorite number?:\n"))
        if number == 0:
            raise ValueError
        print(18/number)
        errorFlag = False
        break

    except ValueError:
        error = sys.exc_info()[1]
        print(error)
        if number == 0:
            print('You entered a 0 but you can\'t divide by it!')
        else:
            print("You didn't enter a number!")
        errorFlag = True
    if not errorFlag:
        print("All is good!")
