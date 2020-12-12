import csv

# fw = open('sample.txt', 'w')
# fw.write('Writing into a text file\n')
# fw.write('2nd line\n')
#
# # Must close open files
# fw.close()
#
# fr = open('sample.txt', 'r')
# text = fr.read()
# print(text)
# fr.close()

# Context manager
with open('sample.txt', 'r') as myTextFile:
    text = myTextFile.read()
    print(text)

# Context manager: copy binary files
with open('sample.jpg', 'rb') as rf:
    with open('sample2.jpg', 'wb') as wf:
        chunk_size = 4096
        rf_chunk = rf.read(chunk_size)
        while len(rf_chunk) >0:
            wf.write(rf_chunk)
            rf_chunk = rf.read(chunk_size)
