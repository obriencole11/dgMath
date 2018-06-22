'''

This module contains all functions for easy importing.

'''

from general import *


#### OPERATIONS ####

class Multiply(object):
    def __new__(cls, *args):
        return DgData(args[0]) * DgData(args[1])


#### GENERAL ####

class Abs(Number):
    pass

class OneMinus(Number):
    pass

class AverageNumber(Number):
    pass


#### TRIGONOMETRY ####

class Sin(Number):
    pass

class Cos(Number):
    pass


#### VECTOR MATH ####

class AddVector(Vector):
    pass

class Dot(Vector):
    pass

class Cross(Vector):
    pass


#### MATRIX MATH ####

class AddMatrix(Matrix):
    pass

class MultMatrix(Matrix):
    pass


