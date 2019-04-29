#annealing

import random
import copy
import time
import math


def boardInit(n):
    """board init"""
    #n = 4
    nBoard = [[0 for i in range(0, n)] for j in range(0, n)]
    """ Initialize queens at random places """
    for i in range(0, n):
        randRow = random.randint(0, n - 1)
        if nBoard[randRow][i] != "Q":
            nBoard[randRow][i] = "Q"
    return nBoard


def printBoard(board, n):
    for i in range(n):
        print("\n")
        for j in range(n):
            print(board[i][j], "   ", end="", flush=True)
    print()
    print()
    print()



def eval(board, n):
    totalhcost = 0
    totaldcost = 0
    for i in range(0, n):
        for j in range(0, n):
            """ if this node is a queen, calculate all collisions """
            if board[i][j] == "Q":
                # subtract 2 so don't count self
                """ Find sideways and vertical from node(i,j) """
                totalhcost -= 2
                for k in range(0, n):
                    if board[i][k] == "Q":
                        totalhcost += 1
                    if board[k][j] == "Q":
                        totalhcost += 1
                """Find diagonal Colisions from node(i,j)"""
                """ Bottom right diagonal"""
                k, l = i + 1, j + 1
                while k < n and l < n:
                    if board[k][l] == "Q":
                        totaldcost += 1
                    k += 1
                    l += 1
                """Bottom left diagonal"""
                k, l = i + 1, j - 1
                while k < n and l >= 0:
                    if board[k][l] == "Q":
                        totaldcost += 1
                    k += 1
                    l -= 1
                """Top right diagonal """
                k, l = i - 1, j + 1
                while k >= 0 and l < n:
                    if board[k][l] == "Q":
                        totaldcost += 1
                    k -= 1
                    l += 1
                """top left diagonal"""
                k, l = i - 1, j - 1
                while k >= 0 and l >= 0:
                    if board[k][l] == "Q":
                        totaldcost += 1
                    k -= 1
                    l -= 1
    return (totaldcost + totalhcost) / 2


def bestMove(board, n):
    lowestCost = eval(board, n)
    moveConfig = board
    oldi = 0
    newi = 0
    oldj = 0
    for i in range(n):
        for j in range(n):
            """ Find a queen """
            if board[i][j] == "Q":
                for ti in range(n):
                    """if there is no queen in the sqaure create a copy of the board, remove the original queen and add a queen to a new empty space"""
                    if board[ti][j] != "Q":
                        tempBoard = copy.deepcopy(board)
                        tempBoard[i][j] = 0
                        tempBoard[ti][j] = "Q"
                        """ Evaluate the configuration of the board from with the queen in the new space """
                        tempCost = eval(tempBoard, n)
                        """ If they configuration is better, save the configuration details """
                        if tempCost < lowestCost:
                            lowestCost = tempCost
                            #moveConfig = tempBoard
                            oldi = i
                            oldj = j
                            newi = ti
    return oldi, oldj, newi


def countControl(board, n, temperature, coolingRate):
    count = 0
    """ loop until goal state is found or temperature reaches 0"""
    while(1):
        count+=1
        currentNodeEval = eval(board, n)
        if currentNodeEval == 0:
            break
        if temperature == 0:
            return board

        """ temporarily take the best move available """
        pos = bestMove(board, n)
        tempBoard = copy.deepcopy(board)
        tempBoard[pos[2]][pos[1]] = "Q"
        tempBoard[pos[0]][pos[1]] = 0

        """ comapre evaluation of states """
        delta = currentNodeEval - eval(tempBoard, n)

        """ if there is no better move """
        if pos[0] == 0 and pos[1] == 0 and pos[2] == 0 and count > 3:
            j = random.randint(0, n - 1)
            for inQueen in range(n):
                if board[inQueen][j] == "Q":
                    row = j
                    col = inQueen
            """ copy board, get rid of Q and add a random queen """
            randomQBoard = copy.deepcopy(board)
            randCol = random.randint(0, n - 1)
            randomQBoard[randCol][row] = "Q"
            randomQBoard[col][row] = 0

            """ evaluate collisions of new board """
            randomNeighborNode = eval(randomQBoard, n)
            delta = currentNodeEval - randomNeighborNode

            """ simmulated annealing logic """
            if temperature == 0:
                break

            probablity = math.exp((delta/temperature))
            determine = random.random()

            if determine <= probablity:
                board[randCol][row] = "Q"
                board[col][row] = 0

        # if there is a better move, take it
        elif delta > 0:
            nextNodeEval = eval(tempBoard, n)
            delta = currentNodeEval - nextNodeEval
            board[pos[2]][pos[1]] = "Q"
            board[pos[0]][pos[1]] = 0

        temperature = temperature * coolingRate

    return board




def testFunc(n, temperature, coolingRate):
    # Initiate random board
    board = boardInit(n)
    # Print starting state
    print("Initial State:")
    printBoard(board, n)
    #run logic
    temp = countControl(board, n, temperature, coolingRate)
    #if soloution is not complete print fail
    if eval(temp, n) != 0:
        print("failed")
    print("Goal State:")
    printBoard(temp, n)
    return temp


"""
best parameters
temperature = 2
coolingRate = 0.90
"""
#set parameters
temperature = 2
coolingRate = 0.90
n = 8
# capture running time
start = time.time()
testFunc(n, temperature, coolingRate)
end = time.time()
totaltime = end - start
#print results
print("n = ", n)
print("Algorithm: Simulated Annealing")
print("Time take: ", totaltime)
