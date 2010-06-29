import geopy

def initKML(f):
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n' +
            '<kml xmlns="http://www.opengis.net/kml/2.2">\n' +
            '<Document>\n' +
            '<Style id="examplePolyStyle">\n' +
            '<PolyStyle>\n' +
            '<color>ff0000cc</color>\n' +
            '</PolyStyle>\n' +
            '</Style>\n')
            
def closeKML(f):
    f.write('</Document>\n' + '</kml>\n')

def createCircle(f, aLatLonCenter, diameter):
    latLonCenter = geopy.util.parse_geo(aLatLonCenter)
    print latLonCenter
    vertices = []
    angle = 0.0
    radius = diameter / 2.0
    while angle <= 360:
        vertex = geopy.distance.destination(latLonCenter, angle, radius)
        vertices.append(vertex)
        angle = angle + 10

    firstVertex = vertices[0]
    vertices.append(firstVertex)
  
    f.write('<Placemark>\n' +
            '<name>cache</name>\n' +
            '<styleUrl>#examplePolyStyle</styleUrl>\n' +
            '<Polygon>\n' +
            '<extrude>1</extrude>\n' +
            '<altitudeMode>clampToGround</altitudeMode>\n' +
            '<outerBoundaryIs>\n' +
            '<LinearRing>\n' +
            '<coordinates>')
    for vertex in vertices:
        f.write(str(vertex[1]) + ',' + str(vertex[0]) + ',' + '0\n')
    f.write('</coordinates>\n' +
            '</LinearRing>\n' +
            '</outerBoundaryIs>\n' +
            '</Polygon>\n' +
            '</Placemark>\n')

f = open('outFile.kml', 'w')
initKML(f)
createCircle(f, '44.142 -76.512', 0.322)
closeKML(f)
f.close()
