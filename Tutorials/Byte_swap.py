import sys

my_string = '01234567'
debug = 1
byte_swapped_string = ''

try:
    if len(my_string) == 0 or len(my_string) % 4 != 0:
        raise ValueError
    errorFlag = False

    if debug == 1:

        # Split string into a list of bytes
        str_list = [my_string[i:i + 2] for i in range(0, len(my_string), 2)]
        print('The original list is {}'.format(str_list))

        # Process two elements at at time and swap them
        byte_swapped_string_list = []
        for i in range(0, int(len(str_list)), 2):
            byte_swapped_string_list.append(str_list[i + 1])
            byte_swapped_string_list.append(str_list[i])
        print(byte_swapped_string_list)
        byte_swapped_string = ''.join(byte_swapped_string_list)

    else:
        # An alternative method working with just strings
        for i in range(0, int(len(my_string)), 4):
            byte_swapped_string += my_string[i + 2:i + 4]
            byte_swapped_string += my_string[i:i + 2]

    print(byte_swapped_string)

except ValueError:
    error = sys.exc_info()[1]
    print(error)
    if len(my_string) == 0:
        print('You entered a 0 but you can\'t have an empty string!')
    else:
        print("String length {} in not divisible by 4!".format(len(my_string)))
    errorFlag = True

if not errorFlag:
    print("All is good!")