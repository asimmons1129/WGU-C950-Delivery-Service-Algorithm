#Project: C950 WGU Delivery Algorithm Program
#Author: Andre Simmons
#Student ID: 009101703

            
#HashTable class
#Inspired by the "Python: Creating a HASHMAP using Lists" Youtube video
#Video link was provided by the course instructor as a guide in the welcome email
class HashTable:

    #constructor for the hashtable
    def __init__(self):
        self.size = 20
        self.map = [None] * self.size

    #gets the hash 
    def _get_hash(self, key):
        hash = 0
        for char in str(key):
            hash+= ord(char)
        return hash % self.size

    #adds values to the hash table
    #used when adding packages to the hashtable
    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]
        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
                self.map[key_hash].append(key_value)
                return True

    #lookup function
    #used for looking up a specific item in hash table
    def get(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if key == pair[0]:
                    return pair[1]
        return None

    #deletes an item from the data structure
    def delete(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is None:
            return False
        for i in range (0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

    #print function that will print all items in data structure
    def print(self):
        print('---PACKAGES----')
        for item in self.map:
            if item is not None:
                print(str(item))
