#Search module
import shlex, subprocess
import datetime
import os.path
import codecs
import logging

import utility
import Output

log = logging.getLogger('geocachepython.Search')

#TODO: handle exceptions more elegantly

def searchCaches(caches, search=""):
    """Search Caches Menu
    
    Gets search string from user, parses it and presents a menu of 
    options to perform on the caches selected
    """
    
    (options, args, search) = parse(search)
    
    if args:
        log.error("No Args please, ARGHHHHH!")
    cacheList = parseOptions(caches, options)
    
    act = 0
    while act != "-1":
        print "Search Menu - Your current search returned", len(cacheList), "caches."
        print "1) *Refine Search"
        print "2) *Clear Search"
        print "3) *View TextOnScreen"
        print "4) *Set FTF"
        print "5) *Set Found"
        print "6) Remove caches"
        print "7) *Send to GPS"
        print "8) *Output to CSV"
        print "9) Output to HTML"
        print "0) *Output to KML/Google Earth (cache saturation circles)"
        print "a) Output to county mapper format"
        print "Any other key to return to main menu"
        choice = raw_input("")
        actions = {"1": 'searchCaches(caches, search)', "2": 'searchCaches(caches)', "3": 'utility.viewCacheList(cacheList)', "4": 'setFTF(cacheList)', "5": 'setFound(cacheList)', "7": 'outputGPXToGarmin(cacheList)', '8': 'Output.writeCSV(cacheList)', '0': 'Output.writeKML(cacheList)', 'a': 'Output.writeCountyMapper(cacheList)'}
        log.debug("choice is %s" %choice)
        act = actions.get(choice, "-1")
        eval(act)
    return cacheList
    
def setFound(cacheList):
    """Sets caches in cacheList to found.
    
    Useful when a new stats query is unavailable.
    """
    for cache in cacheList:
        cache.found = 1
        print cache.gcid, "is now set to found"
                        
def setFTF(cacheList):
    """Sets caches in cacheList to ftf.
    
    Necessary since geocaching.com does not track ftf.
    """
    for cache in cacheList:
        cache.ftf = 1
        print cache.gcid, "is now set to ftf"
    
def outputGPXToGarmin(cacheList=[]):
    """Outputs a gpx file to garminOutputDDMMYY.gpx to send to gps."""
    
    #TODO: smart name fields
    #TODO: integrate with gpsbabel (perhaps use gpsbabel-python library
    #TODO: output proper xml through minidom
    
    #length of name field on GPS
    #need when specifying an output
    nameLength = 8
    
    if cacheList == []:
        cacheList = buildListOfGCID()
    
    today = datetime.datetime.today()
    outFile = "garminOutput" + str(today.date())
    print outFile
    f = codecs.open(outFile, 'w', 'utf-8', 'xmlcharrefreplace')
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<gpx version="1.0" \n\tcreator="GeoCachePython alarobric.homeip.net" \n\txmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \n\txmlns="http://www.topografix.com/GPX/1/0"\n\txsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">\n')
    s = "<time>" + str(today) + "</time>\n"
    f.write(s)
    #TODO should write bounds?
    
    for cache in cacheList:
        s = '<wpt lat="' + cache.lat + '" lon="' + cache.lon + '">\n'
        f.write(s)
        #<wpt lat="44.221783290" lon="-76.488766624">
        
        #is elevation necessary?
        #<ele>119.088135</ele>
        
        #s='\t<names>' + cache.gcid[:nameLength] + '</name>\n'
        ####s = '\t<name>' + unidecode(cache.cacheName[:nameLength]).replace('&', '&amp;').replace('<', '&lt;') + '</name>\n'
        s = '\t<name>' + cache.cacheName[:nameLength].replace('&', '&amp;').replace('<', '&lt;') + '</name>\n'
        #.encode("ascii", "xmlcharrefreplace")
        f.write(s)
        #<name>001</name>
        
        #unused by mine
        #<cmt>001</cmt>
        #<desc>001</desc>
        
        #what are the choices?
        #know Flag, Geocache
        f.write('\t<sym>Geocache</sym>\n')
        #<sym>Flag</sym>
        
        f.write('</wpt>\n')
    f.write('</gpx>')
    f.close()
    
    os.getcwd()
    args = "sudo gpsbabel -i gpx -f " + "'" + os.getcwd() + os.sep() + outFile + "' -o garmin -F /dev/ttyUSB0"
    args = shlex.split(args)
    #print args
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    p.wait()

