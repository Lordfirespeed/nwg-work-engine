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

import matplotlib.pyplot as plt
import numpy as np
import GenJohn as gj
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def nearity (nodes):
   for i in range (0, nodes):
      aMatrix, listOfLists = gj.makeGraphAndTemps(nodes)
      # print("AMatrix", aMatrix)
      # print("ListOfLists:", listOfLists) # Coldest temp recorded, largest difference in temp, average pressure (per 12 hours). Each represents
      # listOflists contains data example as a matrix for each edge

      # defining feature matrix(X) and response vector(y)
      coldestTemps = listOfLists[0, : , 0]
      averagePressures = listOfLists[0, : , 2]
      X = np.column_stack((coldestTemps, averagePressures))
      y = listOfLists[0, : , 1]

      #Splitting X and y into training and testing sets

      #create linear regression object
      reg = linear_model.LinearRegression()

      #train model using training sets
      reg.fit(X, y)

      #regression coefficients
      #print('Coefficients', reg.coef_)

      #plot for residual error
      ## set plot style
      plt.style.use('fivethirtyeight')

      ##plotting residual errors in training data
      #plt.scatter(reg.predict(X_train), reg.predict(X_train) - y_train, color='blue', label='Test data', linewidth=3)

      ##plotting line for zero residual error
      #plt.hlines(y=0, xmin=0, xmax=50, linewidth=2)

      ## y-intercept
      print('y-intercept for node', i, "is", reg.intercept_)


nearity(10)
