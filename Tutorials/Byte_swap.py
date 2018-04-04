import sys


my_string = '12345678'

try:
    if len(my_string) == 0 or len(my_string) % 4 != 0:
        raise ValueError
    errorFlag = False

    # Split string into a list of bytes
    str_list = [my_string[i:i + 2] for i in range(0, len(my_string), 2)]
    print('The original list is {}'.format(str_list))

    byte_swapped_string_list = []
    for i in range(0, int(len(str_list)), 2):
        byte_swapped_string_list.append(str_list[i + 1])
        byte_swapped_string_list.append(str_list[i])
    print(byte_swapped_string_list)

    byte_swapped_string = ''.join(byte_swapped_string_list)
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