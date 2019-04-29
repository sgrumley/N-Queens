import random
import copy
import time


def boardInit(n):
    """board init"""
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
                oldi = i
                oldj = j
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


def countControl(board, n):
    """Check if the problem is solved """
    while(1):
        previousEval = eval(board,n)
        if eval(board, n) != 0:
            """ Check for better moves """
            pos = bestMove(board, n)
            #replace Q on board
            if eval(board, n) == previousEval:
                board[random.randint(0, n - 1)][pos[1]] = "Q"
                board[pos[0]][pos[1]] = 0
            else:
                board[pos[2]][pos[1]] = "Q"
                board[pos[0]][pos[1]] = 0
        else:
            break
    return board

def testFunc(n):
    # Initiate random board
    board = boardInit(n)
    # Print starting state
    print("Start State:")
    printBoard(board, n)
    start= time.time()
    temp = countControl(board, n)
    print("Goal State:")
    printBoard(temp, n)
    end = time.time()
    time1 = end - start
    print("n = ", n)
    print("Algorithm: Hill Climb")
    print("Time taken: ", time1)



n=8
testFunc(n)
