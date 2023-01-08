#Project: C950 WGU Delivery Algorithm Program
#Author: Andre Simmons
#Student ID: 009101703

import datetime
import csv
from HashTable import HashTable
from Packages import Package
from Truck import Truck

#imported addresses from csv file and stored in an empty list
#used Youtube link provided by the course instructor as a reference
addresses = []
with open('Addresses.csv') as address_csvfile:
    addressCSV = csv.reader(address_csvfile, delimiter = ',')
    for row in addressCSV:
        addresses.append(row)

        
#imported distance values from csv file and stored in an empty list
#used Youtube link provided by the course instructor as a reference
with open('Distances.csv') as distance_csvfile:
    distanceCSV_list = csv.reader(distance_csvfile, delimiter = ',')
    distanceCSV_list = list(distanceCSV_list)
    
#imported all package data from csv and stored in the hash table
#used the add function from hash table to add data
#assigned each row to a specific attribute from each package
packages = HashTable()
with open('WGUPS Package File.csv') as package_csvfile:
    packageCSV = csv.reader(package_csvfile, delimiter = ',')
    for row in packageCSV:
        Id = int(row[0])
        address = row[1]
        city = row[2]
        state = row[3]
        postal_code = row[4]
        deadline = row[5]
        mass = row[6]
        status = "At Delivery Hub"
        package = Package(Id, address, city, state, postal_code, deadline, mass, status)
        packages.add(Id, package)

#function that returns the id of an inputed address
#matches the address input with an address from the address list created from the csv
#inspired by this reddit post: https://www.reddit.com/r/WGU_CompSci/comments/x20bko/how_to_complete_c950_the_easy_wayespecially_if/
def get_address_id(address_input):
    for row in addresses:
        if address_input == row[2]:
            return int(row[0])

#function that returns the distance value based on the x/y coordinates in the distance adjacency list from csv
#the x/y coordinates will be the address ID found in a seperate function
#if there's a blank space, the function flips the 2 input values
#aided by meeting with course instructor
def distance_between_addresses(address_id1, address_id2):
    distance_value = distanceCSV_list[address_id1][address_id2]
    if distance_value != '':
        distance_value = distanceCSV_list[address_id1][address_id2]
    else:
        distance_value = distanceCSV_list[address_id2][address_id1]
    return float(distance_value)






#creating the 3 truck objects
truck1 = Truck(1)
truck2 = Truck(2)
truck3 = Truck(3)

#using a for loop to add packages with the listed id's into the truck's package set
#this method represents loading each truck
#uses add function from the 'Truck' class
for row in [1,13,14,15,16,19,20,29,30,31,34,37,40]:
    truck1.add(packages.get(row))

for row in [3,9,12,17,18,21,22,23,24,26,27,35,36,38,39]:
    truck2.add(packages.get(row))

for row in [6,2,4,5,7,8,10,11,25,28,32,33]:
    truck3.add(packages.get(row))

#set the departure time and current time to specific times based on the packages
#truck 1 will leave the earliest at 8 which will help account for certain package deadlines
#truck 2 will leave at 10:20 due to the address issue with package 9. All other packages do not have a deadline
#truck 3 will leave at 9:05 to account for the delayed packages
truck1.time_of_leaving = datetime.timedelta(hours = 8)
truck1.current_time = datetime.timedelta(hours = 8)
truck2.time_of_leaving = datetime.timedelta(hours = 10, minutes = 20)
truck2.current_time = datetime.timedelta(hours = 10, minutes = 20)
truck3.time_of_leaving = datetime.timedelta(hours = 9, minutes = 5)
truck3.current_time = datetime.timedelta(hours = 9, minutes = 5)


#implementation of the nearest neighbor algorithm
#accepts a truck object
#aided by meeting with course instructor
def delivery_algorithm(truck):
    #assigns truck id to package. Used later when displaying package info at a given time
    for package in truck.package_set:
        package.truck_id = truck.truckId

    #ensures that the algorithm runs until there are no packages left to deliver (when truck's package set has 0 elements)
    while len(truck.package_set) > 0:
        #truck is En Route as it's delivering packages
        truck.status = "En Route"
        #set minimum distance to a high value initially
        min_distance = 1000000
        #represents the upcoming package that will be delivered next
        upcoming_package = None
        #loops through the packages in the truck's package set
        for package in truck.package_set:
            #uses the distance function to find the distance value given the id of the truck's address and the id of the package's address
            #if that value is less than the minimum distance from before, that value becomes the new minimum distance
            #the upcoming package now becomes that specific package
            if distance_between_addresses(get_address_id(truck.current_address), get_address_id(package.address)) <= min_distance:
                min_distance = distance_between_addresses(get_address_id(truck.current_address), get_address_id(package.address))
                upcoming_package = package
                
        #the upcoming package is removed from the truck's package set since it was delivered
        truck.package_set.remove(upcoming_package)
        #the truck's mileage is incremented by the value of the minimum distance
        truck.miles_traveled += min_distance
        #the trucks address is set to the upcoming package's address
        truck.current_address = upcoming_package.address
        #the truck's time is incremented by the value of the minimum distance divided by 18 (truck's speed of 18 mph)
        #converted to hours since miles/mph = hours
        truck.current_time += datetime.timedelta(hours = min_distance/18)
        #departure time of the package is set to the truck's departure time
        upcoming_package.time_of_departure = truck.time_of_leaving
        #delivery time of the package is set to the current time of the truck
        upcoming_package.time_of_delivery = truck.current_time

    #truck finishes it's route once all packages have been delivered
    truck.status = "Route Finished"
        
