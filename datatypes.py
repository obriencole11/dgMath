from general import DgData, DgArray
import _factories


class Float(DgData):
    _type = 'float'
    _defaultInputs = 0

    def createConstant(self):
        node = self.createNode('network')
        node.addAttr('constant')
        return node.constant

    def multiply(self, *args, **kwargs):
        return _factories.getOperation('multiply', self, *args, **kwargs)

    def __mul__(self, *args, **kwargs):
        return self.multiply(*args, **kwargs)

    def divide(self, *args, **kwargs):
        return _factories.getOperation('divide', self, *args, **kwargs)

    def __div__(self, *args, **kwargs):
        return self.divide(*args, **kwargs)

    def add(self, *args, **kwargs):
        return _factories.getOperation('add', self, *args, **kwargs)

    def __add__(self, *args, **kwargs):
        return self.add(*args, **kwargs)

    def subtract(self, *args, **kwargs):
        return _factories.getOperation('subtract', self, *args, **kwargs)

    def __sub__(self, *args, **kwargs):
        return self.subtract(*args, **kwargs)

    def pow(self, power):
        return _factories.getOperation('pow', self, power)

    def sqrt(self):
        return _factories.getOperation('sqrt', self)

    def abs(self):
        return _factories.getOperation('abs', self)

    def negate(self):
        return _factories.getOperation('negate', self)

    def degrees(self):
        return _factories.getOperation('degrees', self)

    def radians(self):
        return _factories.getOperation('radians', self)

    def round(self):
        return _factories.getOperation('round', self)

    def floor(self):
        return _factories.getOperation('floor', self)

    def ceil(self):
        return _factories.getOperation('ceil', self)


class Vector(DgArray):
    _type = 'vector'
    _defaultInputs = [[0,0,0]]

    def createConstant(self):
        node = self.createNode('network')
        node.addAttr('constant', at='double3')
        node.addAttr('constantX', at='double', parent='constant')
        node.addAttr('constantY', at='double', parent='constant')
        node.addAttr('constantZ', at='double', parent='constant')

        return node.constant

    def add(self, *args, **kwargs):
        return _factories.getOperation('add', self, *args, **kwargs)

    def __add__(self, *args, **kwargs):
        return self.add(*args, **kwargs)

    def subtract(self, *args, **kwargs):
        return _factories.getOperation('subtract', self, *args, **kwargs)

    def __sub__(self, *args, **kwargs):
        return self.subtract(*args, **kwargs)

    def multiply(self, *args, **kwargs):
        return _factories.getOperation('multiply', self, *args, **kwargs)

    def __mul__(self, *args, **kwargs):
        return self.multiply(*args, **kwargs)

    def divide(self, *args, **kwargs):
        return _factories.getOperation('divide', self, *args, **kwargs)

    def __div__(self, other):
        return self.divide(*args, **kwargs)

    def cross(self, *args, **kwargs):
        return _factories.getOperation('cross', self, *args, **kwargs)

    def dot(self, *args, **kwargs):
        return _factories.getOperation('dot', self, *args, **kwargs)

    def distanceTo(self, *args, **kwargs):
        return _factories.getOperation('distance', self, *args, **kwargs)

    def normalize(self, *args, **kwargs):
        return _factories.getOperation('normalize', self, *args, **kwargs)

    def normal(self, *args, **kwargs):
        return _factories.getOperation('normalize', self, *args, **kwargs)

    def negate(self, *args, **kwargs):
        return _factories.getOperation('negate', self, *args, **kwargs)

    def length(self, *args, **kwargs):
        return _factories.getOperation('length', self, *args, **kwargs)

    def magnitude(self, *args, **kwargs):
        return _factories.getOperation('length', self, *args, **kwargs)

    def asQuaternion(self, *args, **kwargs):
        return _factories.getOperation('eulerToQuat', self, *args, **kwargs)

    def asRotationMatrix(self, *args, **kwargs):
        return _factories.getOperation('compose', rotate=self, *args, **kwargs)

    def asTranslationMatrix(self, *args, **kwargs):
        return _factories.getOperation('compose', translate=self, *args, **kwargs)

    def asScaleMatrix(self, *args, **kwargs):
        return _factories.getOperation('compose', scale=self, *args, **kwargs)


