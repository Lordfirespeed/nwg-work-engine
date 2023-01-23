'''
Inputs:
Pressure tolerance in each pipe
Temperature tolerance in each pipe
History of pressures and temperatures
Where current leaks are

Low pressure could mean a leak

Output predictions for pressure and temperature of the system for each day of the next week
Take average pressure and minimum temperature

1. Use linear regression to find projection of data
2. Use projected data in logistic regression to find 
'''

import numpy
from random_network import RandomWaterDistributionNetwork
from random_network_properties import random_properties_for_network
from sklearn import linear_model


class LeakPredictor:
    def __init__(self, adjacency_matrix: numpy.ndarray, pipe_properties_over_time: numpy.ndarray) -> None:
        self.adjacency = adjacency_matrix
        self.pipe_properties_over_time = pipe_properties_over_time

    def temperature_change_to_break(self, edge_index: int):
        # defining feature matrix(X) and response vector(y)
        coldestTemps = self.pipe_properties_over_time[edge_index, :, 0]
        averagePressures = self.pipe_properties_over_time[edge_index, :, 2]
        X = numpy.column_stack((coldestTemps, averagePressures))
        y = self.pipe_properties_over_time[edge_index, :, 1]

        # create linear regression object
        reg = linear_model.LinearRegression()

        # train model using training sets
        reg.fit(X, y)

        # regression coefficients
        # print('Coefficients', reg.coef_)

        # y-intercept
        return reg.intercept_

    def rank_pipes_by_break_nearity(self):
        pipes = [(index, self.temperature_change_to_break(index)) for index in range(self.pipe_properties_over_time.shape[0])]
        ranked_pipes = sorted(pipes, key=lambda pipe: pipe[1], reverse=True)
        return ranked_pipes


if __name__ == "__main__":
    random_network_maker = RandomWaterDistributionNetwork()
    network = random_network_maker.random_network(10, 0, 0)
    adjacency, pipe_props = random_properties_for_network(network)

    predictor = LeakPredictor(adjacency, pipe_props)
    results = predictor.rank_pipes_by_break_nearity()
    print(results)