#runs the nearest neighbor delivery algorithm for each truck
delivery_algorithm(truck1)
delivery_algorithm(truck2)
#runs the algorithm only if truck 1 or truck 2 has finished their route due to there only being 2 drivers
if truck1.status == "Route Finished" or truck2.status == "Route Finished":
    delivery_algorithm(truck3)

#calculates the total mileage by adding the mileage of each truck together
total_combined_mileage = truck1.miles_traveled + truck2.miles_traveled + truck3.miles_traveled

#User Interface
print("------------------------------------------------")
print("                      WGUPS                     ")
print("------------------------------------------------")
#displays the total mileage
print("\n\nThe total mileage for all 3 trucks is " + str(total_combined_mileage) + " miles\n\n")
#asks the user to select an option whether to display all package statuses or an individual package status
menu_input = input("Press 1 to get the status of all packages at a given time \n OR \nPress 2 to get the status of an individual package: ")
#if user inputs "1", interface prompts user to select a time
if menu_input == "1":
    hour_input = input("Please enter an hour value between 0 and 23: ")
    if int(hour_input) >= 0 and int(hour_input) <24:
        minute_input = input("Please enter a minute value between 0 and 59: ")
        if int(minute_input) >= 0 and int(minute_input) < 60:
            #creates time input based on hour and minute values
            time_input = datetime.timedelta(hours = int(hour_input), minutes = int(minute_input))
        #validates minute value input
        else:
            print("Invalid minute value entered.  This program will now close")
            exit()
    #checks if valid hour value entered
    else:
        print("Invalid hour value entered.  This program will now close")
        exit()

    #loops through all packages, gets the package info based on package id        
    for row in range(1,41):
        package = packages.get(row)
        #updates the package status based on the time input, uses function from package class
        package.get_package_status(time_input)
        #displays the original address for package 9 if input time is before 10:20
        #displays the corrected address if input time is after 10:20
        special_time = datetime.timedelta(hours = 10, minutes = 20)
        if package.package_id == 9 and time_input > special_time:
            package.address = "410 S State St"
        else:
            package.address = "300 State St"
        #displays all attributes required for each package
        print("Package ID: " + str(package.package_id))
        print("Truck ID: " + str(package.truck_id))
        print("Address: " + package.address)
        print("Deadline: " + package.delivery_deadline)
        print("City: " + package.city)
        print("Zip Code: " + package.zipcode)
        print("Weight: " + package.mass)
        print("Departure Time: " + str(package.time_of_departure))
        print("Status: " + package.status)
        #only shows a delivery time if the package was in fact delivered
        if package.status == "Delivered":
            print("Delivery Time: " + str(package.time_of_delivery) + "\n\n")
        else:
            print("\n\n")

#if the user inputs "2" the interface prompts the user to input a time and input a package id
elif menu_input == "2":
    hour_input = input("Please enter an hour value between 0 and 23: ")
    #checks if valid hour value entered
    if int(hour_input) >= 0 and int(hour_input) <24:
        minute_input = input("Please enter a minute value between 0 and 59: ")
        #checks if valid minute value entered
        if int(minute_input) >= 0 and int(minute_input) < 60:
            #creates time input based on hour and minute values
            time_input = datetime.timedelta(hours = int(hour_input), minutes = int(minute_input))
        #displays error message and quits program if invalid minute value entered
        else:
            print("Invalid minute value entered.  This program will now close")
            exit()
            
    #displays error message and quits program if invalid hour value entered
    else:
        print("Invalid hour value entered.  This program will now close")
        exit()
        
    #prompts user to input package id between 1 and 40
    package_id_input = input("Please enter a package id number between 1 and 40: ")

    #checks if valid package id was entered
    if int(package_id_input) >= 1 and int(package_id_input) <= 40:
        #grabs package from hashtable based on the id inputed by the user
        package = packages.get(int(package_id_input))
        #updates package status based on the time input
        package.get_package_status(time_input)
        #displays the original address for package 9 if input time is before 10:20
        #displays the corrected address if input time is after 10:20
        special_time = datetime.timedelta(hours = 10, minutes = 20)
        if package.package_id == 9 and time_input > special_time:
            package.address = "410 S State St"
        else:
            package.address = "300 State St"
        #displays all attributes required for each package
        print("Package ID: " + str(package.package_id))
        print("Truck ID: " + str(package.truck_id))
        print("Address: " + package.address)
        print("Deadline: " + package.delivery_deadline)
        print("City: " + package.city)
        print("Zip Code: " + package.zipcode)
        print("Weight: " + package.mass)
        print("Departure Time: " + str(package.time_of_departure))
        print("Status: " + package.status)
        #only shows a delivery time if the package was in fact delivered
        if package.status == "Delivered":
            print("Delivery Time: " + str(package.time_of_delivery) + "\n\n")
        else:
            print("\n\n")

    else:
        print("Invalid id value entered.  This program will now close")
        exit()

#checks if valid value entered 
else:
    print("Invalid value entered.  This program will now close")
    exit()
            
        
    
        
    


        
    
    

    
    


        



    
    
