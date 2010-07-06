import codecs

def writeFile(filename, num, line):
    out = codecs.open(filename + '.arc', 'w', 'utf-8')

    if line[7:9] == "Mu":
        line = line.split('>')[5].split('<')[0]
    else:
        print line[:15], line[7:9]
        line = line.split('>')[4].split('<')[0]
    line = line.split(' ')
    for point in line:
        try:
            point = point.split(',')
            out.write('%s\t%s\n' %(point[0], point[1]))
        except IndexError:
            print line
            print point
        
    
    #out.write('<?xml version="1.0" encoding="utf-8" ?>\n')
    #out.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    #out.write('<Document><Folder><name>' + filename + ' num ' + num + '</name>\n')
    #out.write('<Placemark>\n')
    #out.write('   <Style><LineStyle><color>ff0000ff</color></LineStyle>  <PolyStyle><fill>0</fill></PolyStyle></Style>\n')
    #out.write(line)
    #out.write('</Placemark\n')
    #out.write('</Folder></Document></kml>')
    out.close()


f = codecs.open("RD_2010.kml", 'r', 'utf-8')

line = f.readline()
while line.find('<\Folder>') == -1:
    while line.find('<Placemark>') == -1:
        line = f.readline()
    line = f.readline()
    line = f.readline()
    line = f.readline()    
    name = f.readline().split('>')[1].split('<')[0]
    print name
    line = f.readline()    
    num = f.readline().split('>')[1].split('<')[0]
    print num
    line = f.readline()
    line = f.readline()
    line = f.readline()
    writeFile(name, num, line)
    line = f.readline()
    line = f.readline()

f.close()
