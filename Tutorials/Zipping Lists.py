items = ['November 30, 2016', 'Bread Gloves', 8.51]
[date, name, price] = items
print(name)


def drop_first_last(grades):
    first, *middle, last = grades
    average = sum(middle) / len(middle)
    print(average)


drop_first_last([65, 76, 98, 54, 21])

first = ['One', 'Two', 'Three']
last = ['Ten', 'Twenty', 'Thirty']

names = zip(first, last)
print(names)

for a, b in names:
    print(a, b)
