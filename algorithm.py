import numpy
import queue
import heapq
from dataclasses import dataclass, field
from typing import Any
from typing import NamedTuple
import copy
from readManifest import * 


#global variables
maxCol = 12
maxRow = 8
repeatedStates = [] #holds list of containers (ships)

#From Other File
# class Container():
#     def __init__(self, location = (-1, -1), weight = 0, name = ''):
#         self.location = location
#         self.weight = weight
#         self.name = name
#     def printContainer(self):
#         return self.weight
        # return f"Location: {self.location}, Weight: {self.weight}, Name: {self.name}"
###

class Node:
    def __init__(self, ship = [], buffer = [], g_n = 0, h_n = 0, toLoad = [], toUnload = [], currColumn = 0, currContainer = Container(), moves = []):
        self.ship = ship
        self.buffer = buffer
        self.g_n = g_n
        self.h_n = h_n
        self.toLoad = toLoad
        self.toUnload = toUnload
        self.currColumn = currColumn
        self.currContainer = currContainer
        self.moves = moves
    
    def __lt__(self, other):
        return self.g_n + self.h_n < other.g_n + other.h_n

def printList(ship):
    for i in ship:
            print(i.__dict__)
    return

def printShip(ship):
    for i in reversed(range(maxRow)):
        print('\n')
        for x in range(maxCol):
            if ship[(i)*maxCol + (x)].name == 'NAN':
                print("-1" + " ", end = " ")
            else:
                print(str(ship[(i)*maxCol + (x)].printContainer()) + " ", end = " ")
    print("\n")
    return

def printWeights(ship):
    for i in range(len(ship)):
        print(str(ship[i].weight) + ", ", end = " ")
    print("\n")
    return

#Balancing example
# ship = []
# ship.append(Container((1, 1), 10, '')) #Ship[0]
# ship.append(Container((1, 2), 0, 'UNUSED'))
# ship.append(Container((1, 3), 0, 'UNUSED'))
# ship.append(Container((1, 4), 4, ''))
# ship.append(Container((2, 1), 6, ''))
# ship.append(Container((2, 2), 0, 'UNUSED'))
# ship.append(Container((2, 3), 0, 'UNUSED'))
# ship.append(Container((2, 4), 0, 'UNUSED'))
ship = []
i = 1
while i <= 8:
    j = 1
    while j <= 12:
        ship.append(Container((i,j),0,'UNUSED'))
        j+=1
    i+=1
     
ship[0] = Container((1,1),130,'Bob')
ship[1] = Container((1,2),20,'Bob2')
ship[2] = Container((1,3),50,'Bob3')
ship[3] = Container((1,4),20,'Bob4')

#print(ship[1].location[0]) #Outputs 1
# ship = openFile()
initialState = Node()
initialState.ship = ship
print("Original:")
printShip(ship)
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

def group_up(lst, var_lst): #https://www.geeksforgeeks.org/python-convert-1d-list-to-2d-list-of-variable-length/
    idx = 0
    for var_len in var_lst:
        yield lst[idx : idx + var_len]
        idx += var_len

def ComputeSIFTMisplacedTile(givenNode, goalShip):
    score = 0
    currShip = givenNode.ship
    i = 0
    while i < maxRow * maxCol:
        if currShip[i].weight != goalShip[i]:
            score+=1
        i+=1
    return score

