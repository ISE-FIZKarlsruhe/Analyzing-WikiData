#v1.3
import csv
from collections import defaultdict
from sys import stdout
import numpy as np

#Information need parameter
start = 700             #define the start node
goal = 2                #define the goal node
maxPathlength = 3       #define the maximal pathlength

#Action parameter
rebuildDict = False      #Specifies wheather or not the dictionary should be rebuild (Has to be set to True for the first run only)
followAllPaths = True   #if True returns all paths from start to X below the set maxPathlength (default: False)
aggregatePaths = False
completePaths = True     #if True it only prints the pathlength to any "seen" node (default: False)
verbose = True           #set to False to disable to progress percentage and to slightly improve performance (default: True)

#initialisation
mainlist = [[start]]
found = False
seen = defaultdict(int)
seen[start] = 0
currentLength = 0
fileextra = "_lengths" if (not completePaths) else ""
outputfile = "output_len%d_Q%d%s" %(maxPathlength,start,fileextra)    

def aggregatepathlengths(obj):
    print("\nNew objects reached per pathlength from entity",start)
    a = np.zeros(maxPathlength+1) 
    for k, v in sorted(obj.items()):
       a[v] += 1
    for i, v in enumerate(a):
        print(i,str(int(v)),sep='; ')
        
#function to print the main list and the dictionary in a nice way
def printplus(obj):
    # Dictionary
    if isinstance(obj, __builtins__.dict):
        maxkey = max(obj, key=int)
        j = 0
        print("\nPrinting dictionary of reached nodes to file",outputfile)
        for k, v in sorted(obj.items()):
            with open(outputfile, "a") as f:
                f.write("\n"+u'{0}: {1}'.format(k, v))
            if (verbose):
                print(str(j))
                if (k == maxkey):
                    j = 100
                if (k >= maxkey*j/100):
                    stdout.write("\r%d" %j+"%")
                    stdout.flush()
                    j = j+1             
    # List         
    elif isinstance(obj, __builtins__.list):
        j = 0
        print("\nPrinting list of full paths to file",outputfile)
        for i,x in enumerate(obj):
            with open(outputfile, "a") as f:
                f.write("\n"+str(x))
            if (verbose):
                if (i >= (len(obj)-1)*j/100):
                    stdout.write("\r%d" %j+"%")
                    stdout.flush()
                    j=j+1
    
#read csv file and build the dictionary
if (rebuildDict):
    dictionary = defaultdict(list);
    i = 0;              
    with open('wikidata_objects-only.csv', newline ='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        print("Buildung up the main dictionary", end=" ")  
        for key, value in reader:
            dictionary[int(key)].append(int(value))
            i = i+1;
            if (i % 3100000 == 0):
                print(".", end=" ")
        print("\nDictionary built successfully!\n")

#throws error when dictionary was not initialized
if (not rebuildDict and dictionary == None):
    print("Error: No dictionary found. Set 'rebuildDict' to 'True'")
    quit()        
    
#iterate over each path in the main list
for p in mainlist:      
    #...until pathlength is greater than 5 or the goal has been found, main is countinously increased
    if len(p) <= maxPathlength and found == False:
        if len(p) != currentLength:
            currentLength = len(p);
            if(verbose):
                print("Checking paths of length =",currentLength)  
        #define the currently viewed node as s
        s = p[len(p)-1]
        #Check if the reached node appears in our dictionary - only if it does, proceed
        if dictionary.get(s) != None:
            #get all immediately connected objects from s from the dictionary
            for o in dictionary.get(s):
                if found == False:
                    #check if the object has ben seen before (i.e. ther eis a shorter path to this o)                  
                    if seen.get(o) == None:
                        #add the new object's full path to the main list 
                        seen[o] = len(p)
                        x = list(p);
                        x.append(o);
                        mainlist.append(x)
                    if (not followAllPaths):
                        if o == goal:
                            found = True 
                            print("Full path from node ", start," to node ",goal,":\n",x,sep='')

#calls the method to print to file
if (followAllPaths):
    if(aggregatePaths):
        aggregatepathlengths(seen)
    else:    
        if(completePaths):
            m = "All Paths (maxLength = "+str(maxPathlength)+") from "+str(start)+" to X:"
            with open(outputfile, "a") as f:
                f.write(str(m))
            printplus(mainlist)
        m = "\nPathlengths (maxLength = "+str(maxPathlength)+") from "+str(start)+" to X:"
        with open(outputfile, "a") as f:
            f.write("\n")
            f.write(str(m))
        printplus(seen)
    
    
