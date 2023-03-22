from algorithm import *
from readManifest import *
# '''
# Balancing example on 2x4 to test algorthm
# '''
# ship = []
# ship.append(Container((1, 1), 10, '')) #Ship[0]
# ship.append(Container((1, 2), 0, 'UNUSED'))
# ship.append(Container((1, 3), 0, 'UNUSED'))
# ship.append(Container((1, 4), 4, ''))
# ship.append(Container((2, 1), 6, ''))
# ship.append(Container((2, 2), 0, 'UNUSED'))
# ship.append(Container((2, 3), 0, 'UNUSED'))
# ship.append(Container((2, 4), 0, 'UNUSED'))


#print(ship[1].location[0]) #Outputs 1
# ship = openFile()
#
# print("Original:")
# printShip(ship)
# print(ship[1].printContainer())
#balance(ship)
#Looks like this now:
        # 6  |    |    |    |
        # ---------------------
        # 10 |    |    |  4 |
#We want:
        #   |     |     |    |
        # ---------------------
        # 10|     |  6  |  4 |
# '''
# Balancing SIFT example on 2x4 to test algorthm
# '''
# ship = []
# ship.append(Container((1, 1), 6, '')) #Ship[0]
# ship.append(Container((1, 2), 100, 'UNUSED'))
# ship.append(Container((1, 3), 4, ''))
# ship.append(Container((1, 4), 0, ''))
# ship.append(Container((2, 1), 0, 'UNUSED'))
# ship.append(Container((2, 2), 0, 'UNUSED'))
# ship.append(Container((2, 3), 0, 'UNUSED'))
# ship.append(Container((2, 4), 0, 'UNUSED'))
# initialState2 = Node()
# initialState2.ship = ship
# balance(initialState2)
# print(checkSIFTGoal(ship,SIFT(ship)))
#Looks like this now:
        #    |    |    |    |
        # ---------------------
        # 6  | 100|  4 |    |
#We want:
        #    |    |    |    |
        # ---------------------
        # 4  | 100|  6 |    |

# '''
# Tests for
# '''
# ship = []
# i = 1
# while i <= 8:
#     j = 1
#     while j <= 12:
#         ship.append(Container((i,j),0,'UNUSED'))
#         j+=1
#     i+=1

#
# ship = openFile()
# initialState = Node()
# initialState.ship = ship
# initialState.toLoad = [Container((0,0),2,'Liz')]
# initialState.toUnload = ['Cat','Dog']
# print("Original:")
# printShip(ship)
# heap = []
# heapq.heapify(heap)
# heapq.heappush(heap,initialState)
# repeatedStates.append(initialState.ship)
# solved = balance(initialState)
# print(estimate_time(solved.moves)) #test estimated time function

# '''
# Test loading/unloading example
# '''
# ship[0] = Container((1,1),10,'Bob')
# ship[12] = Container((2,1),20,'Bob2')
# ship[2] = Container((1,3),50,'Bob3')
# ship[3] = Container((1,4),30,'Bob4')
# initialState = Node()
# initialState.ship = ship
# initialState.toUnload = ["Bob","Bob2"]
# initialState.toLoad = [Container((0,0),30,'Bob3'), Container((0,0),40,'Bob4')]
# ship = openFile()
# initialState = Node()
# initialState.ship = ship
# initialState.toLoad = [Container((0,0),2,'Liz')]
# initialState.toUnload = ['Cat','Dog']
# print("Original:")
# printShip(ship)
# heap = []
# heapq.heapify(heap)
# heapq.heappush(heap,initialState)
# repeatedStates.append(initialState.ship)
# unload(initialState)

# '''
# Test expand unloading
# '''
# print("Level 1\n")
# print("--------------------------\n")
# popState = heapq.heappop(heap) #initial
# expandUnload(initialState,heap)
# popState = heapq.heappop(heap)
# print("Level 2 Node\n")
# print("--------------------------\n")
# printShip(popState.ship)
# print("Level 2\n")
# print("--------------------------\n")
# expandUnload(popState, heap)
# for i in repeatedStates:
#     print("Repeated States:")
#     printShip(i)

# '''
# Test SIFT in isolation
# '''
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

# '''
# Test reading manifest
# '''
# ship = openFile()
# printShip(ship)

# '''
# Test writing manifest
# Manually check that file is written correctly
# '''
# #Test function
# ship = []
# i = 1
# while i <= 8:
#     j = 1
#     while j <= 12:
#         ship.append(Container((i,j),0,'UNUSED'))
#         j+=1
#     i+=1
#
# ship[0] = Container((1,1),130,'Bob')
# ship[1] = Container((1,2),20,'Bob2')
# ship[2] = Container((1,3),50,'Bob3')
# ship[3] = Container((1,4),20,'Bob4')
# #Test function
# writeManifest("Example_manifest", ship)
