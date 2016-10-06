#import numpy as np
import math

class Drone:  
    
    def __init__(self, maxWeight, inventory):
        self.maxWeight = maxWeight
        self.inventory = inventory
        self.currentLocationX = 0;
        self.currentLocationY = 0;
        self.busyTime = 0
        self.unloadingTime = 0 # used to compute the time neaded for "unloading"
        self.totalTime = 0
        self.currentWeight = 0
        self.warehouseAssigned = 0
        self.delivering  = False
        
    def load(self,item,itemWeight,amount,warehouse):
        #print "amount " + str(amount)
        #print "itemWeight " + str(itemWeight)
        #print "currentWeight " + str(self.currentWeight)
        #print "maxWeight " + str(self.maxWeight)
        if (itemWeight*amount+self.currentWeight) > self.maxWeight:
            #raise Exception("Too much weight")
            return False
        
        #self.inventory[item]+=amount
        if self.busyTime == 0:
            self.busyTime = math.ceil(math.sqrt((self.currentLocationX - warehouse.locationX)**2 + (self.currentLocationY - warehouse.locationY)**2))
            self.totalTime += self.busyTime
        
        self.busyTime += 1 # loading = for each product one time unit
        self.totalTime += 1
        
        self.unloadingTime += 1
            
        self.currentWeight += itemWeight*amount
        #print "newCurrentWeight" + str(self.currentWeight)        
        
        #self.busyTime = np.ceil(np.sqrt(np.abs(self.currentLocationX - warehouse.locationX)^2 + np.abs(self.currentLocationY - warehouse.locationY)^2))
        warehouse.removeItems(item,amount) #todo: check if working
        self.currentLocationX = warehouse.locationX
        self.currentLocationY = warehouse.locationY
        #self.delivering = False
        return True
        
    def deliverAll(self, customer):
        addTime = math.ceil(math.sqrt((self.currentLocationX - customer.locationX)**2 + (self.currentLocationY - customer.locationY)**2))
        addTime += self.unloadingTime
        self.unloadingTime = 0
        
        self.busyTime += addTime
        self.totalTime += addTime
        
        self.currentLocationX = customer.locationX
        self.currentLocationY = customer.locationY
        self.currentWeight = 0
             
   
    def deliver(self, item, amount, customer):
        
        if(item not in self.inventory):
            raise Exception("Products were not in inventory")
        
        self.inventory[item]-=amount
        #customer
        self.busyTime = math.ceil(math.sqrt(abs(self.currentLocationX - customer.locationX)^2 + abs(self.currentLocationY - customer.locationY)^2))
        customer.removeFromOrder(item,amount)
        self.currentLocationX = customer.locationX
        self.currentLocationY = customer.locationY
        self.delivering = True
        
    '''
    def unload(self,item,amount):
        if(item not in self.inventory):
            raise Exception("Products were not in inventory")
        
        self.inventory[item]-=amount 


    
    def wait(self,turns):
        
        self.busyTime = turns
    '''

class Warehouse:
    
    def __init__(self, locationX, locationY, inventory = {}):
        self.locationX = locationX
        self.locationY = locationY
        self.inventory = inventory
        self.numCustomers = 0
        self.numDrones = 0
        self.numDronesOperating = 0
        self.customers = []
        
    def receiveItems(self, productName, count):
        self.inventory[productName] += count        
    
    def removeItems(self, productName, count):
        self.inventory[productName] -= count
    

class Customer:
    
    def __init__(self, itemsWanted, locationX, locationY, closestWarehouse):
        self.itemsWanted = itemsWanted 
        self.locationX = locationX
        self.locationY = locationY
        self.closestWarehouse = closestWarehouse
    
#    def isOrderCompleted(self):
#        pass
    def removeItems(self,productName,count):
        self.itemsWanted[productName] -= count
        
    def addItems(self,productName,count):
        self.itemsWanted[productName]+=count
    
    

class Order:
    
    def __init__(self, customer):
        self.customer = customer
        self.inventory = []
    
    def addItem(self, product, count):
        newItem = Item(product, count)
        self.inventory.append(newItem)
    
class Item:
    
    def __init__(self, productName, weight):
        self.productName = productName
        self.weight = weight
        
    
    


    