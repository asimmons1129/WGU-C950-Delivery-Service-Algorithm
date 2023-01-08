#Project: C950 WGU Delivery Algorithm Program
#Author: Andre Simmons
#Student ID: 009101703

import datetime

#class to create a Truck object
class Truck:
    #constructor for truck class
    #uses a truck id as parameter
    #has a set to store packages
    #initializes address to the hub
    #sets the packages loaded to 0
    #sets the speed of truck to 18 since it's given that it's 18 mph
    #has an attribute for the time of departure and current time
    #initializes status to At Delivery Hub
    #has miles traveled initialized to 0
    def __init__(self, truckId):
        self.truckId = truckId
        self.package_set = set()
        self.current_address = "4001 South 700 East"
        self.packages_loaded = 0
        self.average_speed = 18
        self.time_of_leaving = datetime.timedelta()
        self.current_time = datetime.timedelta()
        self.miles_traveled = float(0)
        self.status = "At Delivery Hub"

    
    #function to add package to the packages set
    #used when loading truck
    def add(self, package):
        #loads truck only up to the limit of 16 packages
        if self.packages_loaded <= 16:
            self.package_set.add(package)
            self.packages_loaded += 1
        #prints message if the maximum has been reached
        else:
            print('The maximum amount of packages has been loaded onto the truck')
        
