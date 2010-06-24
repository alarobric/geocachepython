'''geocachepython

Geocache Database by Alan Richards
code.google.com/p/geocachepython
'''
# -*- coding: utf-8 -*-
VERSION = '0.5.9'

import xml.dom.minidom
import os.path
import pickle
import zipfile
import webbrowser
from geopy import distance, util
import codecs
import datetime
#import time
#import operator
import shlex, subprocess

import geocache
from utility import *
import stats
import globals
import HomeLocation
import Search

def readGPX(wpts, timeCreated):
    """Reads through gpx file and updates or appends new caches to global list caches."""
    
    #iterated through wpt records, retrieve and write data
    for i, wpt in enumerate(wpts):
        #read each element of a wpt record
        timeElement = (getText(wpt.getElementsByTagName("time")[0].childNodes)[:10])
        gcidElement = getText(wpt.getElementsByTagName("name")[0].childNodes)
        urlElement = getText(wpt.getElementsByTagName("url")[0].childNodes)
        difficultyElement = getText(wpt.getElementsByTagName("groundspeak:difficulty")[0].childNodes)
        terrainElement = getText(wpt.getElementsByTagName("groundspeak:terrain")[0].childNodes)
        nameElement = getText(wpt.getElementsByTagName("groundspeak:name")[0].childNodes)
        latElement = wpt.attributes["lat"].value
        lonElement = wpt.attributes["lon"].value
        symElement = getText(wpt.getElementsByTagName("sym")[0].childNodes)
        if symElement == "Geocache Found":
            symElement = 1
        else:
            symElement = 0
        cacheElement = wpt.getElementsByTagName("groundspeak:cache")[0]
        cacheIDElement = cacheElement.attributes["id"].value
        availableElement = toBool(cacheElement.attributes["available"].value)
        archivedElement = toBool(cacheElement.attributes["archived"].value)
        placedByElement = getText(wpt.getElementsByTagName("groundspeak:placed_by")[0].childNodes)
        ownerIDElement = wpt.getElementsByTagName("groundspeak:owner")[0].attributes["id"].value
        ownerElement = getText(wpt.getElementsByTagName("groundspeak:owner")[0].childNodes)
        typeElement = getText(wpt.getElementsByTagName("groundspeak:type")[0].childNodes)
        containerElement = getText(wpt.getElementsByTagName("groundspeak:container")[0].childNodes)
        countryElement = getText(wpt.getElementsByTagName("groundspeak:country")[0].childNodes)
        stateElement = getText(wpt.getElementsByTagName("groundspeak:state")[0].childNodes)
        shortDescElement = getText(wpt.getElementsByTagName("groundspeak:short_description")[0].childNodes)
        longDescElement = getText(wpt.getElementsByTagName("groundspeak:long_description")[0].childNodes)
        hintElement = getText(wpt.getElementsByTagName("groundspeak:encoded_hints")[0].childNodes)
        travelbugsElements = wpt.getElementsByTagName("groundspeak:travelbug")
        travelbugID, travelbugREF, travelbugName = [], [], []
        for j in travelbugsElements:
            #print i
            travelbugID.append(j.attributes["id"].value)
            travelbugREF.append(j.attributes["ref"].value)
            travelbugName.append(getText(j.getElementsByTagName("groundspeak:name")[0].childNodes))
        travelbugElement = [travelbugID, travelbugREF, travelbugName]
        #logs
        logsElement = wpt.getElementsByTagName("groundspeak:logs")
        logs = logsElement[0].getElementsByTagName("groundspeak:log")
        dateFoundElement = "" #TODO - check this makes sense
        foundLogIDElement = "" #TODO - and this
        for log in logs:
            logDate = getText(log.getElementsByTagName("groundspeak:date")[0].childNodes)
            logType = getText(log.getElementsByTagName("groundspeak:type")[0].childNodes)
            logID = log.attributes["id"].value
            if (logType == "Found it" or logType == "Attended"):
                dateFoundElement = datetime.date(int(logDate[:4]), int(logDate[5:7]), int(logDate[8:10]))
                #dateFoundElement = datetime.date(*time.strptime(logDate[:10], "%Y-%m-%d")[0:5])
                print "Found cache %s" % (logDate)
                foundLogIDElement = logID
                break

        ftfElement = 0
        
        #unique = 1
        #record = 0
        #for cache in caches:
        #    if cache.gcid == gcidElement:
        #        print "Cache exists:", gcidElement
        #        unique = 0
        #        record = i
        #        break

        #if unique == 1:        
        tempCache = geocache.Geocache(timeElement, gcidElement, urlElement, difficultyElement, terrainElement, nameElement, latElement, lonElement, symElement, cacheIDElement, availableElement, archivedElement, placedByElement, ownerIDElement, ownerElement, typeElement, containerElement, countryElement, stateElement, shortDescElement, longDescElement, hintElement, dateFoundElement, foundLogIDElement, timeCreated, travelbugElement, ftfElement)
        if tempCache.checkUnique(caches) == 1:
            caches.append(tempCache)
        #logs

