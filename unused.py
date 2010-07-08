#Unused functions

#TODO print travelbugs
def printCacheFull(cache):
    """Prints a full cache description - needs redoing."""
    print "%s placed by %s and owned by %s" % (cache.cacheName, cache.placedBy, cache.owner)
    print "   Published %s - %s - Difficulty:%s Terrain:%s" % (cache.cacheDate, cache.gcid, cache.difficulty, cache.terrain)
    print "   Latitude:%s Longitude:%s - coord.info/%s" % (cache.lat, cache.lon, cache.gcid)
    print "   Distance from home location:", cache.distanceToHome(homeLocation[0])
    print "   Imported on %s:", cache.dateImported

    if cache.found == 1:
        print "You've found this cache!",
    else:
        print "You haven't found this cache yet.",
    if cache.available == 1:
        print "Cache is available.",
    else:
        print "Cache is unavailable.",
    if cache.archived == 1:
        print "Cache is archived."
    else:
        print
    print "Cache type:%s - Container:%s" % (cache.cacheType, cache.container)
    print "%s - %s" % (cache.country, cache.state)
    print ""
    print
    print cache.shortDesc
    print
    print cache.longDesc
    print
    print cache.hint
    print
    print
    
def printCacheMid(cache):
    """Prints a medium detail cache description - needs overhaul."""
    print "%s placed by %s and owned by %s" % (cache.cacheName, cache.placedBy, cache.owner)
    print "   Published %s - %s - Difficulty:%s Terrain:%s" % (cache.cacheDate, cache.gcid, cache.difficulty, cache.terrain)
    print "   Latitude:%s Longitude:%s - coord.info/%s" % (cache.lat, cache.lon, cache.gcid)
    print "   Distance from home location:", cache.distanceToHome(homeLocation[0])
    print "   Imported on %s:", cache.dateImported

    if cache.found == 1:
        print "You've found this cache!",
    else:
        print "You haven't found this cache yet.",
    if cache.available == 1:
        print "Cache is available.",
    else:
        print "Cache is unavailable.",
    if cache.archived == 1:
        print "Cache is archived."
    else:
        print
    print "Cache type:%s - Container:%s" % (cache.cacheType, cache.container)
    print "%s - %s" % (cache.country, cache.state)
    print ""
    print
    print

def printCacheShort(cache):
    """Prints a short description of the cache."""
    try:
        print cache.gcid, " ", cache.cacheName
        print "D:%s T:%s  coord.info/%s" % (cache.difficulty, cache.terrain, cache.gcid)
        print "Distance from home location: %0.1fkm" % cache.distanceToHome(homeLocation[0])
        print
    except UnicodeEncodeError:
        print "ERROR printing unicode character - sorry"
        print
		
		
def displayCache():
    """Display a cache."""
    choice = raw_input("Please enter the gcid of the cache you wish to display: ")
    choice = choice.upper()
    if choice[:2] != "GC":
        choice = "GC" + choice
    for cache in caches:
        if cache.gcid == choice:
            printCacheFull(cache)
            return
    print "No cache found for: %s" % (choice)
    
def debug():
    """Temporary holder for new function testing."""
    
    #look for earthcaches
    for cache in caches:
        if cache.found == 0:
            if cache.cacheType == "Traditional Cache":
                pass
            elif cache.cacheType == "Multi-cache":
                pass
            elif cache.cacheType == "Unknown Cache":
                pass
            elif cache.cacheType == "Virtual Cache":
                print "Virtual:", cache.gcid
            elif cache.cacheType == "Letterbox Hybrid":
                print "Letterbox:", cache.gcid
            elif cache.cacheType == "Earthcache":
                print "Earthcache:", cache.gcid
            elif cache.cacheType == "Event Cache":
                pass
            else:
                print cache.cacheType, cache.gcid

# Check if running as a program
if __name__ == '__main__':
     print "Run Debug Suite"
else:
     # No, I must have been imported as a module
     pass
