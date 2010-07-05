#stats.py

import datetime
from utility import DDToDM, initializeMatrix, convertToRange, outputMatrix

def calculateMatrix(caches):
    """Calculates D/T matrix.
    
    Calls initializeMatrix(), then loops through caches and fills matrix - currently only 1 or 0.
    """
    #TODO: mechanism for knowing how many caches of each combo
    matrix = initializeMatrix()
    for cache in caches:
        if (cache.found == 1):
            matrix[convertToRange(cache.difficulty) - 1][convertToRange(cache.terrain) - 1] = 1
    return matrix

def statsToConsole(caches, homeLocation):
    """Outputs a wide variety of statistics to the screen.
    
    Need list of stats?
    """
	
    #output some stats
    foundCaches = []
    for cache in caches:
        if cache.found == 1:
            foundCaches.append(cache)
    
    #sort by ID of find logs
    foundCaches.sort(key=lambda obj: obj.foundLogID)
    
    #initialize variables
    states = []
    countries = []
    oldest = [foundCaches[0].gcid, foundCaches[0].cacheDate, foundCaches[0].cacheName]
    newest = oldest
    closest = [foundCaches[0].gcid, foundCaches[0].distanceToHome(homeLocation[0]), foundCaches[0].cacheName]
    farthest = closest
    north = [foundCaches[0].gcid, foundCaches[0].lat, foundCaches[0].cacheName]
    south = north
    east = [foundCaches[0].gcid, foundCaches[0].lon, foundCaches[0].cacheName]
    west = east
    oldestFind = foundCaches[0].dateFound
    #types - trad, multi, unknown, virtual, letterbox, earthcache, event, mega-event
    types = [0, 0, 0, 0, 0, 0, 0, 0]
    #containers - micro, small, regular, large, other, not chosen, virtual
    containers = [0, 0, 0, 0, 0, 0, 0]
    dayOfWeek = [0, 0, 0, 0, 0, 0, 0]
    averageDifficulty = 0
    averageTerrain = 0
    numArchived = 0
    ftfList = []
     
    for cache in foundCaches:
        #TODO - clean up list search
        try:
            temp = states.index(cache.state)
        except ValueError:
            states.append(cache.state)
        try:
            temp = countries.index(cache.country)
        except ValueError:
            countries.append(cache.country)
        if cache.cacheDate < oldest[1]:
            oldest = [cache.gcid, cache.cacheDate, cache.cacheName]
        if cache.cacheDate > newest[1]:
            newest = [cache.gcid, cache.cacheDate, cache.cacheName]
        if cache.distanceToHome(homeLocation[0]) < closest[1]:
            closest = [cache.gcid, cache.distanceToHome(homeLocation[0]), cache.cacheName]
        if cache.distanceToHome(homeLocation[0]) > farthest[1]:
            farthest = [cache.gcid, cache.distanceToHome(homeLocation[0]), cache.cacheName]
        if float(cache.lat) > float(north[1]):
            north = [cache.gcid, cache.lat, cache.cacheName]
        if float(cache.lat) < float(south[1]):
            south = [cache.gcid, cache.lat, cache.cacheName]
        if float(cache.lon) > float(east[1]):
            east = [cache.gcid, cache.lon, cache.cacheName]
        if float(cache.lon) < float(west[1]):
            west = [cache.gcid, cache.lon, cache.cacheName]
        if cache.dateFound < oldestFind:
            oldestFind = cache.dateFound
        if cache.cacheType == "Traditional Cache":
            types = [types[0]+1, types[1], types[2], types[3], types[4], types[5], types[6], types[7]]
        elif cache.cacheType == "Multi-cache":
            types = [types[0], types[1]+1, types[2], types[3], types[4], types[5], types[6], types[7]]
        elif cache.cacheType == "Unknown Cache":
            types = [types[0], types[1], types[2]+1, types[3], types[4], types[5], types[6], types[7]]
        elif cache.cacheType == "Virtual Cache":
            types = [types[0], types[1], types[2], types[3]+1, types[4], types[5], types[6], types[7]]
        elif cache.cacheType == "Letterbox Hybrid":
            types = [types[0], types[1], types[2], types[3], types[4]+1, types[5], types[6], types[7]]
        elif cache.cacheType == "Earthcache":
            types = [types[0], types[1], types[2], types[3], types[4], types[5]+1, types[6], types[7]]
        elif cache.cacheType == "Event Cache":
            types = [types[0], types[1], types[2], types[3], types[4], types[5], types[6]+1, types[7]]
        elif cache.cacheType == "Mega-Event Cache":
            types = [types[0], types[1], types[2], types[3], types[4], types[5], types[6], types[7]+1]
        else:
            print cache.cacheType
        if cache.container == "Micro":
            containers = [containers[0]+1, containers[1], containers[2], containers[3], containers[4], containers[5], containers[6]]
        elif cache.container == "Small":
            containers = [containers[0], containers[1]+1, containers[2], containers[3], containers[4], containers[5], containers[6]]
        elif cache.container == "Regular":
            containers = [containers[0], containers[1], containers[2]+1, containers[3], containers[4], containers[5], containers[6]]
        elif cache.container == "Large":
            containers = [containers[0], containers[1], containers[2], containers[3]+1, containers[4], containers[5], containers[6]]
        elif cache.container == "Other":
            containers = [containers[0], containers[1], containers[2], containers[3], containers[4]+1, containers[5], containers[6]]
        elif cache.container == "Not chosen":
            containers = [containers[0], containers[1], containers[2], containers[3], containers[4], containers[5]+1, containers[6]]
        elif cache.container == "Virtual":
            containers = [containers[0], containers[1], containers[2], containers[3], containers[4], containers[5], containers[6]+1]
        else:
            print cache.container
        averageDifficulty += float(cache.difficulty)
        averageTerrain += float(cache.terrain)
        if cache.archived:
            numArchived += 1
        if cache.ftf:
            ftfList.append(cache)
        dayOfWeek[cache.dateFound.isoweekday() - 1] += 1
                    
    typesTotal = sum(types)
    containersTotal = sum(containers)
    averageDifficulty = (averageDifficulty/len(foundCaches))
    averageTerrain = (averageTerrain/len(foundCaches))
    
    todayDate = datetime.date.today()
    daysCaching = (todayDate - oldestFind).days
    
    print ""
    print "---------STATS----------"
    print "You've found %d caches since %s" % (len(foundCaches), oldestFind)
    print "Overall find rate: %0.2f/day, %0.2f/week, %0.2f/month" % (float(len(foundCaches))/daysCaching, float(len(foundCaches))/daysCaching*7, float(len(foundCaches))/daysCaching*30)
    if(int(oldestFind.year) != int(todayDate.year)):
        thisYearsFoundCaches = [item for item in foundCaches if int(item.dateFound.year) == int(oldestFind.year)]
        daysCaching = 365 - (oldestFind - oldestFind.replace(month=1, day=1)).days
        print "%d find rate: %0.2f/day, %0.2f/week, %0.2f/month - %d finds" % (int(oldestFind.year), float(len(thisYearsFoundCaches))/daysCaching, float(len(thisYearsFoundCaches))/daysCaching*7, float(len(thisYearsFoundCaches))/daysCaching*30, len(thisYearsFoundCaches))
    daysCaching = 365
    for year in range(int(oldestFind.year) + 1, int(todayDate.year)):
        thisYearsFoundCaches = [item for item in foundCaches if int(item.dateFound.year) == year]
        print "%d find rate: %0.2f/day, %0.2f/week, %0.2f/month - %d finds" % (year, float(len(thisYearsFoundCaches))/daysCaching, float(len(thisYearsFoundCaches))/daysCaching*7, float(len(thisYearsFoundCaches))/daysCaching*30, len(thisYearsFoundCaches))
    thisYearsFoundCaches = [item for item in foundCaches if int(item.dateFound.year) == int(todayDate.year)]
    daysCaching = (todayDate - todayDate.replace(month=1, day=1)).days
    print "%d find rate: %0.2f/day, %0.2f/week, %0.2f/month - %d finds" % (year+1, float(len(thisYearsFoundCaches))/daysCaching, float(len(thisYearsFoundCaches))/daysCaching*7, float(len(thisYearsFoundCaches))/daysCaching*30, len(thisYearsFoundCaches))
    
    print "Average Difficulty: %0.1f" % (averageDifficulty)
    print "Average Terrain: %0.1f" % (averageTerrain)
    
    print "%d of the caches have now been archived (%0.1f%%)" % (numArchived, float(100*numArchived)/len(foundCaches))
    
    if (len(ftfList) != 0):
        print "FTF List"
        for item in ftfList:
            print "*", item.cacheName
    
    print "States cached in:"
    for state in states:
        print "*", state
    
    print "Countries cached in:"
    for country in countries:
        print "*", country
            
    daysofWeek = ['Monday:    ', 'Tuesday:   ', 'Wednesday: ', 'Thursday:  ', 'Friday:    ', 'Saturday: ', 'Sunday:    ']  
    print
    print "By Day of Week:  "    
    for i in range(len(dayOfWeek)):
        print "%s\t%d\t%0.1f%%" % (daysofWeek[i], dayOfWeek[i], float(dayOfWeek[i])/len(foundCaches)*100)
    
    print ""
    print "Oldest cache found:\n* %s - %s - %s" % (oldest[0], oldest[1], oldest[2])
    print "Newest cache found:\n* %s - %s - %s" % (newest[0], newest[1], newest[2])
    print "Closest cache found:\n* %s - %0.1fkm - %s" % (closest[0], closest[1], closest[2])
    print "Farthest cache found:\n* %s - %0.1fkm - %s" % (farthest[0], farthest[1], farthest[2])
    print "Most Westerly Cache:\n* %s - %s - %s" % (west[0], DDToDM(west[1], 2), west[2])
    print "Most Easterly Cache:\n* %s - %s - %s" % (east[0], DDToDM(east[1], 2), east[2])
    print "Most Northerly Cache:\n* %s - %s - %s" % (north[0], DDToDM(north[1], 1), north[2])
    print "Most Southerly Cache:\n* %s - %s - %s" % (south[0], DDToDM(south[1], 1), south[2])
    print
    print "Cache types:"
    print "  Type\t\tNumber\tPercentage"
    print "* Traditional: \t%4d%8.1f\n* Multi: \t%4d%8.1f\n* Unknown: \t%4d%8.1f\n* Virtual: \t%4d%8.1f\n* Letterbox: \t%4d%8.1f\n* Earthcache: \t%4d%8.1f\n* Event: \t%4d%8.1f\n* Mega-Event: \t%4d%8.1f" % (types[0], 100.0 * types[0] / typesTotal, types[1], 100.0 * types[1] / typesTotal, types[2], 100.0 * types[2] / typesTotal, types[3], 100.0 * types[3] / typesTotal, types[4], 100.0 * types[4] / typesTotal, types[5], 100.0 * types[5] / typesTotal, types[6], 100.0 * types[6] / typesTotal, types[7], 100.0 * types[7] / typesTotal)
    print "Container types:"
    print "  Type\t\tNumber\tPercentage"
    print "* Micro: \t%4d%8.1f\n* Small: \t%4d%8.1f\n* Regular: \t%4d%8.1f\n* Large: \t%4d%8.1f\n* Other: \t%4d%8.1f\n* Not Chosen: \t%4d%8.1f\n* Virtual: \t%4d%8.1f" % (containers[0], 100.0* containers[0] / containersTotal, containers[1], 100.0*containers[1]/containersTotal, containers[2], 100.0*containers[2]/containersTotal, containers[3], 100.0*containers[3]/containersTotal, containers[4], 100.0*containers[4]/containersTotal, containers[5], 100.0*containers[5]/containersTotal, containers[6], 100.0*containers[6]/containersTotal)
    print ""
    matrix = calculateMatrix(caches)
    outputMatrix(matrix)
        