def getText(nodelist):
    """Gets text from a node."""
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def printHeader(name, timeCreated, numWpts):
    """Prints header from a gpx file."""
    print "Pocket Query: %s , Created: %s, containing %d waypoints" % (getText(name.childNodes), getText(timeCreated.childNodes)[:10], numWpts)

def searchMatrix(matrix, output):
    """Search D/T matrix for caches that would fill it.
    
    output is an option for choosing what to do with each cache that meets the criteria
    """
    #TODO:redo this so it returns a list (perhaps of GCIDs) that can share methods already written
    if output == 4:
        outFile = 'cacheOutput.html'
        initHTML(outFile)
    for cache in caches:
        if (matrix[convertToRange(cache.difficulty) - 1][convertToRange(cache.terrain) - 1] == 0):
            if output == 1:
                printCacheFull(cache)
            elif output == 2:
                printCacheMid(cache)
            elif output == 3:
                printCacheShort(cache)
            elif output == 4:
                exportHTML(cache, outFile)
    if output == 4:
        print "showHTML"
        showHTML(outFile)

def pickGPX():
    """Pick a GPX or ZIP file to import.
    
    Offers user a choice of all zip and gpx files in the working directory. Gets query name from gpx for more detail.
    """
    #print os.name
    path = os.getcwd()  # gets current working directory
    fileList = []
    dirList = os.listdir(path)
    for fname in dirList:
        #check for zip or gpx extension
        ext = fname.split(".")[len(fname.split("."))-1]
        if ext == "zip" or ext == "gpx":
            fileList.append(fname)
    print "Loading file list..."
    fileChoices = "Please choose a file: \n0) None\n"
    for i in range(len(fileList)):
        fname = fileList[i]
        ext = fname.split(".")[len(fname.split("."))-1]
        if ext == "gpx":
            xmldom = xml.dom.minidom.parse(fname)
        elif ext == "zip":
            zipped = zipfile.ZipFile(fname, "r")
            gpx = zipped.read(fname[:-4] + ".gpx")
            xmldom = xml.dom.minidom.parseString(gpx)
            zipped.close()
        name = xmldom.getElementsByTagName("name")[0]
        fileChoices += "%s) %s - %s \n" % (i+1, fileList[i], getText(name.childNodes))
    print fileChoices
    choice = raw_input("")
    choice = int(choice)
    if choice > 0 and choice <= len(fileList): #and choice == str(int(choice)):
        choice = int(choice)
        fname = fileList[choice-1]
        ext = fname.split(".")[len(fname.split("."))-1]
        print "You picked", fname, "which is a", ext
        if ext == "gpx":
            return xml.dom.minidom.parse(fname)
        elif ext == "zip":
            zipped = zipfile.ZipFile(fname, "r")
            print zipped.namelist(), "files in zip"
            #need to check this exists
            gpx = zipped.read(fname[:-4] + ".gpx")
            xmldom = xml.dom.minidom.parseString(gpx)
            zipped.close()
            return xmldom
            #can possibly clean this up a little
        else:
            print "ERROR - somehow selected a file that is not gpx or zip"
    print "No choice"
    return -1

def loadDatabase():
    """Loads saved database on startup"""
    caches = []
    homeLoc = HomeLocation.HomeLocation()
    print len(caches)
    #choice = raw_input("Load previous data.pkl file? ")
    choice = "y"
    if choice == "Y" or choice == "y":
        #to depickle
        try:
            pkl_file = open('geoDatabase.pkl', 'rb')
            homeLoc = pickle.load(pkl_file)
            caches = pickle.load(pkl_file)
            print "Number of records loaded:", len(caches)
            print "Locations loaded:", homeLoc.homeName
            pkl_file.close()
        except IOError:
            print "No geoDatabase.pkl file found, no records loaded"
    #if len(caches) == 0:
    #	return [homeLoc, []]
    return [homeLoc, caches]

#saves database on exit
def saveDatabase():
    """Saves cache database on exit."""
    choice = raw_input("Save database?")
    if choice == "Y" or choice == "y":
        output = open('geoDatabase.pkl', 'wb')

        # Pickle dictionary using protocol 0.
        pickle.dump(homeLoc, output)
        pickle.dump(caches, output)

        output.close()
        print "Database Saved - Bye..."
    else:
        print "Database not saved - Come back soon..."     

