# Short if/else
condition = True
x = 1 if condition else 0
print(x)

# large number formatting
num1 = 10_00_000_000
num2 = 100_000_000
total = num1 + num2
print(f"{total:,}")

# File opening using context manager
with open("text.txt", "r") as f:
    file_contents = f.read()
words = file_contents.split(" ")
word_count = len(words)
print(word_count)

# Counter using enumerate
names = ["Corey", "Chris", "Dave", "Travis"]
for index, name in enumerate(names, start=1):
    print(index, name)

# Zip lists
names = ["Peter parker", "Clark Kent", "Wade Wilson", "Bruce Wayne"]
heroes = ["Spiderman", "Superman", "Deadpool", "Batman"]
universes = ["Marvel", "DC", "Marvel", "DC"]

for name, hero, universe in zip(names, heroes, universes):
    print(f"{name} is actually {hero} from {universe}")

# Unpacking
a, _ = (1, 2)
a, b, *c = (1, 2, 3, 4, 5)
print(a, b, c)

# Set class attribute
class Person:
    pass


person = Person()
first_key = "first"
first_val = "Vadim"
setattr = (person, first_key, first_val)

first = getattr(person, first_key)

print(person.first)

person_info = {"first": "Vadim", "last": "Blaker"}
for key, value in person_info.items:
    setattr(person, key, value)

print(person.first, person.last)