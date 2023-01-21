from network import RandomWaterDistributionNetwork
from networkx import adjacency_matrix
from datetime import datetime
from meteostat import Point, Hourly
import numpy

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

durhamLocation = Point(54.77676, -1.57566, 77)
start = datetime(2019, 1, 1)
end = datetime(2019, 1, 3)
weatherData = Hourly(durhamLocation, start, end)
tempsFrame = weatherData.fetch()
tempsFrame.drop(tempsFrame.columns[[1,2,3,4,5,6,7,8,9,10]], axis=1, inplace=True)
print(tempsFrame)

graph = network()
matrix = graph.random_network(5, 100, 0)
adjacency = numpy.matrix(adjacency_matrix(matrix).toarray())
print(adjacency)