def SIFT(SIFT_ship):       
    var_lst = []
    ship = []
    for container in SIFT_ship:
        ship.append(container.weight)
    #divided_ship = [[8,7,6,5],[4,3,2,1]]
    #new_divided_ship = [[8,7,6,5],[4,3,2,1]]
    #ship = [8,7,6,5,4,3,2,1]
    ship.sort(reverse = True) # https://stackoverflow.com/questions/403421/how-do-i-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
    for i in range(maxRow):
        var_lst.append(maxCol)
    divided_ship  = list(group_up(ship,var_lst))

    new_divided_ship = copy.deepcopy(divided_ship)

    ship_pointer = 0
    nested_index = 0
    for i in divided_ship: #Each row, Outputs i = [8,7,6,5] and then i = [4,3,2,1]
        left_pointer = len(i)/2 - 1 #len([8,7,6,5]) / 2  - 1 which is 1
        right_pointer = len(i)/2 #len([8,7,6,5]) / 2  which is 12
        while left_pointer >= 0 and right_pointer < len(i):

            new_divided_ship[nested_index][int(left_pointer)] = ship[ship_pointer]
            left_pointer -= 1
            ship_pointer += 1
            
            new_divided_ship[nested_index][int(right_pointer)] = ship[ship_pointer]
            right_pointer += 1
            ship_pointer += 1
        nested_index += 1
    new_divided_ship_flattened = sum(new_divided_ship,[]) # https://www.geeksforgeeks.org/python-ways-to-flatten-a-2d-list/
    return new_divided_ship_flattened

def checkSIFTGoal(ship, goalShip): #goalship = [1,2,3,4,5,6,7,8]
    for i in range(len(goalShip)):
        if ship[i].weight != goalShip[i]:
            return False
    return True
# ship = []
# ship.append(Container((1, 1), 4, '')) #Ship[0]
# ship.append(Container((1, 2), 10, 'UNUSED'))
# ship.append(Container((1, 3), 6, ''))
# ship.append(Container((1, 4), 0, ''))
# ship.append(Container((2, 1), 0, 'UNUSED'))
# ship.append(Container((2, 2), 0, 'UNUSED'))
# ship.append(Container((2, 3), 0, 'UNUSED'))
# ship.append(Container((2, 4), 0, 'UNUSED'))
# initialState2 = Node()
# initialState2.ship = ship
# print(checkSIFTGoal(ship,SIFT(ship)))
    
def checkBalanceGoal(ship):
    leftWeight = 0
    rightWeight = 0
    for cont in ship:
        if(cont.location[1] <= (maxCol/2)): #need to fix this later
            leftWeight += cont.weight
        else:
            rightWeight += cont.weight
    if leftWeight + rightWeight == 0: #Empty Ship or all weights are 0
        return True
    #elif max(leftWeight, rightWeight) == 0:
        #return False
    return min(leftWeight, rightWeight)/max(leftWeight, rightWeight) >= 0.9

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
    index = 84 #replace with number of top left index
    while index >= 0:
        if currNode.ship[index + (column - 1)].name != 'NAN' and currNode.ship[index + (column - 1)].name != 'UNUSED': #Container name != NAN or UNUSED:
            return currNode.ship[index+(column - 1)]
        index = index - maxCol   #change according to ship size
    return currNode.ship[index+(column - 1)]

def doSIFT(initialState):
    currState = Node()
    heap = []
    heapq.heapify(heap)
    heapq.heappush(heap,initialState)
    repeatedStates.append(initialState.ship)

    # currIt = 0
    SIFTvalue = SIFT(initialState.ship)
    while True:
        currState = heapq.heappop(heap)
        #printWeights(currState.ship)
        # print("State:")
        # printList(currState.ship)
        if checkSIFTGoal(currState.ship,SIFTvalue):
            for i in currState.moves:
                print(i)
            # print("G_N:")
            # print(currState.g_n)
            return currState
        else:
            #expand node
            expand(currState, heap, True)
    

# print(checkBalanceGoal(initialState2.ship))
# print("Original:")
# printList(ship)

def return_top_available_cell_location(currNode,column):
    index = 84 
    while index >= 0:
        if currNode.ship[index + (column - 1)].name != 'UNUSED':  #If is NAN or Container
            tempLocation = (currNode.ship[index+(column - 1)].location[0] + 1, currNode.ship[index+(column - 1)].location[1])
            if tempLocation[0] <= maxRow:
                return tempLocation
            else: #Full Column
                return (-1,-1)
        index = index - maxCol
    return (1,column) #Empty Column, return bottom most cell
        
# testing = return_top_available_cell_location(initialState,1)
# print(testing)

# testCont = return_top_container(initialState,1)
# print(testCont.location,testCont.weight, testCont.name)
# #Should return Container((1, 2), 6, '')
    
