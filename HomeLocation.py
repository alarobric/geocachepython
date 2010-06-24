#homeLocation
from utility import DMToDD

class HomeLocation():
    def __init__(self):
        """Init homeLocation"""
        self.homeName = []
        self.homeLocation = []
        
    def setLocation(self):
        """Set new home location, reorder the list or remove locations."""
        #global homeName, homeLocation
        print "Current home locations:"
        for i in range(len(self.homeName)):
            print "  %s) %s %s" % (i, self.homeName[i], self.homeLocation[i])
        choice = raw_input("Please select \"n\" for a new location, \"s\" to set the current home location, or \"d\" to delete a location: ")
        actions = {"n": self.enterNewLocation, "s": self.setCurrentLocation, "d": self.deleteLocation}
        actions.get(choice, self.noLocationChoice)()
        
    def enterNewLocation(self):
        """Enter a new home location."""
        name = raw_input("Enter name for new location (enter for default of Kingston): ")
        if len(name) == 0:
            print "Setting default location of Kingston"
            self.homeName.append("Kingston, ON")
            self.homeLocation.append(DMToDD("N 44 13.573 W 076 29.090"))
        else:
            coords = raw_input("Enter new location coords in 'N 49 00.000 W 079 00.000' format: ")
            coords = DMToDD(coords)
            if coords != -1:
                coords = util.parse_geo(coords)
            #needs error checking
            print "Confirm new location? ", name, coords,
            choice = raw_input("")
            if choice == "y" or choice == "Y":
                self.homeName.append(name)
                self.homeLocation.append(coords)
                
    def setCurrentLocation(self):
        """Reorder the list of current locations to set a new home."""
        print "set main location"
        choice = raw_input("Enter number of location to promote: ")
        if choice == str(int(choice)) and int(choice) >= 0 and int(choice) < len(self.homeName):
            self.homeName.insert(0, self.homeName.pop(int(choice)))
            self.homeLocation.insert(0, self.homeLocation.pop(int(choice)))

    def deleteLocation(self):
        """Delete a location."""
        try:
            choice = raw_input("Enter number of location to delete: ")
            if choice == str(int(choice)) and int(choice) >= 0 and int(choice) < len(self.homeName):
                print "Record removed: ", self.homeName.pop(int(choice)), self.homeLocation.pop(int(choice))
            else:
                print "Invalid choice"
        except ValueError:
            print "Invalid choice"
            
    def noLocationChoice(self):
        """If no valid choice from location menu."""
        print "Invalid choice."

    def hasLocation(self):
        """Returns true if there is at least one location."""
        if len(self.homeName) > 0 and len(self.homeLocation) > 0:
            return 1
        return 0

if __name__ == "__main__":
    print "Doesn't do anything when run as script"
