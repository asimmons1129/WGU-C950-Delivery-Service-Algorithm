#Project: C950 WGU Delivery Algorithm Program
#Author: Andre Simmons
#Student ID: 009101703


#class used to create package object
class Package:
    #contstructor for package object
    #contains all attributes from the packages csv file
    def __init__(self, package_id, address, city, state, zipcode, delivery_deadline, mass, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_deadline = delivery_deadline
        self.mass = mass
        #used to get the status of package
        self.status = status
        #used to assign truck id to package
        #ensures that package is on the correct truck
        self.truck_id = None
        #used to get the time of departure for a package
        self.time_of_departure = None
        #used to get the time of delivery for a package
        self.time_of_delivery = None

    #function to set the status of a package based on a time input
    #course instructor suggested this method
    def get_package_status(self, time_input):
        #package is delivered if the input time is after the time of delivery
        if time_input > self.time_of_delivery:
            self.status = "Delivered"
        #package is en route if input time is after time of departure and before time of delivery
        elif time_input > self.time_of_departure and time_input < self.time_of_delivery:
            self.status = "En Route"
        #package is at the hub if any other time is inputed
        else:
            self.status = "At Delivery Hub"



    