def exists(ship):
    for list_of_containers in repeatedStates:
        counter = 0
        same = True
        for container in list_of_containers:
            if not container.name == ship[counter].name:
                # print(container.name, ship[counter].name)
                same = False
                break
            counter += 1
        if same:
            # print("True")
            return True
        # print("end of inner loop ", counter)
    # print("False")
    return False
    # for list_of_containers in repeatedStates: #iterates through ships in repeates states
    #     for containers in ship:        
    #         for container in list_of_containers: #iterates through containers in current ship from repeated states
    #             print(container.name, containers.name)
    #             if container.name == containers.name:
    #                 return True
    # return False

def expand(givenNode, heap, isSift):
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

                    # print(len(repeatedStates))
                    nodeToPush = copy.deepcopy(newNode)
                    nodeToPush.moves.append((currNode.currColumn, tempLocation[1]))
                    # print("New:")
                    # printList(nodeToPush.ship)
                    # print("Curr container: ")
                    # print(nodeToPush.currContainer.name, nodeToPush.currContainer.weight, nodeToPush.currContainer.location )
                    # if any(x == nodeToPush.ship for x in repeatedStates):#https://stackoverflow.com/questions/9371114/check-if-list-of-objects-contain-an-object-with-a-certain-attribute-value
                    if not exists(nodeToPush.ship): 
#                         print("New:")
#                         printShip(nodeToPush.ship)
                        if isSift:
                            nodeToPush.h_n = ComputeSIFTMisplacedTile(nodeToPush,SIFT(nodeToPush.ship))   
                        heapq.heappush(heap,nodeToPush) 
                        repeatedStates.append(nodeToPush.ship)
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
        return doSIFT(initialState)
    currState = Node()
    heap = []
    heapq.heapify(heap)
    heapq.heappush(heap,initialState)
    repeatedStates.append(initialState.ship)
    # currIt = 0
    while True:
        # print("iteration",currIt)
        # currIt = currIt + 1
        if (len(heap) == 0):
            return "Failure"
        currState = heapq.heappop(heap)
        # print("State:")
        # printShip(currState.ship)
        if checkBalanceGoal(currState.ship):
            for i in currState.moves:
                print(i)
            # print(currState.g_n)
            return currState
        else:
            #expand node
            expand(currState, heap, False)
            # print(len(heap))
            # print("State After:")
            # printList(currState.ship)

        #apply operators and add new nodes to heap
        # move to column left
        # move to column right
        # move to buffer
        # move from buffer to smaller side
# ship = []
# ship.append(Container((1, 1), 0, 'Bob')) #Ship[0]
# ship.append(Container((1, 2), 0, 'UNUSED'))
# ship.append(Container((1, 3), 7, 'Bob3'))
# ship.append(Container((1, 4), 3, 'Bob4'))
# ship.append(Container((2, 1), 0, 'UNUSED'))
# ship.append(Container((2, 2), 0, 'UNUSED'))
# ship.append(Container((2, 3), 2, 'Bob5'))
# ship.append(Container((2, 4), 2, 'Bob6'))
# initialState3 = Node()
# initialState3.ship = ship
# print("Original:")
# printShip(ship)
# test = (0,100,10,0,0,1,0,0)
# print(checkSIFTGoal(ship,test))
#repeatedStates.append(initialState.ship)
# repeatedStates.append(initialState3.ship)
# exists(initialState.ship)

temp = balance(initialState)
if temp == "Failure":
    print(temp)
else:
    print("Solved:")
    printShip(temp.ship)
 

###############################################################




# ship = []
# ship.append(Container((1, 1), 100, '')) #Ship[0]
# ship.append(Container((1, 2), 9, ''))
# ship.append(Container((1, 3), 8, ''))
# ship.append(Container((1, 4), 0, ''))
# ship.append(Container((2, 1), 0, ''))
# ship.append(Container((2, 2), 3, ''))
# ship.append(Container((2, 3), 2, ''))
# ship.append(Container((2, 4), 1, ''))
# initialState3 = Node()
# initialState3.ship = ship
# print("SIFT:")
# print(SIFT(ship))



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