def parse(search = "", s=True):
    """Get a search string from the user and parse it into a dictionary
    
    Optional argument of a previously used search string to display.
    TODO: find some way to use previous string but allow it's editing as well
    
    Returns: (options, args, search)
    options and args from parser and search string parsed
    """
    
    from optparse import OptionParser
    parser = OptionParser(usage = "usage: [option] <option argument> ...")
    
    parser.add_option("-n", "--name", dest="cacheName",
            help="cacheName")
    parser.add_option("-f", "--found",
            action="store_true", dest="found",
            help="only found caches")
    parser.add_option("-F", "--notfound",
            action="store_false", dest="found",
            help="only cache that have not been found (by you)")
    parser.add_option("-t", "--terrain", dest="terrain",
            help="comma seperated list or dashed range of terrain ratings to include. Ex: '1.5,2,2.5' or '1.5-2.5'")
    parser.add_option("-d", "--difficulty", dest="difficulty",
            help="comma seperated list or dashed range of difficulty ratings to include. Ex: '1.5,2,2.5' or '1.5-2.5'")
    parser.add_option("-g", "--gcid", dest="gcid",
            help="enter comma-seperated list of gcids with or without the gc prefix - case insensitive but no spaces")
    parser.add_option("-a", "--available", 
            action="store_true", dest="available",
            help="only show caches that are available (not disabled)")
    parser.add_option("-A", "--notavailable", 
            action="store_false", dest="available",
            help="only show caches that are not available (disabled)")
    parser.add_option("-b", "--archived", 
            action="store_true", dest="archived",
            help="only show caches that are archived")
    parser.add_option("-B", "--notarchived", 
            action="store_false", dest="archived",
            help="only show caches that are not archived")
    parser.add_option("-l", "--latitude", dest="lat",
            help="range of latitudes in following format: 'NXX XX.XXX-NXX XX.XXX' - don't forget quotes")
    parser.add_option("-L", "--longitude", dest="lon",
            help="range of longitudes in following format: 'WXXX XX.XXX-WXXX XX.XXX' - don't forget quotes")
    #TODO could allow NXX XX.XXX-XX.XXX
    parser.add_option("-c", "--container", dest="container",
            help="type of container: L=large, R=regular, S=small, M=micro, O=other, N=not chosen, V=virtual - can specify multiple ex L,R")
    parser.add_option("-T", "--type", dest="type",
            help="type of cache: T=traditional, M=multi, U=unknown/puzzle, V=virtual, L=letterbox, E=earthcache, N=event, G=mega-event - can specify multiple ex L,R")
    parser.add_option("-C", "--country", dest="country",
            help="country, can either use exact string used by groundspeak or possibly 2digit country code, ex. CA,US")
    parser.add_option("-s", "--state", dest="state",
            help="state/province, use exact string used by groundspeak, or US or CA state codes, ex. BC,WA,NY,ON")
    parser.add_option("-O", "--county", dest="county",
            help="county, use exact string or two character shortcode (see help for both) - C to get all caches without a county")
    parser.add_option("-o", "--owner", dest="owner",
            help="owner, finds all caches with owners containing your string as a substring")
    #TODO: cacheDate, placedBy, dateFound, dateImported, travelbug, distance from home

    #s=True is now a function parameter
    while (s == True):
        print "Search caches:   -h for help"
        s = False
        if search != "":
            print "Previous search:", search
        search = raw_input("Search string: ")
        if search == "-h":
            parser.print_help()
            s = True
    log.debug(shlex.split(search))
    (options, args) = parser.parse_args(shlex.split(search))
    log.debug(options)
    log.debug("args %s" %args)
    return (options, args, search)
   
