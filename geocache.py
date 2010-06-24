from geopy import distance, util

class Geocache: 
    """Geocache class - Describes all attributes of a geocache.
    
    Further info......
    """
    
    def __init__(self, cacheDateIN, gcidIN, urlIN, difficultyIN, terrainIN, cacheNameIN, latIN, lonIN, foundIN, cacheIDIN, availableIN, archivedIN, placedByIN, ownerIDIN, ownerIN, cacheTypeIN, containerIN, countryIN, stateIN, shortDescIN, longDescIN, hintIN, dateFoundIN, foundLogIDIN, dateImportedIN, travelbugIN, ftfIN):
        """Creates a new Geocache object.
        
        Setting geocache attributes as passed in by parameter.
        """
        self.cacheDate = cacheDateIN
        self.gcid = gcidIN
        self.url = urlIN
        self.difficulty = difficultyIN
        self.terrain = terrainIN
        self.cacheName = cacheNameIN
        self.lat = latIN
        self.lon = lonIN
        self.found = foundIN
        self.cacheID = cacheIDIN
        self.available = availableIN
        self.archived = archivedIN
        self.placedBy = placedByIN
        self.ownerID = ownerIDIN
        self.owner = ownerIN
        self.cacheType = cacheTypeIN
        self.container = containerIN
        self.country = countryIN
        self.state = stateIN
        self.shortDesc = shortDescIN
        self.longDesc = longDescIN
        self.hint = hintIN
        self.dateFound = dateFoundIN
        self.foundLogID = foundLogIDIN
        self.dateImported = dateImportedIN
        self.travelbug = travelbugIN
        self.ftf = ftfIN
        #print "cache created in memory successfully"
           
    def checkUpdateCache(self, otherCache):
        """Checks if otherCache needs updating from info in self."""
        
        oldDate = otherCache.dateImported
        newDate = self.dateImported
        #print "Date of old cache:", oldDate, "Date of new cache:", newDate
        if oldDate == newDate:
            print "Same import date, no updates were made"
            return 0
        else:
            print "Dates differ update necessary"
            #need to check which is newer - 
            #TODO change to straight alphabetical check
            print "year:", newDate[:4]
            if newDate[:4] > oldDate[:4]:
                print "newer year"
                self.updateCache(otherCache)
                return 1
            elif newDate[:4] == oldDate[:4]:
                print "month:", newDate[5:7]
                if newDate[5:7] > oldDate[5:7]:
                    print "newer month"
                    self.updateCache(otherCache)
                    return 1
                elif newDate[5:7] == oldDate[5:7]:
                    print "day:", newDate[8:10]
                    if newDate[8:10] > oldDate[8:10]:
                        print "newer day"
                        self.updateCache(otherCache)
                        return 1
                    elif newDate[8:10] == oldDate[8:10]:
                        print "same day - check times"
            print "Must be older"
            return 0
                    
    def updateCache(self, otherCache):
        """Updates all attributes of otherCache with values from self.
        
        ftf status is unchanged, since this cannot be imported
        """
        print "updating cache..."
        otherCache.cacheDate = self.cacheDate
        otherCache.gcid = self.gcid
        otherCache.url = self.url
        otherCache.difficulty = self.difficulty
        otherCache.terrain = self.terrain
        otherCache.cacheName = self.cacheName
        otherCache.lat = self.lat
        otherCache.lon = self.lon
        otherCache.found = self.found
        otherCache.cacheID = self.cacheID
        otherCache.available = self.available
        otherCache.archived = self.archived
        otherCache.placedBy = self.placedBy
        otherCache.ownerID = self.ownerID
        otherCache.owner = self.owner
        otherCache.cacheType = self.cacheType
        otherCache.container = self.container
        otherCache.country = self.country
        otherCache.state = self.state
        otherCache.shortDesc = self.shortDesc
        otherCache.longDesc = self.longDesc
        otherCache.hint = self.hint
        otherCache.dateFound = self.dateFound
        otherCache.foundLogID = self.foundLogID
        otherCache.dateImported = self.dateImported
        otherCache.travelbug = self.travelbug
        #don't change ftf status, since won't be imported
            
    def checkUnique(self, caches):
        """check this cache against others for doubles - if found run checkUpdateCache
        
        return 1 for a unique cache
        """
        for otherCache in caches:
            if otherCache.gcid == self.gcid:
                print "Possible match: ",
                if self.checkUpdateCache(otherCache):
                    print "updated cache"
                else:
                    print "nothing new"
                return 0
        return 1
        
    def distanceToHome(self, home):
        """Returns distance from self to current home location in kilometers."""
        return distance.distance(home, util.parse_geo("%s %s" % (self.lat, self.lon))).kilometers
#end Geocache class 

# Check if running as a program
if __name__ == '__main__':
     print "Run Debug Suite"
else:
     # No, I must have been imported as a module
     pass
