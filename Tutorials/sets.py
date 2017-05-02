groceries_set = {'cereal', 'milk', 'crunch', 'beer', 'tape', 'lotion', 'beer'}

print(groceries_set)

if 'milk' in groceries_set:
    print('Milk is already there')
else:
    print("Oh yeah, you need milk")

groceries_set.add('one last thing')
print(groceries_set)


#groceries is a list
groceries_list = ['cereal', 'milk', 'crunch', 'beer', 'tape', 'lotion', 'beer']
if 'milk' in groceries_set:
    print('Milk is already there')
else:
    print("Oh yeah, you need milk")

groceries_list.append('one last thing...')
print(groceries_list)