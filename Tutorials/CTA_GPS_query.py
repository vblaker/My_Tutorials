from urllib.request import urlopen

u = urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
data = u.read()
fptr = open('rt22.xml', 'wb')
fptr.write(data)
fptr.close()