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
from sklearn import datasets, linear_model, metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import classification_report, confusion_matrix

aMatrix, listOfLists = gj.makeGraphAndTemps(6)
print("AMatrix", aMatrix)
print("ListOfLists:", listOfLists) # Coldest temp recorded, largest difference in temp, average pressure (per 12 hours). Each represents
# listOflists contains data example as a matrix for each edge

# defining feature matrix(X) and response vector(y)
X = listOfLists[0, ]

#Splitting X and y into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1)

#create linear regression object
reg = linear_model.LinearRegression()

#train model using training sets
reg.fit(X_train, y_train)

#regression coefficients
print('Coefficients', reg.coef_)

#Variance score: 1 means perfect prediction
print('Variance score: {}'.format(reg.score(X_test, y_test)))

#plot for residual error
## set plot style
plt.style.use('fivethirtyeight')

##plotting residual errors in training data
plt.scatter(reg.predict(X_train), reg.predict(X_train) - y_train, color='blue', s=10, label='Test data')

##plotting line for zero residual error
plt.hlines(y=0, xmin=0, xmax=50, linewidth=2)

##plotting legend
plt.legend(loc='upper right')

##plot title
plt.title('Residual errors')

##Show plot
plt.show()
'''
x = np.arange(10).reshape(-1,1)
y = np.array([0,0,0,0,1,1,1,1,1,1])

model1 = LinearRegression().fit(x,y)

model2 = LogisticRegression(solver='liblinear', random_state=0)
model2.fit(x,y)

plt.scatter(x,y)
plt.show()
'''



