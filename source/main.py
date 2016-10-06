'''
Created on Feb 11, 2016

@author: Martin Borek, Miguel Gordo
'''
from droneio import DroneInput, DroneOutput, DroneAction;
import math

#entities
#import numpy as np
#from entities import Customer

#fname = "busy_day"
TRY_CLOSE = 5
for fname in ["redundancy"]:
#for fname in ["busy_day","redundancy","mother_of_all_warehouses"]:
    alldata = DroneInput("input/"+ fname + ".in")
    
    
    
    o = DroneOutput();
    #SIMULATION
    
    # for each warehouse, count how many customers (houses) have it as the closest warehouse ~ numCusomters
    # based on this information, compute how many drones should be assigned to this warehouse at the beginning (proportionally) ~ numDrones
    availableDrones = alldata.numdrones
    for warehouse in xrange(0, alldata.numwarehouses, 1):
        for x in xrange(0, alldata.numhouses, 1):
            if  alldata.house[x].closestWarehouse == warehouse:
                alldata.warehouse[warehouse].numCustomers += 1
        
        alldata.warehouse[warehouse].numDrones = math.floor(alldata.warehouse[warehouse].numCustomers*alldata.numdrones/alldata.numhouses)
        availableDrones-=alldata.warehouse[warehouse].numDrones
    
    # some drones might be still unassigned because of using the function "floor";
    # todo: assign these drones to the warehouse with the "closest" customers (min of average distance warehouse->customer)    
    while availableDrones > 0:
        alldata.warehouse[0].numDrones += 1
        availableDrones -= 1
    
    # assign all drones to their initial warehouse
    #assignedDrones = 0 # not used      
    for drone in xrange(0, alldata.numdrones, 1):
        print "drone " + str(drone)
        #assigned = False
        for warehouse in xrange(0, alldata.numwarehouses, 1):
            if alldata.warehouse[warehouse].numDronesOperating < alldata.warehouse[warehouse].numDrones:
                alldata.drone[drone].warehouseAssigned = warehouse
                alldata.warehouse[warehouse].numDronesOperating += 1 
                print "warehouse assigned" + str(alldata.drone[drone].warehouseAssigned)
                #o.addAction(DroneAction(drone,"L",warehouse,productType,amount))
                #o.addAction(DroneAction(drone,"D",order,productType,amount))            
                
                #load operation -- BEGIN          
                #load items -- BEGIN
                successfulLoad = False
                carring = {}
                closestNumSet = False
                
                for order in alldata.warehouse[warehouse].customerdistances:
                    carringOrder = {}
                    
                    itemNo = -1
                    
                    while True: #load all stuff you can carry for one order -- BEGIN
                        itemNo += 1
                        
                        if itemNo >= len(alldata.house[order].itemsWanted):
                            break
                        
                        #wantedAmount = alldata.house[order].itemsWanted[itemNo]
                        productNumber = alldata.house[order].itemsWanted[itemNo]
                        wantedAmount = 1 #todo:amount
                        
                        if productNumber == -1:
                            continue
                        
                        tryNum = min(alldata.warehouse[warehouse].inventory[productNumber], wantedAmount)                   
                        
                        while tryNum > 0:
                            result = alldata.drone[drone].load(productNumber, alldata.productweights[productNumber], tryNum, alldata.warehouse[warehouse])
                            if result:
                                successfulLoad = True
                                carringOrder[productNumber] = tryNum
                                alldata.house[order].itemsWanted[itemNo] = -1 # ~ item sent for delivery
                                alldata.warehouse[warehouse].inventory[productNumber] -= 1
                                carring[order] = carringOrder # TODO: shallow / deep copy?
                                closestNum = 0
                                closestNumSet = True
                                break #try taking more things from the same order
                            else:
                                #print tryNum
                                #print "fail"
                                tryNum -= 1
                            
                    #load all stuff you can carry for one order -- END
                    if closestNumSet:
                        closestNum += 1
                        if closestNum > TRY_CLOSE:
                            break
                    
                if successfulLoad:
                    #alldata.drone[drone].deliverAll(alldata.house[order])
                    for carOrder in carring:
                        alldata.drone[drone].deliverAll(alldata.house[carOrder])
                    # check if the planned operation does not exceed the simulation time; if not, log these commands
                    if alldata.drone[drone].totalTime <= alldata.duration:
                        for carOrder in carring:        
                            for loadItem in carring[carOrder]:                  
                                o.addAction(DroneAction(drone,"L", warehouse, loadItem, carring[carOrder][loadItem]))
                                
                        for carOrder in carring:        
                            for loadItem in carring[carOrder]:                     
                                o.addAction(DroneAction(drone,"D", carOrder, loadItem, carring[carOrder][loadItem]))                      
                    break
                    
                #load items -- END
                
                
                if not successfulLoad: # no items to bring from this warehouse, move drone to another warehouse
                    alldata.drone[drone].warehouseAssigned = (alldata.drone[drone].warehouseAssigned + 1) % alldata.numwarehouses
                
                #load operation -- END
                break
                
            else: # this warehouse has enough of assigned drones
                continue           
                            
                            
                           
                       
    '''
    This is already handled when counting how many drones to assign to each warehouse
        
                assignedDrones += 1 # not used
                assigned = True
                break
        if not assigned:
            alldata.drone[drone].warehouseAssigned = warehouse # TODO
            
            
            
            for customer in alldata.warehouse[warehouse].customers:
                for item in alldata.customer[customer].itemsWanted:
                        
                    if alldata.warehouse[warehouse].inventory[item] > 0:
                        while True:
                            tryNum = np.min(alldata.warehouse[warehouse].inventory[item], alldata.customers[customer].itemsWanted[item])
                               
                            try:
                                alldata.drone[drone].load(alldata.product[item], tryNum)
                                o.addAction(DroneAction(drone, "L", warehouse, item, tryNum))
                                break
                            except:
                                tryNum -= 1
                                if tryNum == 0:
                                    break
                                continue
            
    '''            
            
        
    # main algorithm for the simulation
    #for turn in xrange(1, alldata.duration, 1):
    duration = min (17200, alldata.duration)
    for turn in xrange(1, duration, 1):
        #print turn
        
        for drone in xrange(0, alldata.numdrones, 1):
            '''
            if alldata.drone[drone].busyTime:
                print "busy"
                alldata.drone[drone].busyTime -= 1
                continue
            '''
            if alldata.drone[drone].totalTime > turn:
                #print "busy"
                continue
            
            else:
