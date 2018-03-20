import string


def reverse_a_string_slowly(a_string):
    new_string = ''
    index = len(a_string)
    while index:
        index -= 1                     # index = index - 1
        new_string += a_string[index]  # new_string = new_string + character
    return new_string


def reversed_string(a_string):
    return a_string[::-1]


print(reversed_string('boj'))
revsrt = reversed_string('boJ')
revsrt = string.ascii_uppercase

print('Upper case is: ' + revsrt.upper())
print('Lower case is: ' + revsrt.lower())
print('Mixed case is: ' + revsrt.swapcase())