def initHTML(outFile):
    """Writes html headers to file."""
    f = open(outFile, 'w')
    f.write('''<html><head><meta content="text/html; charset=ISO-8859-1" http-equiv="content-type"><title>Cache Output</title></head><body>''')
    f.close()
    
def exportHTML(cache, outFile, desc=1):
    """Writes cache info to file in html format."""
    f = codecs.open(outFile, 'a', "utf-8")
    f.write('<b><font face="Verdana" size="3">%s</b><br>' %cache.cacheName)
    f.write('<b><font size="1">A cache by </b>%s&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Hidden:</b> %s &nbsp; ' %(cache.owner, cache.cacheDate))
    f.write('<b>GCID:</b>&nbsp;%s&nbsp;&nbsp;<a href="http://coord.info/%s">coord.info/%s</a><br>' %(cache.gcid, cache.gcid, cache.gcid))
    f.write('<b>Latitude:</b> %s &nbsp;<b>Longitude:</b> %s &nbsp' %(DDToDM(cache.lat), DDToDM(cache.lon)))
    f.write('<b>Size:</b>&nbsp;%s&nbsp;&nbsp;&nbsp;<b>Difficulty:</b> %s &nbsp;&nbsp;&nbsp;<b>Terrain:</b>&nbsp;%s' %(cache.container, cache.difficulty, cache.terrain))
    f.write('<b>Distance from %s:<b>&nbsp;%0.2fkm<br>' %(homeLoc.homeName[0], cache.distanceToHome(homeLoc.homeLocation[0])))
    if desc == 2:
        f.write('%s<br><br>%s<br><b>Hint: </b>%s<br><br>' %(cache.shortDesc, cache.longDesc, cache.hint))
    elif desc == 1:
        f.write('%s<br><b>Hint: </b>%s<br><br>' %(cache.shortDesc, cache.hint))
    f.close()  
    
def showHTML(outFile):
    """Writes footers to html file and attempts to open it in user's web browser."""
        #TODO need to make more robust - use working directory
    f = open(outFile, 'a')
    f.write('''</body></html>''')
    f.close()
    print outFile
    try:
        webbrowser.open(outFile, 2)
    except IOError:
        print "exception"
        outFile = "/Users/alarobric/Documents/Geocaching/GeoCachePython/cacheOutput.html"
        webbrowser.open(outFile, 2)
        
def closestCaches():
    """Prints the 10 closest caches."""
    #find 10 closest caches
    #TODO - need to be active caches
    #TODO - use choice
    #choice = raw_input("Just unfound caches?")
    cacheList = []
    farthestDist = 0
    farthestID = 0
    for cache in caches:
        if len(cacheList) < 10 and cache.found == False:
            cacheList.append(cache)
            farthestDist = 0
            #recalculate farthest
            for j in cacheList:
                if j.distanceToHome(homeLocation[0]) > farthestDist:
                    farthestDist = j.distanceToHome(homeLocation[0])
                    farthestID = j
        elif cache.distanceToHome(homeLocation[0]) < farthestDist and cache.found == False:
            #remove farthest and add new one
            cacheList.remove(farthestID)
            cacheList.append(cache)
            #recalculate farthest
            farthestDist = 0
            for j in cacheList:
                if j.distanceToHome(homeLocation[0]) > farthestDist:
                    farthestDist = j.distanceToHome(homeLocation[0])
                    farthestID = j
                    
    #TODO sort cacheList
    
    print "\nYour 10 Closest Caches are:"
    for i in cacheList:
        print i.gcid, i.cacheName, "%0.1fkm" % i.distanceToHome(homeLocation[0])
        
def outputCSV():
    """Outputs a list of all found caches to a csv file."""
        #output found caches to csv for excel use
    f = codecs.open('foundCache.csv', 'w', "utf-8")
    f.write("GCID, cacheDate, cacheName, state")
    
    for cache in caches:
        if cache.found == 1:
            f.write("\n%s,%s,%s,%s" %(cache.gcid, cache.dateFound, cache.cacheName, cache.state))

    f.close()
    print "foundCache.csv written successfully"        
       
def removeUnfoundCaches():
    """Remove unfound caches from database."""
    i = 0
    for cache in caches[:]:
        if (cache.found == 0):
            caches.remove(cache)
            i += 1
    print "Removed", i, "unfound caches from the database"       


