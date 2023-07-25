"""
BDMST:
Problem Description: 
We have a network of nodes that represent post offices but these post offices have a unique capacity that dictates the amount of connections
to other post offices that they can handle. We need to find a network of post offices that uses the smallest amount of connections between post offices while 
also making sure that none of the post offices are overwhelmed by their connections, and insuring that all the post offices are not 
left out of the network. Test cases will consist of thousands to tens of thousands of post offices that can have as little as one connection
before being overwhelmed.



Plan: 
First : Run Prims
Second : Find all nodes that have a degree(number of edges) greater than their bound and multiply these edge weights by a factor slightly
larger than one
Why? Because this will encourage the next run of prims to shy away from incorporating these edges into the minimum spanning tree
and this will hopefully result in a satisfactory minimum spanning tree after a few runs of prims
Third: Find all nodes that have a degree less than their bound and subtract a small factor from those edge weights 
Why? Because this will encourage the next run of prims to shy away from incorporating these edges into the minimum spanning tree
and this will hopefully result in a satisfactory spanning tree
Fourth: Check if we have found a satisfactory spanning tree and return it.
"""

import heapq as hq
from collections import defaultdict
import BoundedMSTProblem


def createGraph(N, bounds, edges):

    graph = defaultdict(list)

    for i in range(len(edges)):
        graph[edges[i][0]].append(i)
        graph[edges[i][1]].append(i)
    
    return graph

#graph format is : index is the node number, bound is the first element, and then edges with node number and weight 

#clarifications for indexing:
#edges have the node names in 1 to n form 
#

def prims(N, graph, edges):
    #print("made it to prims")
    #print(edges)

    cost = [-1] * (N)
    cost[0] = 0

    queue = []
    hq.heappush(queue, (0 , 1))
    #pushing the starting cost and the name of the node
    seen = set()

    prev = set()

    edgeRecord = defaultdict(list)
    
    while queue:

        price, nodeName = hq.heappop(queue)

        prev.add(nodeName)
        
        if nodeName not in seen:
            seen.add(nodeName)

            for i in range(1, len(graph[nodeName])):
                #start from one because we are also storing the bound 
                
                edgeIndex = graph[nodeName][i]
                pathCost = edges[edgeIndex][2]
                
                if (edges[edgeIndex][0] == nodeName):
                    edgeNodeName = edges[edgeIndex][1]
                else:
                    edgeNodeName = edges[edgeIndex][0]


                if edgeNodeName not in prev:
                    
                    if (cost[edgeNodeName - 1] > pathCost + 10) or (cost[edgeNodeName - 1] == -1):
                        
                        

                        if (cost[edgeNodeName - 1] == -1):
                            #if it is a new node we just want to add each edgeIndex to edge record for both nodes
                            edgeRecord[nodeName].append(edgeIndex)
                            edgeRecord[edgeNodeName].append(edgeIndex)
                            #print("just adding")
                            #print(edgeRecord)

                        elif (cost[edgeNodeName - 1] > pathCost):
                            #if we are updating a cost, this means we have to remove edges from edgeRecord
                            #we have to remove the edgeIndex from the edgeNode we are looking at, and also from the node that the edgeNode connects to
                            max = len(edgeRecord[edgeNodeName]) - 1
                            edgeIndexToRemove = edgeRecord[edgeNodeName][max]
                            edgeToRemove = edges[edgeIndexToRemove]
                            
                            if edgeToRemove[0] == edgeNodeName: 
                                nodeToRemove = edgeToRemove[1] 
                            else:
                                nodeToRemove = edgeToRemove[0]

                            
                            edgeRecord[nodeName].append(edgeIndex)
                            edgeRecord[nodeToRemove].remove(edgeIndexToRemove)

                            edgeRecord[edgeNodeName][max] = edgeIndex

                        #print(edgeRecord)

                        cost[edgeNodeName - 1] = pathCost

                        hq.heappush(queue, (cost[edgeNodeName - 1], edgeNodeName))
    
    return edgeRecord
    #outputs the array of total costs

def findEdges(edgeRecord):

    seen = set()

    for i in range(len(edgeRecord)):
        for j in range(len(edgeRecord[i+1])):
            if edgeRecord[i+1][j] not in seen:
                seen.add(edgeRecord[i+1][j])
    


def updateEdges(edgeOver, edgeUnder, edgeRight, edges):

    for i in edgeOver:
        #if i not in edgeRight:
        edges[i][2] = edges[i][2] * 1.03
    
    
    
    return edges



def checkBounds(edgeDict, bounds):

    edgeOver = set()

    edgeUnder = set()

    edgeRight = set()

    success = False

    
    
    for i in range(len(bounds)):
        if len(edgeDict[i+1]) > bounds[i]:
            for j in range(len(edgeDict[i+1])):
                if edgeDict[i+1][j] not in edgeOver:
                    edgeOver.add(edgeDict[i+1][j])
        elif len(edgeDict[i+1]) < bounds[i]:
            for k in range(len(edgeDict[i+1])):
                if edgeDict[i+1][k] not in edgeUnder:
                    edgeUnder.add(edgeDict[i+1][k])
        else:
            for q in range(len(edgeDict[i+1])):
                edgeRight.add(edgeDict[i+1][q])

        
       # else:
    
    if len(edgeOver) == 0:
        success = True
    
    
    return edgeOver, edgeUnder, edgeRight, success

def returnEdges(nodeEdges):

    output = []

    for i in range(len(nodeEdges)):

        for j in range(len(nodeEdges[i])):
            
            if nodeEdges[i][j]+1 not in output:
                output.append(nodeEdges[i][j] + 1)

    output = sorted(output)

    return output

def changeWeights(edges):

    for i in range(len(edges)):
        edges[i][2] = 1
    return edges

def solve(N, M, bounds, edges):

    graph = createGraph(N, bounds, edges)

    finished = False
    edges = changeWeights(edges)
    while not finished:

        nodeEdges = prims(N, graph, edges)
        findEdges(nodeEdges)
        
        #print(nodeEdges[0])
        edgesOver, edgesUnder, edgesRight, finished = checkBounds(nodeEdges, bounds)

        if finished:
            return returnEdges(nodeEdges)
        else:
            edges = updateEdges(edgesOver, edgesUnder, edgesRight, edges)
        





def read_input():
    N, M = [int(i) for i in input().split()]
    bounds = [int(input()) for _ in range(N)]
    edges = [[int(i) for i in input().split()] for _ in range(M)]
    
    
    return N, M, bounds, edges


def main():

    #inst = BoundedMSTProblem.from_file('input01.txt')
    #e, cost = inst.score_file('my_output01.txt')  
    #print(inst)

    

    N, M, bounds, edges = read_input()
    #BDMST = BoundedMSTProblem.BoundedMSTProblem(bounds, edges)
    t = solve(N, M, bounds, edges)

    for i in range(len(t)):
        print(t[i])
    #print(t)

    



    #inst = BDMST.from_file('input01.txt')
    #e, cost = inst.score_file('output01.txt')


if __name__ == '__main__':
    main()