#                print "not busy"
                #print alldata.drone[drone].totalTime
                warehouse = alldata.drone[drone].warehouseAssigned
                alldata.drone[drone].busyTime = 0
                
                successfulLoad = False
                carring = {}
                closestNumSet = False
                
                for order in alldata.warehouse[warehouse].customerdistances:
                    carringOrder = {}
                    
                    itemNo = -1
                    
                    while True: #load all stuff you can carry for one order -- BEGIN
                        itemNo += 1
                        
                        if itemNo >= len(alldata.house[order].itemsWanted):
                            break
                        
                        #wantedAmount = alldata.house[order].itemsWanted[itemNo]
                        productNumber = alldata.house[order].itemsWanted[itemNo]
                        wantedAmount = 1 #todo:amount
                        
                        if productNumber == -1:
                            continue
                        
                        tryNum = min(alldata.warehouse[warehouse].inventory[productNumber], wantedAmount)                   
                        
                        while tryNum > 0:
                            result = alldata.drone[drone].load(productNumber, alldata.productweights[productNumber], tryNum, alldata.warehouse[warehouse])
                            if result:
                                successfulLoad = True
                                carringOrder[productNumber] = tryNum
                                alldata.house[order].itemsWanted[itemNo] = -1 # ~ item sent for delivery
                                alldata.warehouse[warehouse].inventory[productNumber] -= 1
                                carring[order] = carringOrder # TODO: shallow / deep copy?
                                closestNum = 0
                                closestNumSet = True
                                break #try taking more things from the same order
                            else:
                                #print tryNum
                                #print "fail"
                                tryNum -= 1
                            
                    #load all stuff you can carry for one order -- END
                    if closestNumSet:
                        closestNum += 1
                        if closestNum > TRY_CLOSE:
                            break
                    
                if successfulLoad:
                    #alldata.drone[drone].deliverAll(alldata.house[order])
                    for carOrder in carring:
                        alldata.drone[drone].deliverAll(alldata.house[carOrder])
                    # check if the planned operation does not exceed the simulation time; if not, log these commands
                    if alldata.drone[drone].totalTime <= alldata.duration:
                        for carOrder in carring:        
                            for loadItem in carring[carOrder]:                  
                                o.addAction(DroneAction(drone,"L", warehouse, loadItem, carring[carOrder][loadItem]))
                                
                        for carOrder in carring:        
                            for loadItem in carring[carOrder]:                     
                                o.addAction(DroneAction(drone,"D", carOrder, loadItem, carring[carOrder][loadItem]))                      
                    break
                    
                #load items -- END
                
                
                if not successfulLoad: # no items to bring from this warehouse, move drone to another warehouse
                    print turn
                    #print "changing warehouse from " + str(alldata.drone[drone].warehouseAssigned)
                    alldata.drone[drone].warehouseAssigned = (alldata.drone[drone].warehouseAssigned + 1) % alldata.numwarehouses
                    #print "...to " + str(alldata.drone[drone].warehouseAssigned)
                
                #load operation -- END
            
    
    
    o.output("testout/"+fname+".out");
    
