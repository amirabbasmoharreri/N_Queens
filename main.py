import math
import operator
import time
import matplotlib.pyplot as plt
import numpy as np
from random import randint


class Coromozom():
    threat = 0

    def __init__(self, array):
        self.array = array
        self.threat = None

    def __setitem__(self, value):
        self.threat = value


def population(n, populationSize):
    p = []
    counterpop = 0
    while counterpop < populationSize:
        history = []
        counter = 0
        while counter < n:
            adad = randint(0, n - 1)
            if not (adad in history):
                history.append(adad)
                counter += 1
        crom = Coromozom(history)
        p.append(crom)
        counterpop += 1

    return p


def fitnessFunction(lists):
    croms = computingTotalThreat(lists)
    croms.sort(key=operator.attrgetter('threat'))
    return croms


###      Correct

def crossover(n):
    ra = []
    for i in range(2):
        a = randint(0, n - 1)
        if not (a in ra):
            ra.append(a)
    rand = (min(ra), max(ra))

    return rand

def muta(n):
    randindex = []
    for i in range(n):
        a = randint(0, n - 1)
        if not (a in randindex):
            if len(randindex) == 2:
                break
            randindex.append(a)
    return randindex

###   Correct

def parentSelection(allpop, rate):
    p = []
    history = []
    popsize = len(allpop)
    pecent = (rate / 100)
    crosssize = int(popsize * pecent)

    parents = []
    i = 0
    while i < 2:
        fmparent = []
        counter = 0
        while counter < (int(crosssize/2)):
            num = randint(0, popsize - 1)
            fmparent.append(num)
            counter += 1
        parents.append(fmparent)
        i += 1
    j = 0
    while j < 2:
        c = []
        for i in range(0, (int(crosssize/2))):
            c.append(allpop[parents[j][i]])
        p.append(c)
        j += 1

    return p


def surviveSelection(allpop, n):
    allpop.sort(key=operator.attrgetter('threat'))
    num = n * 5
    percent = (20 / 100)
    popsize = int(len(allpop) * percent)
    best = allpop[0:popsize + 1]
    while len(best) < num:
        rand = randint(popsize + 1, len(allpop) - 1)
        best.append(allpop[rand])
    return best


###   Correct

def mutation(childs, rate):
    popsize = len(childs)
    lens = len(childs[0].array)
    randcrom = []
    randindex = []
    pecent = (rate / 100)
    musize = int(popsize * pecent)
    # random coromozoms for mutation
    for i in range(musize):
        randcrom.append(randint(0, popsize - 1))

    for i in randcrom:
        randindex = muta(lens)
        item1 = childs[i].array[randindex[0]]
        item2 = childs[i].array[randindex[1]]
        childs[i].array[randindex[0]] = item2
        childs[i].array[randindex[1]] = item1

    return childs


###   Correct

def computingThreat2x2(point1, point2):
    threatsum = 0
    if point1[0] == point2[0] or point1[1] == point2[1]:
        threatsum += 1

    if abs(point1[0] - point2[0]) == abs(point1[1] - point2[1]):
        threatsum += 1

    return threatsum


###   Correct

def computingTotalThreat(croms):
    sum1 = 0
    popsize = len(croms)
    lens = len(croms[0].array)
    for j in range(0, popsize):
        for i in range(0, lens):
            for g in range(0, lens):
                if not (i == g):
                    value1 = croms[j].array[i]
                    index1 = i
                    value2 = croms[j].array[g]
                    index2 = g
                    point1 = (value1, index1)
                    point2 = (value2, index2)
                    # total of threat cromozom
                    sum1 += computingThreat2x2(point1, point2)
        croms[j].threat = sum1

    return croms


