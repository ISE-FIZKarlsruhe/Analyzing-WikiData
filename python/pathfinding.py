#!/usr/bin/env python

#v3.1 -current
import csv
from collections import defaultdict
from sys import stdout
import numpy as np
import time
import random
import sys

#Information need parameter
start = 1              #define the start node
goal = 42                #define the goal node
maxPathlength = 10      #define the maximal pathlength

#Action parameter
rebuildDirected = True      #Specifies wheather or not the dictionary should be rebuild (Has to be set to True for the first run only)
rebuildUndirected = False    #build an undirected version of the graph (only apllied when "rebuildDirected = False")
verbose = False         #set to False to disable to progress percentage and to slightly improve performance (default: True)
tofile = False           #if True, any output is printed to a generated file, following certain name specifications

#file parameter
inputfile = "wikidata_objects_noduplicates.csv"
#inputfile = "../igraph/smallgraph4.csv"
outputFolderPath = "output_testing/"

#methods:
#printAggregatePathLengths(dictionary)
#printplus(dictionary or list)
#buildDict()
#getPath(start,[goal])  - if no goal is defined, all data on shortest paths is returned
#getReachableNodes(start)   - returns a dictionary
#getAllShortestPaths(start)   - returns a list
#getClosenessCentrality(start)
#getHarmonicCentrality(start)
#printSinglePath(path)


def main():
    print("")
#   examples:
#   pathToFile(getPath(start,goal)) 
#   pathToFile(randomPath(100)[2][0])  
#   printplus(getAllShortestPaths(start))
#   printplus(getReachableNodes(start))
#   print(getClosenessCentrality(start))
#   print(getHarmonicCentrality(start))    
#   printAggregatePathLengths(start)
   
# ------------------ Code here --------------------- #
    
#'''Overlap between two random entities:'''
#    for x in range(0, 25): 
#        for e,o in zip(random.sample(sorted(dictionary.keys()), 1),random.sample(sorted(dictionary.keys()), 1)):
#            print(e,"vs.",o)
#            a = list(getReachableNodes(e).keys())
#    #       print(len(a))
#            b = list(getReachableNodes(o).keys())
#    #       print(len(b))
#            print(getOverlap(a,b)) 
#            print("-----------------------")
        
#'''Find existing path between two random entities'''   
#    count = 0
#    for i in range(0,50):
#        print(i)
#        p=randomPath(0)
#        print (p)
#        if (not p[2] == []):
#           count += 1
#    print("Successful:",count,"of",i+1)
##    for sp in p[2]:
##        pathToFile(sp)              

    # for k,o in dictionary.items():
    #     print(k,getClosenessCentrality(k))
    # print()
    # for k,o in dictionary.items():
    #     print(k,getHarmonicCentrality(k))

    print(getPath(start, goal))


#returns the path between two random entities from a sample of the frist 'r' wikidata entitites
def randomPath(r):        
    if r == 0:
        r = len(dictionary.keys())-1
    for e,o in zip(random.sample(sorted(dictionary.keys())[:r], 1),random.sample(sorted(dictionary.keys())[:r], 1)):
       return e,o,getPath(e,o)   
         
#prints the number of shortest paths to other nodes for each given pathlength

def printAggregatePathLengths(start):
    seen = getReachableNodes(start)
    print("\nNew objects reached per pathlength from entity",start)
    a = np.zeros(maxPathlength+1) 
    for k, v in sorted(seen.items()):
       a[v] += 1
    for i, v in enumerate(a):
        print(i,str(int(v)),sep='; ')
    print("")

def pathToFile(path):
    if (path == []):
        print("No path")
        return;
    #output file parameters
    outputfile = outputFolderPath+"output_Q%d_to_Q%d" %(path[0],path[len(path)-1])  
    prev = path[0];
    print("Detailed path printed to file",outputfile)
    with open(outputfile, "a") as f:     
       for e  in path[1:]: 
           m = str(prev)+" "+str(e)+"\n" 
           f.write(m)
           print(m,end='')
           prev = e
       
#function to print the main list and the dictionary in a nice way
def printplus(obj,tofile=tofile):
    # Dictionary
    if isinstance(obj, __builtins__.dict):
        outputfile = outputFolderPath+"output_len%d_Q%d_reached" %(maxPathlength,sorted(obj, key=obj.get)[0])
        maxkey = max(obj, key=int)
        j = 0
        print("Printing dictionary of reached nodes")
        if(tofile):  print("to file",outputfile)
        for k, v in sorted(obj.items()):
            if(tofile):
                with open(outputfile, "a") as f:
                    f.write("\n"+u'{0}: {1}'.format(k, v))
                if (verbose):
                    if (k == maxkey):
                        j = 100
                    if (k >= maxkey*j/100):
                        stdout.write("\r%d" %j+"%")
                        stdout.flush()
                        j = j+1  
            else:
                print(u'{0}: {1}'.format(k, v))  
                   
    # List         
    elif isinstance(obj, __builtins__.list):
        outputfile = outputFolderPath+"output_len%d_Q%d_pathlist" %(maxPathlength,obj[0][0])
        j = 0
        print("Printing list of paths")
        if(tofile):  print("to file",outputfile)
        for i,x in enumerate(sorted(obj,key=lambda x:x[len(x)-1])):
            if(tofile):
                with open(outputfile, "a") as f:
                    f.write("\n"+str(x))
                if (verbose):
                    if (i >= (len(obj)-1)*j/100):
                        stdout.write("\r%d" %j+"%")
                        stdout.flush()
                        j=j+1
            else:
                print(str(x))
    print(" ")

