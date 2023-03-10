import numpy
import queue
import heapq
from dataclasses import dataclass, field
from typing import Any
from typing import NamedTuple
import copy
# from readManifest import * #Uncomment later and remove container class from this file

# class cell:
#     def __init__(self, name, weight):
#         self.name = name
#         self.weight = weight
#     def __str__(self):
#         return self.name + " " + str(self.weight)

#From Other File
class Container():
    def __init__(self, location = (-1, -1), weight = 0, name = ''):
        self.location = location
        self.weight = weight
        self.name = name
    def printContainer(self):
        return f"Location: {self.location}, Weight: {self.weight}, Name: {self.name}"
###

class Node:
    def __init__(self, ship = [], buffer = [], g_n = 0, h_n = 0, toLoad = [], toUnload = [], currColumn = 0, currContainer = Container()):
        self.ship = ship
        self.buffer = buffer
        self.g_n = g_n
        self.h_n = h_n
        self.toLoad = toLoad
        self.toUnload = toUnload
        self.currColumn = currColumn
        self.currContainer = currContainer
    
    def __lt__(self, other):
        return self.g_n + self.h_n < other.g_n + other.h_n

def printList(ship):
    for i in ship:
            print(i.__dict__)
    return

def calH(node):
    return 

#Balancing example
ship = []
ship.append(Container((1, 1), 10, '')) #Ship[0]
ship.append(Container((1, 2), 0, 'UNUSED'))
ship.append(Container((1, 3), 0, 'UNUSED'))
ship.append(Container((1, 4), 4, ''))
ship.append(Container((2, 1), 6, ''))
ship.append(Container((2, 2), 0, 'UNUSED'))
ship.append(Container((2, 3), 0, 'UNUSED'))
ship.append(Container((2, 4), 0, 'UNUSED'))

#print(ship[1].location[0]) #Outputs 1

initialState = Node()
initialState.ship = ship
print("Original:")
printList(ship)
# print(ship[1].printContainer())
#Looks like this now:
        # 6  |    |    |    |
        # ---------------------
        # 10 |    |    |  4 |
#We want:
        #   |     |     |    |
        # ---------------------
        # 10|     |  6  |  4 |

# def algorithm(): #load/unload
#     tree = queue.PriorityQueue(0)
#     ship = numpy.empty([8, 12])
#     buffer = numpy.empty([4, 24])
    
#     print('Hello World')
def is_solvable(initialState):
    sum = 0.0
    maxW = 0.0
    for cont in initialState.ship:
        sum += cont.weight
        if(cont.weight > maxW):
            maxW = cont.weight
    return (sum-maxW) >= maxW*0.9

def checkBalanceGoal(ship):
    leftWeight = 0
    rightWeight = 0
    for cont in ship:
        if(cont.location[0] <= 4):
            leftWeight += cont.weight
        else:
            rightWeight += cont.weight
    if leftWeight + rightWeight == 0:
        return True
    elif max(leftWeight, rightWeight == 0):
        return False 
    return min(leftWeight, rightWeight)/max(leftWeight, rightWeight) > 0.9

#returns container at the top of the column given
# def return_top_container(currNode,column):
#     row = 4  #replace with number of rows in ship
#     while row >= 0:
#         if currNode.ship[row + (column - 1)].name != 'NAN' and currNode.ship[row + (column - 1)].name != 'UNUSED': #Container name != NAN or UNUSED:
#             return currNode.ship[row+(column - 1)]
#         row = row - 4 
#     emptyContainer = Container()
#     return emptyContainer

#returns container at the top of the column given -- mod
def return_top_container(currNode,column):
    row = 4  #replace with number of rows in ship
    while row >= 0:
        if currNode.ship[row + (column - 1)].name != 'NAN' and currNode.ship[row + (column - 1)].name != 'UNUSED': #Container name != NAN or UNUSED:
            return currNode.ship[row+(column - 1)]
        row = row - 4     
    return currNode.ship[row+(column - 1)]

# testCont = return_top_container(initialState,1)
# print(testCont.location,testCont.weight, testCont.name)
# #Should return Container((1, 2), 6, '')
    