def recombination(allpop, parent):
    lens = len(parent[0][0].array)
    #cross = crossover(lens)
    recomsize = len(parent[0])
    childs = []
    for j in range(0, recomsize):
        cross = crossover(lens)
        child1 = []
        child2 = []
        for i in range(0, lens):
            child1.append(-1)
            child2.append(-1)
        p1 = parent[0][j].array
        p2 = parent[1][j].array

        # creating middle of cromozom childs

        for i in range(cross[0], cross[1] + 1):
            child1[i] = p1[i]
            child2[i] = p2[i]

        # creating next to the childs cromozom

        # creating left-side
        for i in range(0, cross[0]):
            if not p2[i] in child1:
                child1[i] = p2[i]
            if not p1[i] in child2:
                child2[i] = p1[i]

        # creating right-side
        for i in range(cross[1] + 1, lens):
            if not p2[i] in child1:
                child1[i] = p2[i]
            if not p1[i] in child2:
                child2[i] = p1[i]

        # completing childs
        for i in range(0, lens):

            index1 = [j for j in range(len(child2)) if child1[j] == -1]
            index2 = [j for j in range(len(child2)) if child2[j] == -1]

            if not p2[i] in child1:
                if not (len(index1) == 0):
                    child1[index1[0]] = p2[i]
            if not p1[i] in child2:
                if not (len(index2) == 0):
                    child2[index2[0]] = p1[i]

        childs.append(Coromozom(child1))
        childs.append(Coromozom(child2))

    return childs


def addchildstopopulation(allpop, childs):
    for i in range(0, len(childs)):
        allpop.append(childs[i])
    return allpop


def showChessBoard(bestcrom):
    x = []
    y = []
    for i in range(0, len(bestcrom)):
        x.append(bestcrom[i])
        y.append(i)

    chess = []
    for j in range(0, len(bestcrom)):
        v = []
        for i in range(0, len(bestcrom)):
            if j % 2 == 0:
                if i % 2 == 0:
                    v.append(1)
                else:
                    v.append(0)
            else:
                if i % 2 == 0:
                    v.append(0)
                else:
                    v.append(1)
        chess.append(v)
    fig, ax = plt.subplots()
    ax.imshow(chess, interpolation='nearest')
    for i in range(0, len(x)):
        # Use "family='font name'" to change the font
        ax.text(x[i], y[i], u'\u2655', size=30 if (len(x) <= 20) else 12, ha='center', va='center',
                color='black' if (x[i] - y[i]) % 2 == 0 else 'white')

    ax.set(xticks=[], yticks=[])
    ax.axis('image')
    plt.show()
    return


def showfitness(lists):
    plt.plot(lists)
    plt.title("ّFitness Function = " + str(lists[len(lists) - 1]))
    plt.ylabel("Threat")
    plt.xlabel("Iteration")
    plt.show()
    return


##################### starting app from here  ######################


list_ministers = []
bestcrom = []
bestfitness = []


print("enter number of cities 'minimum 4' ")
while True:
    num = int(input())
    if num >= 4:
        break
    else:
        print("try again")

# intializing Coordinates of cities with random

start = time.time()

for j in range(num):
    x = randint(0, num - 1)
    list_ministers.append(x)

print("input the population")
populationSize = int(input())

print("input mutation rates")
mutationRate = int(input())

print("input crossover rates")
crossRate = int(input())

print("list of Ministers")
print(list_ministers)

# ADT allgorithm

i = 0
j = 0
fit1 = 100
fit2 = 200
allPopulation = population(num, populationSize)
allPopulation = fitnessFunction(allPopulation)
bestfitness.append(allPopulation[0].threat)
evaluate = abs(fit1 - fit2)
while not(fit2 == 0):
    if evaluate < 1:
        j += 1
    else:
        j = 0
    print("Generation " + str(i) + "  Fitness: " + str(fit2) + "  Count fitness not change: " + str(j))
    parent = parentSelection(allPopulation, crossRate)
    childs = recombination(allPopulation, parent)
    childs = mutation(childs, mutationRate)
    childs = fitnessFunction(childs)
    allPopulation = addchildstopopulation(allPopulation, childs)
    allPopulation = surviveSelection(allPopulation, populationSize)
    bestcrom.append(allPopulation[0])
    bestfitness.append(allPopulation[0].threat)
    fit2 = bestfitness[len(bestfitness) - 1]
    if len(bestfitness) > 1:
        fit1 = bestfitness[len(bestfitness) - 2]
    evaluate = abs(fit1 - fit2)
    i += 1
bestcrom.sort(key=operator.attrgetter('threat'))
showChessBoard(bestcrom[0].array)
showfitness(bestfitness)
print("Fitness: " + str(fit2))
end = time.time()
print("Runtime of the program is " + str(end-start) + " seconds")