#read csv file and build the dictionary
def buildDirected(inputfile):    
    dictionary = defaultdict(list);
    i = 0;              
    with open(inputfile, newline ='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        print("Building up the main dictionary", end=" ")
        for key, value in reader:
            dictionary[int(key)].append(int(value))
            i = i+1;
            if (i % 3100000 == 0):
                print(".", end=" ")
        print("\nDictionary built successfully!\n")
        return dictionary

#read csv file and build the dictionary
def buildUndirected(inputfile):    
    undirected = defaultdict(list);
    i = 0;              
    with open(inputfile, newline ='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        print("Buildung up the main dictionary", end=" ")  
        for key, value in reader:
            if not (value in undirected[key]):
                undirected[int(key)].append(int(value))
            if not (key in undirected[value]):
                undirected[int(value)].append(int(key))
            i = i+1;
            if (i % 3100000 == 0):
                print(".", end=" ")
        print("\nDictionary built successfully!\n")
        return undirected       
    
#return the shortest path in accordance to the provided parameters or prints it to file
#if no goal is specifies, a tupel consiting of 1. a list of all shortest paths and 2. a dictionary with all reachable nodes
def getPath(start=start,goal=goal,maxPathlength=maxPathlength,verbose=verbose):        
    #initialisation
    mainlist = [[start]]
    result = []
    seen = defaultdict(int)
    seen[start] = 0
    currentLength = 0
    if ((goal != None) and (goal == start)):
        return [[start]]
    #iterate over each path in the main list
    for p in mainlist:      
        #...until pathlength is greater than 5 or the goal has been found, main is countinously increased
        if len(p) <= maxPathlength:
            if len(p) != currentLength:
                currentLength = len(p);
                if(verbose):
                    print("Checking paths of length =",currentLength)
            #define the currently viewed node as s (subject)
            s = p[len(p)-1]
            #Check if the reached node appears in our dictionary - only if it does, proceed
            if dictionary.get(s) != None:
                #get all immediately connected objects from s from the dictionary
                for o in dictionary.get(s):
                    #check if the object has been seen before (i.e. there is a shorter path to this o)                  
                    if seen.get(o) == None or o == goal:
                        #define the object as 'seen' together with the shortest pathlength to said object
                        seen[o] = currentLength
                        #create the full path leading to new object  
                        x = list(p);
                        x.append(o);
                        #add the object's path to the main list
                        if len(result)==0: 
                            mainlist.append(x)
                    if (goal != None):
                        if o == goal:
                            result.append(x)
                            maxPathlength = currentLength
    #if no path was found, None is returned
    if (goal != None):                                   
        return result
    #if no geal was defined, all gathered data is returned
    if (goal == None):
        return [mainlist, seen]
        
def getAllShortestPaths(start):
    return getPath(start,None)[0]

def getReachableNodes(start):
    return getPath(start,None)[1]

def getOverlap(listA,listB):
    setA = set(listA)
    setB = set(listB) 
    overlap = setA & setB
    universe = setA | setB 
    oA = round(float(len(overlap)) / len(setA) * 100,5)
    oB = round(float(len(overlap)) / len(setB) * 100,5)
    oU = round(float(len(overlap)) / len(universe) * 100,5)
    difference = list(set(universe)-set(overlap))
    print("Difference:",difference)
    print("Difference size:",len(difference))
    return oA,oB,oU

#claculates the closeness for a given start node. I.e. the average distance of the shortest path to any other node
def getClosenessCentrality(start):  
    closeness = 0
    for k, v in sorted(dictionary.items()):
        goal = k
        path = getPath(start, goal, maxPathlength=20, verbose=False)
        #print(path)
        pathlength = len(path[0]) if path != [] else 0
        #The else part is equal to the "punishement" for not being able to reach a node
        if pathlength != 0:
            distance = pathlength-1
        else:
            distance = len(dictionary.keys())
        closeness += distance
        #print(start, goal, distance, "--", closeness)
    closeness = (len(dictionary.items())-1)/closeness if closeness != 0 else 0
    #print("Closeness for",start,": ",closeness,"\n")
    return closeness
     
def getHarmonicCentrality(start):  
    closeness = 0
    for k, v in sorted(dictionary.items()):
        goal = k
        path = getPath(start,goal,maxPathlength, verbose = False)
        # print(path)
        pathlength = len(path[0]) if path != [] else 0
        if pathlength != 0:
            distance = pathlength-1
        else:
            distance = len(dictionary.keys())
        closeness += 1/distance if distance != 0 else 0
        #print(start, goal, distance)
    closeness /= len(dictionary.items())-1
    #print("Closeness for",start,": ",closeness)
    return closeness

if (rebuildDirected):
        dictionary = buildDirected(inputfile)
if (rebuildUndirected and not rebuildDirected):
        dictionary = buildUndirected(inputfile) 
main()    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    