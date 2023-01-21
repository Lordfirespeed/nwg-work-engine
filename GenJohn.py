from network import RandomWaterDistributionNetwork
from networkx import adjacency_matrix
from datetime import datetime
from meteostat import Point, Hourly
from math import sin, cos
import numpy
import random

#define classes of material, edge and node for the graph
class Material:
  def __init__(self,pressureTol, tempTol) -> None:
    self.pressureTol = pressureTol
    self.tempTol = tempTol

class Edge(Material):
  def __init__(self,pressureTol, tempTol, length, diameter) -> None:
    super().__init__(pressureTol, tempTol)
    self.length = length
    self.diameter = diameter
  
class network(RandomWaterDistributionNetwork):
  pass

def pressure_gen(t):
  return (10 * (0.0572 * cos(4.667 * t) + 0.0218 * cos(12.22*t)) + 1)

def generateBaseTemps():
  durhamLocation = Point(54.77676, -1.57566, 77)

  startYear = random.randint(2022,2022)
  startMonth = random.randint(1,12)
  startDay = random.randint(1,21)

  coldestList = []
  differencesList = []
  for i in range(7):
    start = datetime(startYear, startMonth, startDay + i)
    end = datetime(startYear, startMonth, startDay + i + 1)
    weatherData = Hourly(durhamLocation, start, end)
    tempsFrame = weatherData.fetch()
    tempsFrame.drop(tempsFrame.columns[[1,2,3,4,5,6,7,8,9,10]], axis=1, inplace=True)
    tempsFrame = tempsFrame.to_numpy()

    earlyTemps = tempsFrame[:13, :]
    coldest = earlyTemps[:,0].min()
    coldestList.append(coldest)
    findDifferences = numpy.concatenate(([[0]],earlyTemps[:-1]))
    findDifferences = earlyTemps - findDifferences
    change = findDifferences.min()
    differencesList.append(change)

    lateTemps = tempsFrame[13:, :]
    coldestLate = lateTemps[:,0].min()
    coldestList.append(coldestLate)
    findDifferencesLate = numpy.concatenate(([[0]],lateTemps[:-1]))
    findDifferencesLate = lateTemps - findDifferencesLate
    changeLate = findDifferencesLate.min()
    differencesList.append(changeLate)

  return coldestList, differencesList

def makeGraph(numNodes):
  graph = network()
  matrix = graph.random_network(numNodes, 0, 0)
  adjacency = numpy.matrix(adjacency_matrix(matrix).toarray())
  return adjacency, matrix.number_of_edges()

def makeGraphAndTemps(numNodes):
  Amatrix, numEdges = makeGraph(numNodes)
  coldestList, differencesList = generateBaseTemps()
  coldestList = numpy.array(coldestList)
  differencesList = numpy.array(differencesList)
  listOfLists = numpy.ndarray((numEdges, 14, 3))
  for i in range(numEdges):
    newColdestList = coldestList + numpy.random.normal(0, 0.5, 14)
    newDifferencesList = differencesList + numpy.random.normal(0, 0.5, 14)
    listOfLists[i,:,0] = (-2 - newColdestList)/(-2)
    listOfLists[i,:,1] = newDifferencesList
    offset = random.randint(0,10)
    increase = numpy.random.normal(0, 0.5)
    pressures = numpy.empty(14)
    for j in range(14):
      pressures[j] = pressure_gen(j * increase + offset)
    if random.random() > 0.3:
      listOfLists[i,:,2] = (1.6 - pressures)/1.6
    else:
      listOfLists[i,:,2] = (1.5 - pressures)/1.5

  return Amatrix, listOfLists
    
print(makeGraphAndTemps(4))