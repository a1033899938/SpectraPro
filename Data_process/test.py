import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsEllipseItem
M = np.zeros((4,4)) # NB M is never a matrix; that would create issues, as then all the vectors must be matrices
M[0:3, 0:3] = [[1,2,3],[4,5,6],[7,8,9]] # We calibrate the conversion of displacements and store it
M[3, 0:3] = 99 # Ensure that the datum pixel transforms to here.
M[3, 3] = 1.0

a = [[1,2,3],[4,5,6]]
print(a)
print(np.shape(a))