import numpy
import queue
import heapq
from dataclasses import dataclass, field
from typing import Any
from typing import NamedTuple
import copy

#global variables
maxCol = 4
maxRow = 2
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
        if(cont.location[1] <= 2): #need to fix this later
            leftWeight += cont.weight
        else:
            rightWeight += cont.weight
    if leftWeight + rightWeight == 0: #Empty Ship or all weights are 0
        return True
    #elif max(leftWeight, rightWeight) == 0:
        #return False
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
    index = 4 #replace with number of top left index
    while index >= 0:
        if currNode.ship[index + (column - 1)].name != 'NAN' and currNode.ship[index + (column - 1)].name != 'UNUSED': #Container name != NAN or UNUSED:
            return currNode.ship[index+(column - 1)]
        index = index - 4   #change according to ship size
    return currNode.ship[index+(column - 1)]

ship = []
ship.append(Container((1, 1), 10, '')) #Ship[0]
ship.append(Container((1, 2), 0, 'UNUSED'))
ship.append(Container((1, 3), 6, ''))
ship.append(Container((1, 4), 4, ''))
ship.append(Container((2, 1), 0, 'UNUSED'))
ship.append(Container((2, 2), 0, 'UNUSED'))
ship.append(Container((2, 3), 0, 'UNUSED'))
ship.append(Container((2, 4), 0, 'UNUSED'))
initialState2 = Node()
initialState2.ship = ship
# print(checkBalanceGoal(initialState2.ship))
# print("Original:")
# printList(ship)

def return_top_available_cell_location(currNode,column):
    index = 4 #replace with number of rows in ship
    while index >= 0:
        if currNode.ship[index + (column - 1)].name != 'UNUSED':  #If is NAN or Container
            tempLocation = (currNode.ship[index+(column - 1)].location[0] + 1, currNode.ship[index+(column - 1)].location[1])
            if tempLocation[0] <= maxRow:
                return tempLocation
            else: #Full Column
                return (-1,-1)
        index = index - 4     
    return (1,column) #Empty Column, return bottom most cell
        
# testing = return_top_available_cell_location(initialState,1)
# print(testing)

# testCont = return_top_container(initialState,1)
# print(testCont.location,testCont.weight, testCont.name)
# #Should return Container((1, 2), 6, '')
    
def expand(givenNode, heap):
    column = 1
    while column <= maxCol: #8 for the puzzle, temp 4
        emptyContainer = Container()
        currNode = copy.deepcopy(givenNode)
        currNode.g_n = currNode.g_n + 1
        currNode.currColumn = column
        # print("Curr Node's Curr Container")
        # print(currNode.currContainer.location)
        if currNode.currContainer.location == (-1,-1): #need to pick up
            #print(currNode.currContainer.name, currNode.currContainer.weight, currNode.currContainer.location )
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
                #Put down container
                innerColumn = 1
                # originalNode = copy.deepcopy(newNode)
                while innerColumn <= maxCol:
                    tempLocation = return_top_available_cell_location(newNode,innerColumn)
                    # print("Current Top Available Cell:", tempLocation)
                    if tempLocation == (-1,-1):
                        innerColumn = innerColumn + 1
                        continue
                    #place it
                    topContainerName = copy.deepcopy(topContainer.name)
                    topContainerWeight = copy.deepcopy(topContainer.weight)
                    # topContainerLocation = copy.deepcopy(topContainer.location)
                    newNode.ship[(tempLocation[0] - 1) * maxCol + (tempLocation[1] - 1)].name = topContainerName
                    newNode.ship[(tempLocation[0] - 1) * maxCol + (tempLocation[1] - 1)].weight = topContainerWeight
                    # newNode.ship[(tempLocation[0] - 1) * maxCol + (tempLocation[1] - 1)].location = topContainerLocation
                    newNode.currContainer = emptyContainer
                    innerColumn = innerColumn + 1

                    nodeToPush = copy.deepcopy(newNode)
                    # print("New:")
                    # printList(nodeToPush.ship)
                    # print("Curr container: ")
                    # print(nodeToPush.currContainer.name, nodeToPush.currContainer.weight, nodeToPush.currContainer.location )
                    heapq.heappush(heap,nodeToPush) 
                    newNode.ship[(tempLocation[0] - 1)* maxCol + (tempLocation[1] - 1)].name = "UNUSED" 
                    newNode.ship[(tempLocation[0] - 1)* maxCol + (tempLocation[1] - 1)].weight = 0

        column = column + 1
    

# heap = [] 
# heapq.heapify(heap)
# expand(initialState,heap)
# heapq.heappop(heap)
# currState = heapq.heappop(heap)
            # while len(heap):
            #     print("Element:")
            #     printList(heapq.heappop(heap).ship)
# print("Orig: ")
# printList(currState.ship)
# print(currState.currContainer.name,currState.currContainer.weight,currState.currContainer.location)
# print("Initial State 2")
# printList(initialState2.ship)
# print(initialState2.currContainer.name,initialState2.currContainer.weight,initialState2.currContainer.location)
# expand(currState,heap)

def balance(initialState):
    if not is_solvable(initialState):
        return "Not Solvable"
    currState = Node()
    heap = []
    heapq.heapify(heap)
    heapq.heappush(heap,initialState)
    # currIt = 0
    while True:
        # print("iteration",currIt)
        # currIt = currIt + 1
        if (len(heap) == 0):
            return "Failure"
        currState = heapq.heappop(heap)
        # print("State:")
        # printList(currState.ship)
        if checkBalanceGoal(currState.ship):
            return currState
        else:
            #expand node
            expand(currState, heap)
            # print(len(heap))
            # print("State After:")
            # printList(currState.ship)

        #apply operators and add new nodes to heap
        # move to column left
        # move to column right
        # move to buffer
        # move from buffer to smaller side

temp = balance(initialState)
if temp == "Failure":
    print(temp)
else:
    print("Solved:")
    printList(temp.ship)

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