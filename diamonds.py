import sys
import urllib.request
from xml.etree.ElementTree import parse
import webbrowser
from bs4 import BeautifulSoup


import numpy
office_lat = 41.980262
office_lon = -87.668452


u = urllib.request.urlopen('http://www.bluenile.com/build-your-own-ring/diamonds?track=NavEngStartWithDia')
data = u.read()
f = open('diamonds.xml', 'wb')
f.write(data)
f.close()
print('Wrote diamonds.xml')

# doc = parse("diamonds.xml")
soup = BeautifulSoup(data, 'html.parser')
allbuses = {}
northbound = {}

for bus in soup.findall('bus'):
    lat = float(bus.findtext("lat"))
    busid = bus.findtext('id')
    allbuses[busid] = Bus(busid,
                          bus.findtext("rt"),
                          bus.findtext("d"),
                          float(bus.findtext("lat")),
                          float(bus.findtext("lon"))
                          )
    if allbuses[busid].latitude >= office_lat and allbuses[busid].direction.startswith("North"):
        northbound[busid] = allbuses[busid]
        print(northbound[busid].id, northbound[busid].direction, northbound[busid].latitude)

openMap(northbound)
webbrowser.open("map.html")