def expand(givenNode, heap):
    column = 1
    maxCol = 4
    while column <= maxCol: #8 for the puzzle, temp 4
        currNode = copy.deepcopy(givenNode)
        currNode.currColumn = column
        emptyContainer = Container()
        if currNode.currContainer.location != (-1,-1): #need to pick up
            # print(currNode.currContainer.name, currNode.currContainer.weight, currNode.currContainer.location )
            #print("Curr Node Ship:")
            #printList(currNode.ship)
            topContainer = return_top_container(currNode,currNode.currColumn)
            # print("This is the top container:")
            # print(topContainer.location,topContainer.weight,topContainer.name)
            if topContainer.name != 'NAN' or topContainer.name != 'UNUSED': #if container is found
                newNode = copy.deepcopy(currNode)
                newNode.currContainer = topContainer
                #currNode.ship[(row - 1)* column - 1]
                newNode.ship[(topContainer.location[0] - 1)* maxCol + (topContainer.location[1] - 1)].name = "UNUSED" 
                newNode.ship[(topContainer.location[0] - 1)* maxCol + (topContainer.location[1] - 1)].weight = 0
                #print("New:")
                #printList(newNode.ship)
                heapq.heappush(heap,newNode)
        else: #need to put down
        #get the currContainer from currNode currNode.currContainer
            newNode = copy.deepcopy(currNode)
            topContainer = return_top_container(currNode,currNode.currColumn)
            if topContainer.name != 'UNUSED': #put it in cell above
                if topContainer.location[0] < 2:
                    newNode.ship[(topContainer.location[0])* maxCol + (topContainer.location[1] - 1)] = copy.deepcopy(newNode.currContainer)
                    # newNode.ship[(topContainer.location[0])* maxCol + (topContainer.location[1] - 1)].name = newNode.currContainer.name
                    # newNode.ship[(topContainer.location[0])* maxCol + (topContainer.location[1] - 1)].weight = newNode.currContainer.weight
                    # newNode.ship[(topContainer.location[0])* maxCol + (topContainer.location[1] - 1)].location = newNode.currContainer.location
                    newNode.currContainer.location = (-1,-1)
                    newNode.currContainer.name = ''
                    newNode.currContainer.weight = 0
                    print("New:")
                    printList(newNode.ship)
                    heapq.heappush(heap,newNode)
            else: #put it at UNUSED location
                newNode.ship[(topContainer.location[0] - 1)* maxCol + (topContainer.location[1] - 1)] = copy.deepcopy(newNode.currContainer)
                # newNode.ship[(topContainer.location[0] - 1)* maxCol + (topContainer.location[1] - 1)]= copy
                # newNode.ship[(topContainer.location[0] - 1)* maxCol + (topContainer.location[1] - 1)].weight = newNode.currContainer.weight
                # newNode.ship[(topContainer.location[0] - 1)* maxCol + (topContainer.location[1] - 1)].location = newNode.currContainer.location
                newNode.currContainer.location = (-1,-1)
                newNode.currContainer.name = ''
                newNode.currContainer.weight = 0
                print("New:")
                printList(newNode.ship)
                heapq.heappush(heap,newNode)
            #check for repeated states

        column = column + 1
    #print("Given Node:")
    #printList(givenNode.ship)
heap = [] 
heapq.heapify(heap)
expand(initialState,heap)
currState = heapq.heappop(heap)
expand(currState, heap)

def balance(initialState):
    if not is_solvable(initialState):
        return "Not Solvable"
    currState = Node()
    heap = []
    heapq.heapify(heap)
    heapq.heappush(heap,initialState)
    while True:
        if (len(heap) == 0):
            return "Failure"
        currState = heapq.heappop(heap)
        if checkBalanceGoal(currState.ship):
            return currState
        else:
            #expand node
            expand(currState, heap)
        #apply operators and add new nodes to heap
        # move to column left
        # move to column right
        # move to buffer
        # move from buffer to smaller side

# temp = balance(initialState)
# print(temp)
# print("New:")
# printList(temp.ship)
#q.push(Node(moveRight(currentPuzzle, blankPosition),nodeDepth + 1,calculateMisplacedTile(moveRight(currentPuzzle, blankPosition)) + nodeDepth));
# temp = swapValues(puzzleTop, row-1, col, "up");

        

# numpy.array(cell, )

# if __name__ == '__main__':
    
#     # ship[0][3] = "Joe"
    
#     algorithm()
#     balance(ship, buffer)

######################################################################
#node class
# include state 4 lists
# 1 for unload, 1 for load, 1 for ship, 1 for buffer (gaol state is empty load/unload/buffer)
# include int for number of moves (time) g(n)
# include heuristic h(n)