def statsToHTML():
    """Outputs a variety of caching statistics to an html file.
    
    Under heavy development
    """
    foundCaches = []
    for cache in caches:
        if cache.found == 1:
            foundCaches.append(cache)
'''                    
    output = open('stats.html', 'w')
    output.write("<HTML>\n<HEAD>")
    output.write('<script type="text/javascript" src="http://www.google.com/jsapi"></script><script type="text/javascript">google.load("visualization", "1", {packages: ["geomap"]});function drawVisualization() {var data = new google.visualization.DataTable();data.addRows(6);data.addColumn("string", "Country");data.addColumn("number", "Popularity");data.setValue(0, 0, "Germany");data.setValue(0, 1, 200);data.setValue(1, 0, "United States");data.setValue(1, 1, 300);data.setValue(2, 0, "Brazil");data.setValue(2, 1, 400);data.setValue(3, 0, "Canada");data.setValue(3, 1, 500);data.setValue(4, 0, "France");data.setValue(4, 1, 600);data.setValue(5, 0, "RU");data.setValue(5, 1, 700);var geomap = new google.visualization.GeoMap(document.getElementById("visualization"));geomap.draw(data, null);}google.setOnLoadCallback(drawVisualization);</script></HEAD>\n<BODY>\n"')
    
    output.write("<p>Hi this is a test of stats.html\n")
    
    output.write("<table>\n<tr><td>---------STATS----------</td></tr>\n")
    output.write("<tr><td>You've found %d caches since %s</td></tr>\n" % (len(foundCaches), oldestFind[:10]))
    
    #states
    output.write("<tr><p>States cached in:</tr>\n")
    stateList = (stateCode(states))
    stateListValues = "100"
    for i in range((len(stateList) / 2) -1):
        stateListValues = stateListValues + ",100"
    output.write("<tr><img src=http://chart.apis.google.com/chart?cht=t&chs=440x220&chtm=usa&chld=%s&chd=t:%s&chco=BEBEBE,AAFFAA,FF0000></tr>\n" % (stateList, stateListValues))
    
    #countries
    output.write("<tr><p>Countries cached in:</tr>\n")
    countryList = (countryCode(countries))
    countryListValues = "100"
    for i in range((len(countryList) / 2) -1):
        countryListValues = countryListValues + ",100"
    output.write("<tr><img src=http://chart.apis.google.com/chart?cht=t&chs=440x220&chtm=world&chld=%s&chd=t:%s&chco=BEBEBE,AAFFAA,FF0000></tr>\n" % (countryList, countryListValues))
    
    output.write("</table>\n")
    
    output.write("<div id='visualization' style='width: 800px; height: 400px;'></div>")
    
    print ""
    print "Oldest cache found:\n* %s - %s - %s" % (oldest[0], oldest[1], oldest[2])
    print "Newest cache found:\n* %s - %s - %s" % (newest[0], newest[1], newest[2])
    print "Closest cache found:\n* %s - %0.1fkm - %s" % (closest[0], closest[1], closest[2])
    print "Farthest cache found:\n* %s - %0.1fkm - %s" % (farthest[0], farthest[1], farthest[2])
    print "Most Westerly Cache:\n* %s - %s - %s" % (west[0], DDToDM(west[1], 2), west[2])
    print "Most Easterly Cache:\n* %s - %s - %s" % (east[0], DDToDM(east[1], 2), east[2])
    print "Most Northerly Cache:\n* %s - %s - %s" % (north[0], DDToDM(north[1], 1), north[2])
    print "Most Southerly Cache:\n* %s - %s - %s" % (south[0], DDToDM(south[1], 1), south[2])
    print
    print "Cache types:"
    print "  Type\t\tNumber\tPercentage"
    print "* Traditional: \t%4d%8.1f\n* Multi: \t%4d%8.1f\n* Unknown: \t%4d%8.1f\n* Virtual: \t%4d%8.1f\n* Letterbox: \t%4d%8.1f\n* Earthcache: \t%4d%8.1f\n* Event: \t%4d%8.1f" % (types[0], 100.0 * types[0] / typesTotal, types[1], 100.0 * types[1] / typesTotal, types[2], 100.0 * types[2] / typesTotal, types[3], 100.0 * types[3] / typesTotal, types[4], 100.0 * types[4] / typesTotal, types[5], 100.0 * types[5] / typesTotal, types[6], 100.0 * types[6] / typesTotal)
    print "Container types:"
    print "* Micro: %d\n* Small: %d\n* Regular: %d\n* Large: %d\n* Other: %d\n* Not Chosen: %d\n* Virtual: %d" % (containers[0], containers[1], containers[2], containers[3], containers[4], containers[5], containers[6])
    print ""
    matrix = calculateMatrix()
    outputMatrix(matrix)
    
    

    
    
    output.write("<img src=http://chart.apis.google.com/chart?cht=s&chd=t:12,87,75,41,23,96,68,71,34,9|98,60,27,34,56,79,58,74,18,76&chs=200x200&chtt=Chart%20Title>")

    output.write("\n</BODY>\n</HTML>")
    output.close()
    print "Stats output to html file: stats.html"
'''
#end stats to html
