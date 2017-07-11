
'''
str(100)
int('100')
float('100)

'''


s = 'hello X42 I\'m a Y-32.35 string Z30'
xy = ("X", "Y", "Z")
num_char = (".", "+", "-")

l = []
out_array=[]

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
    out_array=[]
    out_number = ''
    total=0
    j = 0
    while j < len(input_str)-2:
        for ele in input_str:
            if ele.isdigit() or ele == '-' or ele == '.':
                out_number += ele
                if input_str[j+1].isdigit() != True and input_str[j+1] != '.' :
                    out_array.append(float(out_number))
                    total  += float(out_number)
                    out_number = ''
            j += 1
    return out_array

#Call function
#print("The grand total from the string is: %.2f" % extract_nbr(s))
extracted_array = extract_nbr(s)
total = sum(extracted_array)
print('Input string was: %s' % s)
print('Extracted array is: ')
print(extracted_array)
print('Sum Grand toal is: %f' % total)