greetings = 'Hello'
name = 'Vadim'
message = f'{greetings}, {name.upper()}. Welcome!\n'
print(message)

# String formatting
person = {'name': 'Jenn', 'age': 23}
print('My name is {0[name]} and my age is {0[age]}'.format(person))


class Person:
    def __init__(self, first_name, age):
        self.first_name = first_name
        self.age = age


p1 = Person('Jack', 33)
print('My name is {0.first_name} and my age is {0.age}'.format(p1))

sentence = 'My name is {name} and I am {age} years old'.format(**person)
print(sentence)

# Commas for large numbers
print('1 MB is equal to {:,} bytes'.format((1024*2)))


# parsing string
s = 'hello X42 I\'m a Y-32.35 string Z30'
xy = ("X", "Y", "Z")
num_char = (".", "+", "-")

l = []
out_array = []

tokens = s.split()

for token in tokens:
    if token.startswith(xy):
        num = ""
        for char in token:
            # print(char)
            if char.isdigit() or (char in num_char):
                num += char

        try:
            l.append(float(num))
        except ValueError:
            pass
print(l)


def extract_nbr(input_str):
    if input_str is None or input_str == '':
        return 0

    input_str += 'VB'
    out_array = []
    out_number = ''
    total = 0
    j = 0
    while j < len(input_str)-2:
        for ele in input_str:
            if ele.isdigit() or ele == '-' or ele == '.':
                out_number += ele
                if not input_str[j+1].isdigit() and input_str[j+1] != '.':
                    out_array.append(float(out_number))
                    total += float(out_number)
                    out_number = ''
            j += 1
    return out_array


# Call function
# print("The grand total from the string is: %.2f" % extract_nbr(s))

extracted_array = extract_nbr(s)
total = sum(extracted_array)
print('Input string was: %s' % s)
print('Extracted array is: ')
print(extracted_array)
print('Sum Grand total is: %.2f' % total)
