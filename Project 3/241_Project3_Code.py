import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# ------ Problem 1(a) ------

with open('walmart_data.txt') as f:  # reading txt file
    lines = f.readlines()  # sets lines variable as a list with each item being a row in the .txt file
    x = [float(line.split(",")[0]) for line in lines]  # sets x values array from .txt file
    y = [float(line.split(",")[1]) for line in lines]  # sets y values array from .txt file
    population = np.array(x)  # converts x array into a numpy array and renames it
    profit = np.array(y)  # converts y array into a numpy array and renames it

plt.scatter(population, profit)  # creates a scatter plot
plt.title("ECE 241 Project 3: Profit vs. Population")  # creates title
plt.xlabel("Population x10000")  # creates x-label
plt.ylabel("Profit x10000")  # creates y-label
# plt.show()

# ------ Problem 1(b) ------

model = LinearRegression().fit(population.reshape((-1, 1)), profit)
b = model.intercept_  # creates variable of the intercept of the line of best fit
m = model.coef_  # creates variable for the slope for the line of best fit
y_pred = model.intercept_ + model.coef_ * x  # creates new array with line of best fit values

# ------ Problem 1(c) ------
plt.plot(population,y_pred)  # plots linear regression
# plt.show()

# ------ Problem 1(d) ------

# The line is a best fit line that accurately represents the scatter plot if it were a linear plot.
# It has roughly half the data points above it and roughly half the data points below it. It basically visualizes
# the linear relationship between the profit and population on the graph.

# ------ Problem 1(e) ------

values = np.array([7.8, 4.4, 4.7, 6.12, 8.55, 6.7, 9.8, 7.01]).reshape((-1,1))  # numpy array of pop values
prof_pred = model.predict(values)  # predicts profits for these pop values
print(prof_pred)

# ------ Problem 1(f) ------

prediction = model.predict(population.reshape((-1,1)))
print(mean_absolute_error(profit, y_pred))


