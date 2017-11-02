import csv
from collections import defaultdict

#Parameter
start = 1;              #define the start node
goal = 11452;           #define the goal node
maxPathlength = 10;      #define the maximal pathlength
searchAll = True;       #if True returns all paths from start to X below the maxPathlength (default: False)
outputfile = "output10"  #specify the name of the output file

#initialisation
main = [[start]];
found = False;
dictionary = defaultdict(list);
seen = defaultdict(int);
seen[start] = 0;
currentLength = 0;

#function to print the main list and the dictionary in a nice way
def printplus(obj):
    # Dictionary
    if isinstance(obj, dict):
        for k, v in sorted(obj.items()):
            with open(outputfile, "a") as f:
                f.write("\n"+u'{0}: {1}'.format(k, v))
    # List         
    elif isinstance(obj, list):
        for x in obj:
            with open(outputfile, "a") as f:
                f.write("\n"+str(x))

#read csv file and build the dictionary
with open('wikidata_objects-only.csv', newline ='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for key, value in reader:
        dictionary[int(key)].append(int(value))
        
#iterate over each path in the main list
for p in main:
    if len(p) != currentLength:
        currentLength = len(p);
        print("Checking paths of length = ",currentLength);        
    #...until pathlength is greater than 5 or the goal has been found, main is countinously increased
    if len(p) <= maxPathlength and found == False:
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
                        seen[o] = len(p);
                        x = list(p);
                        x.append(o);
                        main.append(x)
                    if searchAll == False:
                        if o == goal:
                            found = True; 
                            print("Full path from Node ", start," to Node ",goal,":\n",x,sep='')

if searchAll == True:
    #m = "All Paths (maxLength = "+str(maxPathlength)+") from "+str(start)+" to X:"
    #with open(outputfile, "a") as f:
    #    f.write(str(m))
    #printplus(main)
    m = "\nPathlengths (maxLength = "+str(maxPathlength)+") from "+str(start)+" to X:"
    with open(outputfile, "a") as f:
        f.write("\n");
        f.write(str(m))
    printplus(seen)


