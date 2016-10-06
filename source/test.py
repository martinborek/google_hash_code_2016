from droneio import DroneInput, DroneOutput, DroneAction;
import droneio, os;

for fname in ["busy_day","redundancy","mother_of_all_warehouses"]:
#for fname in ["busy_day"]:
    #i = DroneInput("input/busy_day.in");
    #i = DroneInput("input/redundancy.in");
    i = DroneInput("input/"+fname+".in");
    
    o = DroneOutput();
    
    lastDrone = 0;
    prevw = 0;
    for w in range(0,i.numwarehouses):
        for h in i.warehouse[w].customerdistances:
            itemNo = 0;
            for d in range(lastDrone,i.numdrones):
            
                if itemNo >= len(i.house[h].itemsWanted):
                    
                    break;
                
                if i.drone[d].totalTime + 2*i.whhdist[w][h] + 4 > i.duration:
                    continue;
                
                item = i.house[h].itemsWanted[itemNo];
                
                i.house[h].itemsWanted[itemNo] = -1;
                
                itemNo += 1;
                
                if item == -1:
                    continue;
                if i.warehouse[w].inventory[itemNo] == 0:
                    continue;
                
                i.warehouse[w].inventory[itemNo] -= 1;
                
                
                i.drone[d].totalTime +=  2*i.whhdist[w][h] + 4;
                    
                o.addAction(DroneAction(d,"L",w,item,1));
                o.addAction(DroneAction(d,"D",h,item,1));
                lastDrone = d;
            
        
            if lastDrone == i.numdrones-1:
                lastDrone = 0;
        prevw = w;
    
    o.output("testout/"+fname+".out");