def DTComboMatrix():
    """Offers user a choice of outputs for caches matching the D/T matrix"""
    #TODO - change so choices return a list of caches which can then be exported from here? maybe?
    matrix = stats.calculateMatrix(caches)
    outputMatrix(matrix)
    choice = raw_input("Find caches in database not on matrix? 1)Full output 2)Mid output 3)Short output 4)HTML ")
    if choice == "Y" or choice == "y" or choice == "3":
        searchMatrix(matrix, 3)
    elif choice == "2":
        searchMatrix(matrix, 2)
    elif choice == "1":
        searchMatrix(matrix, 1)
    elif choice == "4":
        searchMatrix(matrix, 4)

def importGPX():
    """Gets filename from pickGPX() then reads in new caches and outputs useful info."""
    doc = pickGPX()

    if (doc != -1):
        print "Loading...."
        name = doc.getElementsByTagName("name")[0]
        description = doc.getElementsByTagName("desc")[0]
        timeCreated = doc.getElementsByTagName("time")[0]
        wpts = doc.getElementsByTagName("wpt")
        numWpts = len(wpts)

        if (getText(description.childNodes) != "Geocache file generated by Groundspeak"):
            print "NOT A VALID FILE"

        printHeader(name, timeCreated, numWpts)
        print len(caches), "before reading"
        readGPX(wpts, getText(timeCreated.childNodes))
        print len(caches), "after"
        
def outputCacheList():
    """Calls buildListOfGCID() to get caches, then outputs to an html file."""
    
    #build list of caches for output
    cacheList = buildListOfGCID()
    outFile = 'cacheOutput.html'
    initHTML(outFile)
    for cacheGCID in cacheList:
        for cache in caches:
            if cache.gcid == cacheGCID:
                exportHTML(cache, outFile, 2)
    showHTML(outFile)
    
def setFound(gcidList):
    """Sets caches in gcidList to found.
    
    Useful when a new stats query is unavailable.
    """
    for cache in caches:
        if cache.gcid in gcidList:
            cache.found = 1
            print cache.gcid, "is now set to found"
                        
def setFTF(gcidList):
    """Sets caches in gcidList to ftf.
    
    Necessary since geocaching.com does not track ftf.
    """
    for cache in caches:
        if cache.gcid in gcidList:
            cache.ftf = 1
            print cache.gcid, "is now set to ftf"
    
def buildListOfGCID():
    """Gets a list of gcids from the user and returns the list."""
    cacheList = []
    gcid = "y"
    while gcid != "n":
        gcid = raw_input("Please enter case-insensitive gcid without the gc prefix(n to stop): ")
        if (gcid != "n" and gcid != ""):
            cacheList.append("GC%s" %gcid.upper())
    return cacheList
        
def alterStatus():
    """Menu lets user change found or ftf status of a group of caches."""
    print "Please choose a task or any key to return to the main menu:"
    print "1) Set found status"
    print "2) Set ftf status"
    choice = raw_input("")
    actions = {"1": setFound, "2": setFTF}
    actions.get(choice, mainMenu)(buildListOfGCID())

def searchCachesCall():
    list = Search.searchCaches(caches)
    print len(list)

def preferencesMenu():
    act = 0
    while act != -1:
        print "Prefs menu"
        print "1) Set Home Location"
        print "Any other key to return to main menu"
        choice = raw_input("")
        actions = {"1": HomeLocation.setLocation}
        act = actions.get(choice, lambda: -1)()
    
def statsToConsoleCall():
    stats.statsToConsole(caches, homeLoc.homeLocation)

def mainMenu():
    """Main menu for geocachepython."""
    print ""
    print "Welcome to Alan's geocache database program"
    print "Version %s  --  You have %s caches in the database." % (VERSION, len(caches))
    if not homeLoc.hasLocation():
        print "\nYou have no home location set - Please enter one now: "
        homeLoc.setLocation()
    else:
        print "Please choose a task or any key to quit:"
        print "1) Import GPX/ZIP"
        print "3) XX Search/Enter group of caches"
        print "4) Statistics"
        print "9) Preferences"
        print "0) DT Combo Matrix"
        print "Any other key to quit"
        choice = raw_input("")
        actions = {"1": importGPX, "9": preferencesMenu, "3": searchCachesCall, "4": statsToConsoleCall, "0": DTComboMatrix}
        return actions.get(choice, lambda: -1)()
        #print "1) Import GPX/ZIP"
        #print "2) Calculate DT Combo Matrix"
        #print "3) Alter found or FTF status"
        #TODO reinstate this
        #print "3) Display Cache Details"
        #print "4) Set home location"
        #print "5) Output Cache List in HTML"
        #print "6) Output CSV"
        #print "7) Stats"
        #print "8) 10 Closest Caches"
        #print "9) Debug/Output GPX to Garmin"   

#main
[homeLoc, caches] = loadDatabase()
menuChoice = mainMenu()
while menuChoice != -1:
    menuChoice = mainMenu()
saveDatabase()
