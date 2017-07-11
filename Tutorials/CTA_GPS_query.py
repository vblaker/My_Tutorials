from urllib.request import urlopen
from xml.etree.ElementTree import parse
import webbrowser

u = urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')

data = u.read()
fptr = open('rt22.xml', 'wb')
fptr.write(data)
fptr.close()

doc = parse('rt22.xml')

for bus in doc.findall('bus'):
    bus_id = int(bus.findtext('id'))
    busdir = bus.findtext('pd')
    lat = float(bus.findtext('lat'))
    lon = float(bus.findtext('lon'))
    direction = bus.findtext('d')
    print('Bus ID %d is running %s Latitude: %f Longitude: %f' % (bus_id, busdir, lat, lon))
    print('Bus ID {} is running {} Latitude: {} Longitude: '.format(bus_id, busdir, lat, lon))
#    webbrowser.open('http://maps.googleapis.com/maps/api/staticmap?size=500x500&sensor=false&markers=|%f,%f' % (lat, lon))