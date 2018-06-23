'''

This module contains all functions for easy importing.

Challenges:
- How do we determine what operation to use on what type
- How do we handle the order of input types


'''

from general import *
import _factories

__functions__ = {
    'multiply': {
        'float': MultiplyFloat,
        'vector': Dot,
        ('float', 'vector'): MultiplyFloatVector
    },
    'cross': Cross,
    'dot': Dot
}

#### OPERATIONS ####

class Multiply(object):
    def __new__(cls, *args):
        return DgData(args[0]) * DgData(args[1])

class MultiplyFloat(object):
    pass

class MultiplyFloatVector(object):
    pass

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


