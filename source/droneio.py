import Queue;
import entities;
import math, os;

debug = True;

class DroneInput:
    def __init__(self, filename):
        f = open(filename, 'r');
        
        line = f.readline();
        print line;
        
        values = line.split(' ');
        self.rows = int(values[0]);
        self.columns = int(values[1]);
        self.numdrones = int(values[2]);
        self.duration = int(values[3]);
        self.maxpayload = int(values[4]);
        
        if debug:
            print " Rows:", self.rows, " Columns:", self.columns, " Drones:", self.numdrones, " Maxpayload:", self.maxpayload;
        
        self.numproducts = eval(f.readline());
        
        if debug:
            print " Numproducts:", self.numproducts;
        
        
        line = f.readline();
        inventory = line.split(' ');
        self.productweights = [];
        for y in range(0,len(inventory)):
            self.productweights.append(int(inventory[y]));
            
        if debug:
            print self.productweights;
            
        
        
        
        #parse warehouses and instantiate       
        self.numwarehouses = eval(f.readline());
        if debug:
            print " Numwarehouses:", self.numwarehouses;
        self.warehouse = [];
        for x in range(0,self.numwarehouses): 
            line = f.readline();
            values = line.split(' ');
            line = f.readline();
            inventory = line.split(' ');
            for y in range(0,len(inventory)):
                inventory[y] = int(inventory[y]);
            self.warehouse.append(entities.Warehouse(int(values[0]),int(values[1]),inventory));
            
        
        #parse houses and instantiate
        self.numhouses = eval(f.readline());
        if debug:
            print " Numhouses:", self.numhouses;
        self.house=[];
        for x in range(0,self.numhouses): 
            line = f.readline();
            values = line.split(' ');
            numwitems = eval(f.readline());
            line = f.readline();
            inventory = line.split(' ');
            for y in range(0,len(inventory)):
                inventory[y] = int(inventory[y]);
            #add new house;
            self.house.append(entities.Customer(inventory, int(values[0]), int(values[1]), 0));


        # warehouse - house distances
        self.whhdist = {};
        for x in range(0,len(self.warehouse)):
            self.whhdist[x] = {};
            for y in range(0,len(self.house)):
                self.whhdist[x][y] = math.sqrt(math.pow(float(self.warehouse[x].locationX)-float(self.house[y].locationX),2) + math.pow(float(self.warehouse[x].locationY)-float(self.house[y].locationY),2));
                #print x,y,float(self.warehouse[x].locationX),float(self.warehouse[x].locationY),float(self.house[y].locationX),float(self.house[y].locationY),self.whhdist[x][y];
        
        # warehouse - warehouse distances
        self.whwhdist = {};
        for x in range(0,len(self.warehouse)):
            self.whwhdist[x] = {};
            for y in range(0, len(self.warehouse)):
                self.whwhdist[x][y] = math.sqrt(math.pow(float(self.warehouse[x].locationX)-float(self.warehouse[y].locationX),2) + math.pow(float(self.warehouse[x].locationY)-float(self.warehouse[y].locationY),2));
        
        for x in range(0,len(self.warehouse)):
             self.warehouse[x].customerdistances = sorted(self.whhdist[x], key=self.whhdist[x].__getitem__);
             
        
        #find closest warehouse for each house
        for x in range(0,self.numhouses):
            
            min = math.hypot(self.rows, self.columns);
            mini = -1;
            for y in range(0, len(self.warehouse)):
                
                if self.whhdist[y][x] < min:
                    min = self.whhdist[y][x];
                    mini = y;
            
            self.house[x].closestWarehouse = mini;
            
        self.drone = [];
        for x in range(0,self.numdrones):
            self.drone.append(entities.Drone(self.maxpayload,[]));
            
        
        
            
            

class DroneOutput:
    def __init__(self):
        self.q = Queue.Queue();
    
    def addAction(self,action):
        self.q.put(action);
    
    def output(self, filename):
        f = open(filename, 'w');
        f.write(str(self.q.qsize())+"\n");
        while not self.q.empty():
            f.write(str(self.q.get())+"\n")
        
class DroneAction:
    def __init__(self, drone, movetype, product, numproduct, house, time = 0):
        self.drone = drone;
        self.movetype = movetype;
        self.product = product;
        self.numproduct = numproduct;
        self.house = house;
        if movetype.__eq__("W"):
            self.time = time;
    
    def __str__(self):
        if self.movetype.__eq__("W"):
            return str(self.drone)+" "+str(self.movetype)+" "+str(self.time);
        else:
            return str(self.drone)+" "+str(self.movetype)+" "+str(self.product)+" "+str(self.numproduct)+" "+str(self.house);
            