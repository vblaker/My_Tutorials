import csv

fw = open('sample.txt', 'w')
fw.write('Writing into a text file\n')
fw.write('2nd line\n')
fw.close()

fr = open('sample.txt', 'r')
text = fr.read()
print(text)
fr.close()

with open('sample.txt', 'r') as myTextFile:
    text = myTextFile.read()
    print(text)