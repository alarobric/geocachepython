#County mapper

import Search
import utility

import codecs
import os, shlex, subprocess
import logging

#gpsbabel -i gpx -f mine.gpx -o xcsv,style=mystyle.style -F mine.new
#gpsbabel -i geo -f 1.loc -x polygon,file=mycounty.txt -o mapsend -F 2.wpt

log = logging.getLogger('geocachepython.countyMapper')

def countyMapperMenu(caches):
    #Filters caches given by BC, then tries to assign them to a regional district of BC.
    
    #Menu to choose province
    print "Will search BC Caches and try to assign counties"
    
    #get caches in BC currently without a county
    (options, args, search) = Search.parse('-s "British Columbia" -O C', False)
    cacheList = Search.parseOptions(caches, options)
    
    #write these caches to a file
    filename = writeCountyMapper(cacheList)
    
    BCPolygons = ['BC/Alberni-Clayoquot.arc', 'BC/Bulkley-Nechako.arc', 'BC/Capital.arc',
                'BC/Cariboo.arc', 'BC/Central Coast.arc', 'BC/Central Kootenay.arc', 
                'BC/Central Okanagan.arc', 'BC/Columbia-Shuswap.arc', 'BC/Comox Valley.arc', 
                'BC/Cowichan Valley.arc', 'BC/East Kootenay.arc', 'BC/Fraser Valley.arc', 
                'BC/Fraser-Fort George.arc', 'BC/Greater Vancouver.arc', 'BC/Kitimat-Stikine.arc',
                'BC/Kootenay Boundary.arc',  'BC/Mount Waddington.arc', 'BC/Nanaimo.arc', 
                'BC/North Okanagan.arc', 'BC/Northern Rockies.arc', 'BC/Okanagan-Similkameen.arc',
                'BC/Peace River.arc', 'BC/Powell River.arc', 'BC/Skeena-Queen Charlotte.arc',
                'BC/Squamish-Lillooet.arc', 'BC/Stikine.arc', 'BC/Strathcona.arc', 
                'BC/Sunshine Coast.arc', 'BC/Thompson-Nicola.arc']
    #call GPSBabel to filter these caches through each polygon, then remove temp files
    gcids = {}
    for polygonName in BCPolygons:
        callPolygonFilter(filename, polygonName, "test.out")
        gcids.update(readCountyMapper(os.path.join(os.getcwd(), 'test.out'), polygonName[3:-4]))
        os.remove("test.out")
        if len(gcids) > 0:
            log.info("%s has caches" %(polygonName[3:]))
        else:
            log.info("%s does not have caches" %(polygonName[3:]))
    os.remove(filename)
    
    #save county name to caches
    for cache in cacheList:
        if cache.gcid in gcids.keys():
            cache.county = gcids[cache.gcid]
        else:
            log.error("%s was not found in a BC Regional District despite being in BC" %cache.gcid)
    return
    
def readCountyMapper(filename, countyName):
    f = codecs.open(filename, 'r', 'utf-8')
    gcids = {}
    
    line = f.readline()
    while line != "":
        gcids[line.split()[0]] = countyName
        line = f.readline()
    f.close()
    return gcids

def callPolygonFilter(filename, polygonFileName, outputFileName):
    os.getcwd()
    args = "gpsbabel -i xcsv,style='" + os.path.join(os.getcwd(), "CountyMapper", "countyMapperFormat.txt") +  "' -f '" + filename + "' -x polygon,file='" + os.path.join(os.getcwd(), "CountyMapper", polygonFileName) + "' -o xcsv,style='" + os.path.join(os.getcwd(), "CountyMapper", "countyMapperFormat.txt") + "' -F '" + outputFileName + "'"
    args = shlex.split(args)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    p.wait()
    
def writeCountyMapper(cacheList):
    filename = utility.saveFileDialog('gcm', 'countyMapper')
    log.debug('county mapper filename: %s' %filename)
    f = codecs.open(filename, 'w', encoding='utf-8', errors='strict')
    for cache in cacheList:
        f.write("%s\t%s\t%s\t%s\n" %(cache.gcid, cache.lat, cache.lon, cache.cacheName))
    f.close()
    return filename

# Check if running as a program
if __name__ == '__main__':
     print "Run Debug Suite"
else:
     # No, I must have been imported as a module
     pass
