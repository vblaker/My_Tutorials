"""
classmates = {'Tony': ' is cool', 'Emma': ' sits behind', 'Lucy': ' asks too many questions'}
print(classmates)
print(classmates['Emma'])

for k, v in classmates.items():
    print(k + v)

print('The size of classmates is:', len(classmates))

class Person(object):
    def __init__(self, name, profession):
        self.name = name
        self.profession = profession

people = [Person("Nick", "Programmer"), Person("Alice", "Engineer")]
professions = dict([(p.name, p.profession) for p in people])

"""

header_list = ['Time (s)', 'VBUS Voltage (V)', 'VBUS Current (A)', 'VCONN Voltage (V)', 'VCONN Current (A)',
           'CC1 Voltage (V)', 'CC1 Current (A)', 'CC2 Voltage (V)', 'CC2 Current (A)']

row = header_list

header_dict = {}
for i in range(len(row)):
    header_dict[header_list[i]] = row.index(header_list[i])

print(header_dict)

for key, value in header_dict.items():
    print(key)