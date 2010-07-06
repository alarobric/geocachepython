#County mapper

import Search
import utility

import codecs
import os, shlex, subprocess

#gpsbabel -i gpx -f mine.gpx -o xcsv,style=mystyle.style -F mine.new
#gpsbabel -i geo -f 1.loc -x polygon,file=mycounty.txt -o mapsend -F 2.wpt

def countyMapperMenu(caches):
    #Menu to choose province
    print "Will search BC Caches and try to assign counties"
    
    (options, args, search) = Search.parse('-s "British Columbia"', False)
    cacheList = Search.parseOptions(caches, options)
    filename = writeCountyMapper(cacheList)
    callPolygonFilter(filename, "BC/Thompson-Nicola.arc", "test.out")

def callPolygonFilter(filename, polygonFileName, outputFileName):
    os.getcwd()
    args = "gpsbabel -i xcsv,style=" + os.path.join(os.getcwd(), "CountyMapper", "countyMapperFormat.txt")
#    +  "' -f '" + filename + "' -x polygon,file='" + os.getcwd() + os.sep() + "CountyMapper" + os.sep() + polygonFileName + "' -o xcsv,style='" + os.getcwd() + os.sep() + "CountyMapper" + os.sep() + "countyMapperFormat.txt" + "' -F '" + outputFileName + "'"
    args = shlex.split(args)
    print args
    return
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    p.wait()
    
def writeCountyMapper(cacheList):
    filename = utility.saveFileDialog('gcm', 'countyMapper')
    print filename
    f = codecs.open(filename, 'w', encoding='utf-8', errors='strict')
    for cache in cacheList:
        f.write("%s\t%s\t%s\t%s\n" %(cache.gcid, cache.lat, cache.lon, cache.cacheName))
    f.close()
    return filename