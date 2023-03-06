import numpy
import queue
import heapq
from dataclasses import dataclass, field
from typing import Any
from typing import NamedTuple
# from readManifest import * #Uncomment later and remove container class from this file

# class cell:
#     def __init__(self, name, weight):
#         self.name = name
#         self.weight = weight
#     def __str__(self):
#         return self.name + " " + str(self.weight)

#From Other File
class Container():
    def __init__(self):
        self.location = (-1,-1)
        self.weight = 0
        self.name = ''
###

class Node:
    def __init__(self):
        self.ship = []
        self.buffer = []
        self.g_n = 0
        self.h_n = 0
        self.toLoad = []
        self.toUnload = []
        self.currColumn = 0 
        self.currContainer = Container()
    
    def __lt__(self, other):
        return self.g_n + self.h_n < other.g_n + other.h_n

def calH(node):
    return 

#Balancing example
ship = []
currContainer = Container((1, 1), 10, '')
ship.append(currContainer) #Ship[0]
ship.append(Container((1, 2), 6, ''))
ship.append(Container((2, 1), 0, 'UNUSED'))
ship.append(Container((2, 2), 0, 'UNUSED'))
ship.append(Container((3, 1), 0, 'UNUSED'))
ship.append(Container((3, 2), 0, 'UNUSED'))
ship.append(Container((4, 1), 4, ''))
ship.append(Container((4, 2), 0, 'UNUSED'))

#print(ship[1].location[0]) #Outputs 1

initialState = Node()
initialState.ship = ship

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
    for cont in initialState:
        sum += cont.weight
        if(cont.weight > maxW):
            maxW = cont.weight
    return sum > maxW*10

def checkBalanceGoal(ship):
    leftWeight = 0
    rightWeight = 0
    for cont in ship:
        if(cont.location[0] <= 4):
            leftWeight += cont.weight
        else:
            rightWeight += cont.weight
    return min(leftWeight, rightWeight)/max(leftWeight, rightWeight) > 0.9

def return_top_container(currNode,column):
    row = 4  #replace with number of rows in ship
    while row >= 0:
        if currNode.ship[row + (column - 1)].name != 'NAN' and currNode.ship[row + (column - 1)].name != 'UNUSED': #Container name != NAN or UNUSED:
            return currNode
        row = row - 4 
    emptyNode = Node()
    return emptyNode

print(return_top_container(initialState,1))
#Should return Container((1, 2), 6, '')
    
def expand(givenNode, heap):
    column = 1
    while column <= 4: #8 for the puzzle, temp 4
        currNode = givenNode
        topContainer = return_top_container(currNode,currNode.currColumn)
        if len(topContainer.ship) != 0: #we have a top container
            currNode.currContainer = topContainer
            nextNode = currNode
            # nextNode.ship[]

        heapq.heappush(heap,)
        column = column + 1
# heap = []
# heapq.heapify(heap)
# expand(initialState,heap)

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
        if len(currState.buffer) == 0 and len(currState.toLoad) == 0 and len(currState.toUnload) == 0:
            return currState
        #apply operators and add new nodes to heap
        # move to column left
        # move to column right
        # move to buffer
        # move from bufffer to smaller side

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