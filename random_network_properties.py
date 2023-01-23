import networkx
from networkx import to_numpy_array
from datetime import datetime
from meteostat import Point, Hourly
from math import sin, cos
import numpy
import random

from random_network import RandomWaterDistributionNetwork


# define classes of material, edge and node for the graph
class Material:
    def __init__(self, pressureTol, tempTol) -> None:
        self.pressureTol = pressureTol
        self.tempTol = tempTol


class Edge(Material):
    def __init__(self, pressureTol, tempTol, length, diameter) -> None:
        super().__init__(pressureTol, tempTol)
        self.length = length
        self.diameter = diameter


def pressure_gen(t):
    return (10 * (0.0572 * cos(4.667 * t) + 0.0218 * cos(12.22 * t)) + 1)


def generateBaseTemps():
    durhamLocation = Point(54.77676, -1.57566, 77)

    startYear = random.randint(2022, 2022)
    startMonth = random.randint(1, 12)
    startDay = random.randint(1, 21)

    coldestList = []
    differencesList = []
    for i in range(7):
        start = datetime(startYear, startMonth, startDay + i)
        end = datetime(startYear, startMonth, startDay + i + 1)
        weatherData = Hourly(durhamLocation, start, end)
        tempsFrame = weatherData.fetch()
        tempsFrame.drop(tempsFrame.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], axis=1, inplace=True)
        tempsFrame = tempsFrame.to_numpy()

        earlyTemps = tempsFrame[:13, :]
        coldest = earlyTemps[:, 0].min()
        coldestList.append(coldest)
        findDifferences = numpy.concatenate(([[0]], earlyTemps[:-1]))
        findDifferences = earlyTemps - findDifferences
        change = findDifferences.min()
        differencesList.append(change)

        lateTemps = tempsFrame[13:, :]
        coldestLate = lateTemps[:, 0].min()
        coldestList.append(coldestLate)
        findDifferencesLate = numpy.concatenate(([[0]], lateTemps[:-1]))
        findDifferencesLate = lateTemps - findDifferencesLate
        changeLate = findDifferencesLate.min()
        differencesList.append(changeLate)

    return coldestList, differencesList


def get_adjacency_matrix_and_edge_count(network: networkx.DiGraph) -> tuple[numpy.ndarray, int]:
    adjacency: numpy.ndarray = to_numpy_array(network)
    return adjacency, len(network.edges)


def random_properties_for_network(network: networkx.DiGraph):
    adjacency_matrix, numEdges = get_adjacency_matrix_and_edge_count(network)
    coldestList, differencesList = generateBaseTemps()
    coldestList = numpy.array(coldestList)
    differencesList = numpy.array(differencesList)
    pipe_properties_over_time = numpy.ndarray((numEdges, 14, 3))
    for i in range(numEdges):
        newColdestList = coldestList + numpy.random.normal(0, 0.5, 14)
        newDifferencesList = differencesList + numpy.random.normal(0, 0.5, 14)
        pipe_properties_over_time[i, :, 0] = (-2 - newColdestList) / (-2)
        pipe_properties_over_time[i, :, 1] = newDifferencesList
        offset = round(random.random() * 10, 3)
        increase = numpy.random.normal(0.5, 1)
        pressures = numpy.empty(14)
        for j in range(14):
            pressures[j] = pressure_gen(j * increase + offset)
        if random.random() > 0.3:
            pipe_properties_over_time[i, :, 2] = (1.5 - pressures) / 1.5
        else:
            pipe_properties_over_time[i, :, 2] = (1.45 - pressures) / 1.45

    return adjacency_matrix, pipe_properties_over_time


if __name__ == "__main__":
    random_network_maker = RandomWaterDistributionNetwork()
    network = random_network_maker.random_network(10, 0, 0)
    adjacency, pipe_props = random_properties_for_network(network)
    print(adjacency, pipe_props)
