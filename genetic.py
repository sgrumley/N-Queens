import time
import random
import copy


def boardInit(n):
    """board init"""
    # n = 4
    nBoard = [[0 for i in range(0, n)] for j in range(0, n)]
    """ Initialize queens at random places """
    for i in range(0, n):
        randRow = random.randint(0, n - 1)
        if nBoard[randRow][i] != "Q":
            nBoard[randRow][i] = "Q"
    return nBoard


def printBoard(board, n):
    print("________________")
    for i in range(n):
        print("\n")
        for j in range(n):
            print(board[i][j], "   ", end="", flush=True)
    print("\n", "\n", "fitness Value: ", eval(board, n))
    print("________________")
    print("\n", "\n")


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


def getParents(k, population, n):
    lowestCost = n * 3
    pos1 = 0
    secondLowest = n * 3
    pos2 = 1
    rand = random.randint(0, k - 1)
    for i in range(k):
        currentEval = eval(population[i], n)
        if currentEval < lowestCost:
            if pos1 != pos2:
                lowestCost = currentEval
                pos1 = i
        elif currentEval <= lowestCost:
            secondLowest = currentEval
            pos2 = i
        elif currentEval <= lowestCost + 1:
            print(pos1, pos2)
    print(pos1, pos2)
    # In some cases the lowest was found early and unable to find a second one that was different
    # if (pos1 == pos2):
    #    pos2 = rand
    return pos1, pos2


def CrossOver(pair, pop, k, n):
    randSplitPoint = random.randint(1, n - 2)
    X1 = pop[pair[0]]
    X2 = pop[pair[1]]
    Y1 = [[0 for i in range(0, n)] for j in range(0, n)]
    Y2 = [[0 for i in range(0, n)] for j in range(0, n)]
    for i in range(n):
        for j in range(0, randSplitPoint):
            Y1[i][j] = X1[i][j]
            Y2[i][j] = X2[i][j]
        for m in range(randSplitPoint, n):
            Y1[i][m] = X2[i][m]
            Y2[i][m] = X1[i][m]

    return Y1, Y2


def mutate(Y, n):
    for i in range(n):
        for j in range(n):
            if Y[i][j] == "Q":
                Y[i][random.randint(0, n - 1)] = "Q"
                Y[i][j] = 0
                break


def worstFitness(population, k):
    lowestCost = 0
    pos1 = 0
    secondLowest = 0
    pos2 = 1
    rand = random.randint(0, k - 1)
    for i in range(k):
        currentEval = eval(population[i], n)
        print(currentEval)
        if currentEval > lowestCost:
            if pos1 != pos2:
                lowestCost = currentEval
                pos1 = i
        elif currentEval >= lowestCost:
            secondLowest = currentEval
            pos2 = i
    print(pos1, pos2)
    """ In some cases the lowest was found early and unable to find a second one that was different """
    # if (pos1 == pos2):
    #    pos2 = rand
    return pos1, pos2


def genetic(iter, k, n):
    mutateProb = 0.05
    population = [None] * k
    """ Generate population """
    for j in range(k):
        population[j] = boardInit(n)
    """ Get 2 of the better parents """
    PairOfParents = getParents(k, population, n)
    print(PairOfParents)
    """Create children for the 2 parents """
    Y = CrossOver(PairOfParents, population, k, n)
    if random.random() < mutateProb:
        Y[0] = mutate(Y[0], n)
    elif random.random() < mutateProb:
        Y[1] = mutate(Y[1], n)

    toBeRemoved = worstFitness(population, k)
    print(toBeRemoved)
    newPopulation = [None] * k


iterations = 12
k = 8
n = 4

genetic(iterations, k, n)