class Matrix(DgArray):
    _type = 'matrix'
    _defaultInputs = [[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]]

    def __new__(cls, *args, **kwargs):
        if len(args) == 16 and cls == Matrix:
            return _factories.getOperation('matrix4x4', *args, **kwargs)
        else:
            return DgArray.__new__(cls, *args, **kwargs)

    def createConstant(self):
        node = self.createNode('network')
        node.addAttr('constant', at='matrix')
        return node.constant

    def multiply(self, *args, **kwargs):
        return _factories.getOperation('multiply', self, *args, **kwargs)

    def __mul__(self, *args, **kwargs):
        return self.multiply(*args, **kwargs)

    def add(self, *args, **kwargs):
        return _factories.getOperation('add', self, *args, **kwargs)

    def __add__(self, *args, **kwargs):
        return self.add(*args, **kwargs)

    def distanceTo(self, *args, **kwargs):
        return _factories.getOperation('distance', self, *args, **kwargs)

    def translate(self, *args, **kwargs):
        return _factories.getOperation('decompose', self, *args, **kwargs).translate

    def rotate(self, *args, **kwargs):
        return _factories.getOperation('decompose', self, *args, **kwargs).rotate

    def scale(self, *args, **kwargs):
        return _factories.getOperation('decompose', self, *args, **kwargs).scale

    def quaternion(self, *args, **kwargs):
        return _factories.getOperation('decompose', self, *args, **kwargs).quaternion

    def xAxis(self, *args, **kwargs):
        return _factories.getOperation('multiply', self, [1,0,0], *args, **kwargs)

    def yAxis(self, *args, **kwargs):
        return _factories.getOperation('multiply', self, [0,1,0], *args, **kwargs)

    def zAxis(self, *args, **kwargs):
        return _factories.getOperation('multiply', self, [0,0,1], *args, **kwargs)

    def inverse(self, *args, **kwargs):
        return _factories.getOperation('inverse', self, *args, **kwargs)

    def transpose(self, *args, **kwargs):
        return _factories.getOperation('transpose', self, *args, **kwargs)


class Quaternion(DgArray):
    _type = 'quaternion'
    _defaultInputs = [[0,0,0,0]]

    def createConstant(self):
        node = self.createNode('network')
        node.addAttr('constant', at='compound', numberOfChildren=4)
        node.addAttr('constantX', at='double', parent='constant')
        node.addAttr('constantY', at='double', parent='constant')
        node.addAttr('constantZ', at='double', parent='constant')
        node.addAttr('constantW', at='double', parent='constant')

        return node.constant

    def multiply(self, *args, **kwargs):
        return _factories.getOperation('multiply', self, *args, **kwargs)

    def __mul__(self, *args, **kwargs):
        return self.multiply(*args, **kwargs)

    def add(self, *args, **kwargs):
        return _factories.getOperation('add', self, *args, **kwargs)

    def __add__(self, *args, **kwargs):
        return self.add(*args, **kwargs)

    def asEulerRotation(self, *args, **kwargs):
        return _factories.getOperation('quatToEuler', self, *args, **kwargs)

    def asMatrix(self, *args, **kwargs):
        return _factories.getOperation('compose', quaternion=self, *args, **kwargs)

    def inverse(self, *args, **kwargs):
        return _factories.getOperation('inverse', self, *args, **kwargs)

    def conjugate(self, *args, **kwargs):
        return _factories.getOperation('conjugate', self, *args, **kwargs)

    def normalize(self, *args, **kwargs):
        return _factories.getOperation('normalize', self, *args, **kwargs)

    def normal(self, *args, **kwargs):
        return _factories.getOperation('normalize', self, *args, **kwargs)

    def negate(self, *args, **kwargs):
        return _factories.getOperation('negate', self, *args, **kwargs)


class Compound(DgArray):
    _type = 'compound'
    _defaultInputs = [[]]
