import sys
import urllib.request
from xml.etree.ElementTree import parse
import webbrowser
import numpy
office_lat = 41.980262
office_lon = -87.668452


class Bus:
    id = None
    route = None
    direction = None
    latitude = None
    longitude = None

    def __init__(self, id, rt, d, lat, lon):
        self.id  = id
        self.route = rt
        self.direction = d
        self.latitude = lat
        self.longitude = lon


def openMap(buslist):
    htmlcode = """
<!DOCTYPE html>
<html>
  <head>
    <title>Simple Map</title>
    <meta name="viewport" content="initial-scale=1.0">
    <meta charset="utf-8">
    <style>
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
      #map {
        height: 100%;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>

    <script>
        // The following example creates complex markers to indicate buses near
        // Sydney, NSW, Australia. Note that the anchor is set to (0,32) to correspond
        // to the base of the flagpole.
"""
    print(buslist.values())
    avglongitude = 0
    for bus in buslist.items():
        avglongitude += bus[1].longitude
    avglongitude /= len(buslist)

    htmlcode += "        function initMap() {\n"
    htmlcode += "          var map = new google.maps.Map(document.getElementById('map'), {\n"
    htmlcode += "          zoom: 13,\n"
    htmlcode += "          center: {lat: " + "{:.9f}".format(office_lat) + ", lng: " + "{:.9f}".format(avglongitude) + "}\n"
    htmlcode += "        });\n"
    htmlcode += "        setMarkers(map);\n"
    htmlcode += "        }"

    htmlcode += """
        // Data for the markers consisting of a name, a LatLng and a zIndex for the
        // order in which these markers should display on top of each other.
        """

    htmlcode += "var buses = [\n"
    last = len(buslist) - 1
    htmlcode += "         ['office', " + "{:.9f}".format(office_lat) + \
                ", " + "{:.9f}".format(office_lon) + ", 1],\n"

    for i, myBus in enumerate(buslist.items()):
        htmlcode += "         ['" + myBus[0] + "', " + "{:.9f}".format(myBus[1].latitude) + \
                                                ", " + "{:.9f}".format(myBus[1].longitude) + ", " + str(i+2) + "]"
        if i != last:
            htmlcode += ",\n"
        else:
            htmlcode += "\n    ];\n"

    htmlcode += """

        function setMarkers(map) {
          // Adds markers to the map.

          // Marker sizes are expressed as a Size of X,Y where the origin of the image
          // (0,0) is located in the top left of the image.

          // Origins, anchor positions and coordinates of the marker increase in the X
          // direction to the right and in the Y direction down.

          var busImage = {
              url: 'http://pngimg.com/upload/small/bus_PNG8602.png',
              size: new google.maps.Size(256, 256),
              scaledSize: new google.maps.Size(50, 50),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(25, 25)
          };
          var officeImage = {
              url: 'http://images.clipartpanda.com/church-building-clipart-black-and-white-building-white-hi.png',
              size: new google.maps.Size(348, 599),
              scaledSize: new google.maps.Size(35, 60),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 30)
          };
          // Shapes define the clickable region of the icon. The type defines an HTML
          // <area> element 'poly' which traces out a polygon as a series of X,Y points.
          // The final coordinate closes the poly by connecting to the first coordinate.
          var shape = {
            coords: [1, 1, 1, 50, 50, 50, 50, 1],
            type: 'poly'
          };

          for (var i = 0; i < buses.length; i++) {
            var bus = buses[i];
            if (i == 0) {
              myImage = officeImage
            } else {
              myImage = busImage
            }
            var marker = new google.maps.Marker({
              position: {lat: bus[1], lng: bus[2]},
              map: map,
              icon: myImage,
              shape: shape,
              title: bus[0],
              zIndex: bus[3]
            });
          }
        }
    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDMMJp-u8Fyt4iFdJipiJyf_xh_5g4etrY&callback=initMap"
    async defer></script>
  </body>
</html>
    """
    maphtml = open("map.html", "w")
    maphtml.write(htmlcode)
    maphtml.close()


# get_rt22.py
#
# From the notes.  Access the CTA website and fetch information
# about route 22 buses.  Write to a file 'rt22.xml'.
# For Python 3, change import urllib to urllib.request

u = urllib.request.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
data = u.read()
f = open('rt22.xml', 'wb')
f.write(data)
f.close()
print('Wrote rt22.xml')

doc = parse("rt22.xml")
allbuses = {}
northbound = {}

for bus in doc.findall('bus'):
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