def parseOptions(caches, options):
    """Parse through the dictionary of option from OptionParser and return a list of cache matching the search string
    
    TODO: test cases
    """
    cacheList = caches[:]
    
    #TODO: need other way of removing caches
    if options.found == True:
        print "found"
        for cache in cacheList[:]:
            if cache.found == False:
                cacheList.remove(cache)
    elif options.found == False:
        print "not found"
        for cache in cacheList[:]:
            if cache.found == True:
                cacheList.remove(cache)
    if options.available == True:
        print "available"
        for cache in cacheList[:]:
            if cache.available == False:
                cacheList.remove(cache)
    elif options.available == False:
        print "not available"
        for cache in cacheList[:]:
            if cache.available == True:
                cacheList.remove(cache)
    if options.archived == True:
        print "archived"
        for cache in cacheList[:]:
            if cache.archived == False:
                cacheList.remove(cache)
    elif options.archived == False:
        print "not archived"
        for cache in cacheList[:]:
            if cache.archived == True:
                cacheList.remove(cache)
    if options.terrain:
        #TODO: make this work with ranges as well
        print "terrain", options.terrain
        terr = options.terrain.split(',')
        tempList = []
        for cache in cacheList:
            for ter in terr:
                if cache.terrain == ter:
                    tempList.append(cache)
        cacheList = tempList
    if options.difficulty:
        print "difficulty", options.difficulty
        #TODO: make this work with ranges as well
        diff = options.difficulty.split(',')
        tempList = []
        for cache in cacheList:
            for dif in diff:
                if cache.terrain == dif:
                    tempList.append(cache)
        cacheList = tempList
    if options.gcid:
        print "gcid", options.gcid
        gcidList = []
        tempList = []
        for gcid in options.gcid.split(","):
            gcid = gcid.upper()
            if gcid[:2] != "GC":
                gcid = "GC" + gcid
            print gcid
            gcidList.append(gcid)
        for cache in cacheList:
            if cache.gcid in gcidList:
                tempList.append(cache)
        cacheList = tempList
    if options.lat:
        print "lat", options.lat
        first, second = options.lat.strip("'").split('-')
        print first, second
        first = utility.DMToDD(first)
        second = utility.DMToDD(second)
        print first, second
        if first == -1 or second == -1:
            raise Exception("Error parsing latitude")
        for cache in cacheList[:]:
            if cache.lat <= first or cache.lat >= second:
                cacheList.remove(cache)
    if options.lon:
        print "lon", options.lon
        first, second = options.lon.strip("'").split('-')
        print first, second
        first = utility.DMToDD(first)
        second = utility.DMToDD(second)
        print first, second
        if first == -1 or second == -1:
            raise Exception("Error parsing latitude")
        for cache in cacheList[:]:
            if cache.lon <= first or cache.lon >= second:
                cacheList.remove(cache)
    if options.cacheName:
        print "name", options.cacheName
        tempList = []
        for cache in cacheList:
            if cache.cacheName.find(options.cacheName) != -1:
                tempList.append(cache)
        cacheList = tempList
    if options.owner:
        print "owner", options.owner
        tempList = []
        for cache in cacheList:
            if cache.owner.find(options.owner) != -1:
                tempList.append(cache)
        cacheList = tempList
    if options.container:
        print "container", options.container
        containers = options.container.split(",")
        for cache in cacheList[:]:
            if cache.container[:1] not in containers:
                cacheList.remove(cache)
    if options.type:
        print "cacheType", options.type
        try:
            types = [{ type=="T": "Traditional Cache",
                    type=="M": "Multi-cache",
                    type=="U": "Unknown Cache",
                    type=="V": "Virtual Cache",
                    type=="L": "Letterbox Hybrid",
                    type=="E": "Earthcache",
                    type=="N": "Event Cache",
                    type=="G": "Mega-Event Cache" 
                    }[1] for type in options.type.split(",")]
        except KeyError:
            print "Bad cache type"
            return cacheList
        print types
        for cache in cacheList[:]:
            if cache.cacheType not in types:
                cacheList.remove(cache)
    if options.country:
        #TODO: add country codes
        print "country", options.country
        countries = options.country.split(",")
        for cache in cacheList[:]:
            if cache.country not in countries:
                cacheList.remove(cache)
    if options.state:
        #TODO: add state codes
        print "state", options.state
        states = options.state.split(",")
        for cache in cacheList[:]:
            if cache.state not in states:
                cacheList.remove(cache)
    if options.county:
        #TODO: add county codes
        print "county", options.county
        counties = options.county.split(",")
        if counties == ["C"]:
            print "YES"
            counties = [""]
        for cache in cacheList[:]:
            if cache.county not in counties:
                cacheList.remove(cache)
    return cacheList

    # Check if running as a program
if __name__ == '__main__':
    print "Running tests:"
    import doctest
    doctest.testmod()
else:
     # No, I must have been imported as a module
     pass
