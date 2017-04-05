def array_gen(num_of_elem):
    new_array = []
    for i in range(0, num_of_elem):
        new_array.append(i)
    return new_array

array_size = int(input('Enter size of the array to be generated: '))
print(array_gen(array_size))