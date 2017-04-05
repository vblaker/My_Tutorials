magicNumber = 26

# Just a comment


''' MULTILINE COMMENT
for n in range(101): # this too is a comment
    if n is magicNumber:
        print()
'''
'''
for n in range(100): # this too is a comment
    if n is magicNumber:
        print(n, " is the magic number")
        break
    else:
        print(n)
 '''

numCount = 0
for n in range(100):  # this too is a comment
    if n % 4 == 0:
        print(n, " is a number divisible by 4")
        numCount += 1

print("NumCount is: %d" % numCount)
