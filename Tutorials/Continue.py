nums = [2, 5, 12, 33, 17]

print("Here are the number that are still available: ")

for num in nums:
    if num == 33:
        print(f'Found ==> {num} <==')
        continue
    print(num)
