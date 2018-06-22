
class Float(DgTypedData):
    _type = 'float'
    _defaultInputs = 0

class Matrix(ArrayData):
    _type = 'matrix'
    _defaultInputs = [[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]]

class Vector(ArrayData):
    _type = 'vector'
    _defaultInputs = [[0,0,0]]

class Quaternion(ArrayData):
    _type = 'quaternion'
    _defaultInputs = [[0,0,0,0]]

class Compound(ArrayData):
    _type = 'compound'
    _defaultInputs = [[]]