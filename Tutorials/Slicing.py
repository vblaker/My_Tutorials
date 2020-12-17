my_list = []
my_list = [*range(0, 20, 1)]
print(my_list)

first, *mid, last = my_list
print(f'{first} => {mid} <= {last}')

# Start from 2, to the end every second element
print(my_list[2:-1:2])

# Reverse order listing from the end to index 2
print(my_list[-1:2:-1])

# Reverse order
print(my_list[::-1])
