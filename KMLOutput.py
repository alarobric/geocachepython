import geopy

#icons borrowed from: http://www.thepropers.com/geocaching/60SeriesCustomSymbols.htm

def initKML(f):
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n' +
            '<kml xmlns="http://www.opengis.net/kml/2.2">\n' +
            '<Document>\n' +
            '  <Style id="Traditional">\n' +
            '    <IconStyle>\n' +
            '      <Icon>\n' +
            '        <href>http://alarobric.homeip.net/geocacheicons/000.bmp</href>\n' +
            '      </Icon>\n' +
            '    </IconStyle>\n' +
            '  </Style>\n' +
            '  <Style id="GreenTrans">\n' +
            '    <LineStyle>\n' +
            '      <width>2</width>\n' +
            '    </LineStyle>\n' +
            '    <PolyStyle>\n' +
            '      <color>7f00ff00</color>\n' +
            '    </PolyStyle>\n' +
            '  </Style>\n')
            
def closeKML(f):
    f.write('</Document>\n' + '</kml>\n')

def createCircle(f, aLatLonCenter, radius, name='cache'):
    latLonCenter = geopy.util.parse_geo(aLatLonCenter)
    vertices = []
    angle = 0.0
    while angle <= 360:
        vertex = geopy.distance.destination(latLonCenter, angle, radius)
        vertices.append(vertex)
        angle = angle + 10

    firstVertex = vertices[0]
    vertices.append(firstVertex)
  
    f.write('<Placemark>\n' +
            '<name>' + name + '</name>\n' +
            '<styleUrl>#GreenTrans</styleUrl>\n' +
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
            '</Placemark>\n' +
            '<Placemark>\n' +
            '<name>' + name + '</name>\n' +
            '<description>' + name + '</description>\n' +
            '<Point>\n' +
            '<extrude>1</extrude>\n' +
            '<altitudeMode>clampToGround</altitudeMode>\n' +
            '<coordinates>\n' + 
            str(latLonCenter[1]) + ',' + str(latLonCenter[0]) + ',' + '0\n' +
            '</coordinates>\n' +
            '</Point>\n' +
            '</Placemark>\n')

f = open('outFile.kml', 'w')
initKML(f)
createCircle(f, '44.142 -76.512', 0.161)
closeKML(f)
f.close()
