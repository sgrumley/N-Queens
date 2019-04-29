from collections import deque
import copy
import time


def boardInit(n):
    """Initiate empty board"""
    #n = 4
    nBoard = [[0 for i in range(0, n)] for j in range(0, n)]
    return nBoard


def printBoard(board, n):
    for i in range(n):
        print("\n")
        for j in range(n):
            print(board[i][j], "   ", end="", flush=True)
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

""" accepts a state of the board and provides children states """
def getChildren(n, node):
    children = []
    for x in range(n):
        for i in range(n):
            tempBoard = copy.deepcopy(node)
            tempBoard[i][x] = 'Q'
            children.append(tempBoard)
    return children

""" return the amount of queens on the board """
def numQueens(board, n):
    count = 0
    for i in range(n):
            for j in range(n):
                if board[i][j] == 'Q':
                    count += 1
    return count

def BFS():
    frontier = deque()
    explored = []
    soloutions = []
    frontier.append(boardInit(n))
    while len(frontier) > 0:
        node = frontier.pop()
        """ If the first node in the queue is goal state add it to soloutions """
        if numQueens(node, n) == n+1:
            break
        if eval(node, n) == 0 and numQueens(node, n) == n:
            soloutions.append(node)
        """ add explored nodes to a list """
        explored.append(node)
        """ generate chilrdren and add them to the frontier """
        if eval(node,n) == 0:
            children = getChildren(n, node)

            exist = False
            if len(children) > 0:
                for child in children:
                    """ if not in explored """
                    for exp in explored:
                        if child == exp:
                            exist = True
                    if exist == False:
                        frontier.appendleft(child)
    return soloutions



n=5
start = time.time()
sols = BFS()
end = time.time()
totaltime = end - start
for sol in sols:
    printBoard(sol, n)
print("n = ", n)
print("Algorithm: BFS (pruning)")
print("time = ", totaltime)
print("soloutions found = ", len(sols))
