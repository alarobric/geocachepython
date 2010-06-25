#UTILITY METHODS
def DMToDD(string):
    """Converts coordinates in Decimal Minute format to Decimal Degree.
    
    Returned as a string with latitude and longitude seperated by a space
    >>> DMToDD('N 44 19.395 W 076 32.595')
	'44.32325 -76.54325'
    >>> DMToDD('N44 23.1 W72')
    string wrong length
    -1
    """
    if len(string) == 24:
        negLat = 0
        negLon = 0
        
        if string[:2] == "N ":
            pass
        elif string[:2] == "S ":
            negLat = 1
        else:
            print "Error: No N or S at start of coords"
            return -1
        lat = int(string[2:4])
        minute = float(string[5:11])
        minute /= 60
        lat += minute
        if negLat == 1:
            lat = -lat

        if string[12:14] == "W ":
            negLon = 1
        elif string[12:14] == "E ":
            pass
        else:
            print "Error: No W or E or otherwise invalid format"
            return -1
        lon = int(string[14:17])
        minute = float(string[18:24])
        minute /= 60
        lon += minute
        if negLon == 1:
            lon = -lon

        return "%s %s" % (lat, lon)
    elif len(string) == 10:
        negLat = 0
        
        if string[:1] == "N":
            pass
        elif string[:1] == "S":
            negLat = 1
        else:
            print "Error: No N or S at start of coords"
            return -1
        lat = int(string[1:3])
        minute = float(string[4:10])
        minute /= 60
        lat += minute
        if negLat == 1:
            lat = -lat
        return "%s" % (lat)
    elif len(string) == 11:
        negLon = 0
        if string[:1] == "W":
            negLon = 1
        elif string[:1] == "E":
            pass
        else:
            print "Error: No W or E or otherwise invalid format"
            return -1
        lon = int(string[1:4])
        minute = float(string[5:11])
        minute /= 60
        lon += minute
        if negLon == 1:
            lon = -lon
        return "%s" %lon
        
def DDToDM(dd, latOrLon=0):
    """Converts coordinates in Decimal Degree format to Decimal Minutes for output.
    
    Returns string in pretty output format ex. 'N44 13.323 W76 32.322'
    latOrLon 1-latitude (N or S)
			 2-longitude (E or W)
	>>> DDToDM(10.123456789)
	'10 7.407'
    >>> DDToDM(44.32323, 1)
    'N44 19.394'
    >>> DDToDM(-76.54321, 2)
    'W76 32.593'
    
    """
    degree = int(float(dd))
    decimal = float(dd) % 1
    if degree < 0:
        decimal = 1 - decimal
    minutes = decimal * 60
    DM = "%d %0.3f" % (degree, minutes)
    if latOrLon == 1:
        if degree > 0:
            DM = "N" + DM
        else:
            DM = "S" + DM[1:]
    elif latOrLon == 2:
        if degree > 0:
            DM = "E" + DM
        else:
            DM = "W" + DM[1:]
    return DM

def toBool(value):
    """Converts string to bool"""
    if value == "True":
        return True
    elif value == "False":
        return False
    else:
		#TODO raise error
        return "Error"
        
def convertToRange(diff):
    """Converts a difficulty or terrain rating (1,1.5-5) to integer (1-9)
    
    >>> convertToRange(1.5)
    2
    >>> convertToRange(5)
    9
    """
    return int(float(diff) * 2 - 1)
    
def initializeMatrix():
    """Initializes D/T Matrix
    
    >>> initializeMatrix()
    [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    """
    
    matrix = []
    for i in range(9):
        matrix.append([0]*9)
    return matrix
    
def outputMatrix(matrix):
    """Prints D/T Matrix"""
    numOnes = 0
    print "     1   1.5   2   2.5   3   3.5   4   4.5   5"
    for i in range(9):
        print float(i+2) / 2, "",
        for j in range(9):
            print matrix[i][j], "  ",
            if matrix[i][j] == 1:
                numOnes = numOnes + 1
        print
    print "You've found", numOnes, "of the possible 81 difficulty/terrain combinations.", 81-numOnes, "to go!"
    
def stateCode(states):
    """Returns a string of state codes for each entry in given list of states.
    
    Prints an error to the screen if a state is not recognised
    >>> stateCode(['Utah', 'Blah'])
    ERROR: State not recognised: Blah
    'UT'
    """
    stateList = ""
    for state in states:
        stateDict = {
            "Utah": "UT",
            "Vermont": "VT",
            "Washington": "WA",
            "Alabama": "AL",
            "Louisiana": "LA",
            "Ohio": "OH",
            "Alaska": "AK",
            "Maine": "ME",
            "Oklahoma": "OK",
            "Arizona": "AZ",
            "Maryland": "MD",
            "Oregon": "OR",
            "Arkansas": "AR",
            "Massachusetts": "MA",
            "Pennsylvania": "PA",
            "California": "CA",
            "Michigan": "MI",
            "Rhode Island": "RI",
            "Colorado": "CO",
            "Minnesota": "MN",
            "South Carolina": "SC",
            "Connecticut": "CT",
            "Mississippi": "MS",
            "South Dakota": "SD",
            "Delaware": "DE",
            "Missouri": "MO",
            "Tennessee": "TN",
            "Florida": "FL",
            "Montana": "MT",
            "Texas": "TX",
            "Georgia": "GA",
            "Nebraska": "NE",
            "Hawaii": "HI",
            "Nevada": "NV",
            "Idaho": "ID",
            "New Hampshire": "NH",
            "Virginia": "VA",
            "Illinois": "IL",
            "New Jersey": "NJ",
            "Indiana": "IN",
            "New Mexico": "NM",
            "West Virginia": "WV",
            "Iowa": "IA",
            "New York": "NY",
            "Wisconsin": "WI",
            "Kansas": "KS",
            "North Carolina": "NC",
            "Wyoming": "WY",
            "Kentucky": "KY",
            "North Dakota": "ND"
        }
        if (stateDict.get(state, "") != ""):
            stateList = stateList + (stateDict.get(state))
        else:
            print "ERROR: State not recognised:", state
    return stateList              
    
def countryCode(countries):
    """Returns a string of country codes for each entry in given list of countries.
    
    Prints error to screen if a country is not recognised
    >>> countryCode(['Canada', 'Blah'])
    ERROR: Country not recognised: Blah
    'CA'
    """
    countryList = ""
    for country in countries:
        countryDict = {
            "Canada": "CA",
            "United States": "US"
        }
        if (countryDict.get(country, "") != ""):
            countryList = countryList + (countryDict.get(country))
        else:
            print "ERROR: Country not recognised:", country
    return countryList 
    #more country codes at http://www.iso.org/iso/english_country_names_and_code_elements
    
def viewCacheList(cacheList):
    """View Cache List"""
    #If lots of caches, get users confirmation
    if len(cacheList) > 20:
        print "List is long -", len(cacheList), "caches."
        choice = raw_input("Are you sure you wish to view the full list? (y/Y)")
        if choice != "y" and choice != "Y":
            return
    #display caches
    for cache in cacheList:
        print "----------------------------------"
        print cache.cacheName, "by", cache.owner, "hidden on", cache.cacheDate, "in", cache.state
        print "D:", cache.difficulty, "T:", cache.terrain, cache.cacheType, cache.container
        print 
    return
    
if __name__ == '__main__':
    # test myself
    import doctest
    doctest.testmod()
