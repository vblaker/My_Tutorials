'''
classmates = {'Tony': ' cool', 'Emma': ' sits behind', 'Lucy': ' asks too many questions'}

print(classmates)
print(classmates['Emma'])

for k, v in classmates.items():
    print(k + v)

'''


# A Python dictionary is a set of key-value pairs
my_dict = {'a_key': 'a_value', 'another_key': 'another_value'}
# which allows access to the values via the keys (lookup)
my_dict['another_key']  # 'another_value'
# This data structure is also known as a `map` or `hash-map`

class intDict(object):
    """A dictionary with integer keys"""

    def __init__(self, numBuckets):
        """Create an empty dictionary"""
        self.buckets = []
        self.numBuckets = numBuckets
        for i in range(numBuckets):
            self.buckets.append([])

    def addEntry(self, dictKey, dictVal):
        """Assumes dictKey an int. Adds an entry."""
        hashBucket = self.buckets[dictKey % self.numBuckets]
        for i in range(len(hashBucket)):
            if hashBucket[i][0] == dictKey:
                hashBucket[i] = (dictKey, dictVal)
                return
        hashBucket.append((dictKey, dictVal))

    def getValue(self, dictKey):
        """Assumes dictKey an int. Returns entry associated
           with the key dictKey"""
        hashBucket = self.buckets[dictKey % self.numBuckets]
        for e in hashBucket:
            if e[0] == dictKey:
                return e[1]
        return None

    def __str__(self):
        result = '{'
        for b in self.buckets:
            for e in b:
                result = result + str(e[0]) + ':' + str(e[1]) + ','
        return result[:-1] + '}' #result[:-1] omits the last comma