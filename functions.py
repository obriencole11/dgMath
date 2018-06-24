'''

This module contains all functions for easy importing.

Challenges:
- How do we determine what operation to use on what type
- How do we handle the order of input types


'''

# TODO Operations to add:
# Lerp
# Slerp
# Wave
# Noise
# ATan2
# Log?


import unittest
import pymel.core as pmc

from general import *
from datatypes import *
import _factories

#### OPERATIONS ####

class Add(object):
    def __new__(cls, *args, **kwargs):
        return DgData(args[0]).add(*args[1:], **kwargs)

class Subtract(object):
    def __new__(cls, *args, **kwargs):
        return DgData(args[0]).subtract(*args[1:], **kwargs)

class Multiply(object):
    def __new__(cls, *args, **kwargs):
        return DgData(args[0]).multiply(*args[1:], **kwargs)

class Divide(object):
    def __new__(cls, *args, **kwargs):
        return DgData(args[0]).divide(*args[1:], **kwargs)

class Negate(object):
    def __new__(cls, *args, **kwargs):
        return DgData(args[0]).negate(**kwargs)

class Average(object):
    def __new__(cls, *args, **kwargs):
        return _factories.getOperation('average', *args, **kwargs)

class Distance(object):
    def __new__(cls, *args, **kwargs):
        return _factories.getOperation('distance', *args, **kwargs)

class Normalize(object):
    def __new__(cls, *args, **kwargs):
        return _factories.getOperation('normalize', *args, **kwargs)

class Inverse(object):
    def __new__(cls, *args, **kwargs):
        return _factories.getOperation('inverse', *args, **kwargs)


#### Float ####

class AddFloat(Float):
    def create(self, *args, **kwargs):
        node = self.createNode('plusMinusAverage')

        for i, arg in enumerate(args):
            self.connectInput(arg, node.input1D[i])

        input_attr = args if isinstance(args, list) else args[0]
        self.addAttribute('input', input_attr)

        return node.output1D

class SubtractFloat(Float):

    def create(self, *args, **kwargs):
        node = self.createNode('plusMinusAverage')
        node.operation.set(2)

        for i, arg in enumerate(args):
            self.connectInput(arg, node.input1D[i])

        input_attr = args if isinstance(args, list) else args[0]
        self.addAttribute('input', input_attr)

        return node.output1D

class MultiplyFloat(Float):

    def create(self, input1=0.0, input2=1.0, **kwargs):
        node = self.createNode('multiplyDivide')

        self.addAttribute('input1', node.input1X, input=input1)
        self.addAttribute('input2', node.input2X, input=input2)

        return node.outputX

class DivideFloat(Float):
    def create(self, input1=0.0, input2=1.0, **kwargs):
        node = self.createNode('multiplyDivide')
        node.operation.set(2)

        self.addAttribute('input1', node.input1X, input=input1)
        self.addAttribute('input2', node.input2X, input=input2)

        return node.outputX

class Pow(Float):
    def create(self, input=1, power=2.0, **kwargs):
        node = self.createNode('multiplyDivide')
        node.operation.set(3)

        self.addAttribute('input', node.input1X, input=input)
        self.addAttribute('power', node.input2X, input=power)

        return node.outputX

class Sqrt(Float):
    def create(self, input=1, **kwargs):
        node = self.createNode('multiplyDivide')
        node.operation.set(3)
        node.input2X.set(0.5)

        self.addAttribute('input', node.input1X, input=input)

        return node.outputX

class Abs(Float):
    def create(self, input=-1, **kwargs):

        pow = self.createNode('multiplyDivide')
        pow.operation.set(3)
        pow.input2X.set(2.0)

        self.addAttribute('input', pow.input1X, input=input)

        sqrt = self.createNode('multiplyDivide')
        sqrt.operation.set(3)
        pow.outputX.connect(sqrt.input1X)
        sqrt.input2X.set(0.5)

        return sqrt.outputX

class NegateFloat(Float):

    def create(self, input):
        node = self.createNode('multiplyDivide')
        node.input2X.set(-1)

        self.addAttribute('input', node.input1X, input=input)

        return node.outputX

class FloatAverage(Float):

    def create(self, *args):
        node = self.createNode('plusMinusAverage')
        node.operation.set(3)

        for i, arg in enumerate(args):
            self.connectInput(arg, node.input1D[i])

        input_attr = args if isinstance(args, list) else args[0]
        self.addAttribute('input', input_attr)

        return node.output1D

class Degrees(Float):

    def create(self, input):
        node = self.createNode('multiplyDivide')
        node.input2X.set(57.2958)

        self.addAttribute('input', node.input1X, input=input)

        return node.outputX

class Radians(Float):
    def create(self, input):
        node = self.createNode('multiplyDivide')
        node.input2X.set(0.0174533)

        self.addAttribute('input', node.input1X, input=input)

        return node.outputX

class OneMinus(Float):
    def create(self, input):
        node = self.createNode('plusMinusAverage')
        node.operation.set(2)
        node.input1D[0].set(1.0)

        self.connectInput(input, node.input1D[1])

        self.addAttribute('input', input)

        return node.output1D

class Round(Float):
    def create(self, input):
        node = self.createNode('network')
        node.addAttr('integer', at='byte')

        self.addAttribute('input', node.integer, input)
        return node.integer

class Floor(Float):
    def create(self, input):
        add = self.createNode('plusMinusAverage')
        self.addAttribute('input', add.input1D[0], input)
        add.input1D[1].set(-0.5)

        node = self.createNode('network')
        node.addAttr('integer', at='byte')
        add.output1D.connect(node.integer)

        return node.integer

class Ceil(Float):
    def create(self, input):
        add = self.createNode('plusMinusAverage')
        self.addAttribute('input', add.input1D[0], input)
        add.input1D[1].set(0.5)

        node = self.createNode('network')
        node.addAttr('integer', at='byte')
        add.output1D.connect(node.integer)

        return node.integer


#### TRIGONOMETRY ####

class Sin(Float):

    def create(self, input=0.0, degrees=False):

        mult_node = self.createNode('multiplyDivide')

        if degrees:
            mult_node.input1X.set(2.0)
        else:
            mult_node.input1X.set(2.0 * 57.2958)

        self.connectInput(input, mult_node.input2X)
        self.addAttribute('input', input)

        quat_node = self.createNode('eulerToQuat')
        mult_node.outputX.connect(quat_node.inputRotateX)

        return quat_node.outputQuatX

class Cos(Float):

    def create(self, input=0.0, degrees=False):

        mult_node = self.createNode('multiplyDivide')

        if degrees:
            mult_node.input1X.set(2.0)
        else:
            mult_node.input1X.set(2.0 * 57.2958)

        self.connectInput(input, mult_node.input2X)
        self.addAttribute('input', input)

        quat_node = self.createNode('eulerToQuat')
        mult_node.outputX.connect(quat_node.inputRotateX)

        return quat_node.outputQuatW

class Tan(Float):

    def create(self, input=0.0, degrees=False):

        mult_node = self.createNode('multiplyDivide')

        if degrees:
            mult_node.input1X.set(2.0)
        else:
            mult_node.input1X.set(2.0 * 57.2958)

        self.connectInput(input, mult_node.input2X)
        self.addAttribute('input', input)

        quat_node = self.createNode('eulerToQuat')
        mult_node.outputX.connect(quat_node.inputRotateX)

        divide_node = self.createNode('multiplyDivide')
        divide_node.operation.set(2)
        quat_node.outputQuatX.connect(divide_node.input1X)
        quat_node.outputQuatW.connect(divide_node.input2X)

        return divide_node.outputX


#### VECTOR MATH ####

class AddVector(Vector):
    def create(self, *args, **kwargs):
        node = self.createNode('plusMinusAverage')

        for i, arg in enumerate(args):
            self.connectInput(arg, node.input3D[i])

        input_attr = args if isinstance(args, list) else args[0]
        self.addAttribute('input', input_attr)

        return node.output3D

class SubtractVector(Vector):
    def create(self, *args, **kwargs):
        node = self.createNode('plusMinusAverage')
        node.operation.set(2)

        for i, arg in enumerate(args):
            self.connectInput(arg, node.input3D[i])

        input_attr = args if isinstance(args, list) else args[0]
        self.addAttribute('input', input_attr)

        return node.output3D

class MultiplyFloatVector(Vector):

    def create(self, inputFloat=2.0, inputVector=(1,0,0)):
        node = self.createNode('multiplyDivide')

        self.addAttribute('input1', [node.input1X, node.input1Y, node.input1Z], input=inputFloat)
        self.addAttribute('input2', node.input2, input=inputVector)

        return node.output

class Dot(Float):

    def create(self, input1=(0,1,0), input2=(1,0,0)):
        node = self.createNode('vectorProduct')
        node.operation.set(1)

        self.addAttribute('input1', node.input1, input=input1)
        self.addAttribute('input2', node.input2, input=input2)

        return node.outputX

class Cross(Vector):
    def create(self, input1=(0,1,0), input2=(1,0,0), normalize=True):
        node = self.createNode('vectorProduct')
        node.operation.set(2)
        node.normalizeOutput.set(normalize)

        self.addAttribute('input1', node.input1, input=input1)
        self.addAttribute('input2', node.input2, input=input2)

        return node.output

class VectorDistance(Float):

    def create(self, input1=(0,1,0), input2=(0,0,0)):
        node = self.createNode('distanceBetween')

        self.addAttribute('input1', node.point1, input1)
        self.addAttribute('input2', node.point2, input2)

        return node.distance

class VectorAverage(Vector):

    def create(self, *args):
        node = self.createNode('plusMinusAverage')
        node.operation.set(3)

        for i, arg in enumerate(args):
            self.connectInput(arg, node.input3D[i])

        input_attr = args if isinstance(args, list) else args[0]
        self.addAttribute('input', input_attr)

        return node.output3D

class VectorNormalize(Vector):
    def create(self, input=(0,2,0)):
        node = self.createNode('vectorProduct')
        node.operation.set(0)
        node.normalizeOutput.set(True)

        self.addAttribute('input', node.input1, input=input)

        return node.output

class VectorNegate(Vector):

    def create(self, input):
        node = self.createNode('multiplyDivide')
        node.input1.set([-1, -1, -1])
        self.addAttribute('input', node.input2, input=input)

        return node.output

class Length(Float):
    def create(self, input=(1,0,0)):
        node = self.createNode('distanceBetween')
        node.point2.set([0,0,0])

        self.addAttribute('input', node.point1, input)

        return node.distance


#### MATRIX MATH ####

class ComposeMatrix(Matrix):
    '''
    We want to use this like:
    
    matrix = ComposeMatrix(translate=[0,1,0], rotate=[0,90,0])
    
    '''

    def create(self, translate=None, rotate=None, scale=None,
               quaternion=None, shear=None, rotateOrder=0, useEulerRotation=True):

        node = self.createNode('composeMatrix')
        node.useEulerRotation.set(useEulerRotation)

        self.addAttribute('translate', node.inputTranslate, translate)
        self.addAttribute('rotate', node.inputRotate, rotate)
        self.addAttribute('scale', node.inputScale, scale)
        self.addAttribute('quaternion', node.inputQuat, quaternion)
        self.addAttribute('shear', node.inputShear, shear)
        self.addAttribute('rotateOrder', node.inputRotateOrder, rotateOrder)

        return node.outputMatrix

class MultiplyMatrix(Matrix):

    def create(self, *args, **kwargs):
        node = self.createNode('multMatrix')

        for i, arg in enumerate(args):
            self.connectInput(arg, node.matrixIn[i])

        self.addAttribute('input', args)

        return node.matrixSum

class AddMatrix(Matrix):
    def create(self, *args, **kwargs):
        node = self.createNode('addMatrix')

        for i, arg in enumerate(args):
            self.connectInput(arg, node.matrixIn[i])

        self.addAttribute('input', args)

        return node.matrixSum

class MatrixDistance(Float):

    def create(self, input1=(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),
               input2=(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1)):
        node = self.createNode('distanceBetween')

        self.addAttribute('input1', node.inMatrix1, input1)
        self.addAttribute('input2', node.inMatrix2, input2)

        return node.distance

class DecomposeMatrix(Vector):

    def create(self, input, rotateOrder=0):

        node = self.createNode('decomposeMatrix')
        self.addAttribute('input', node.inputMatrix, input)

        self.addAttribute('translate', node.outputTranslate)
        self.addAttribute('rotate', node.outputRotate)
        self.addAttribute('scale', node.outputScale)
        self.addAttribute('quaternion', node.outputQuat)
        self.addAttribute('shear', node.outputShear)
        self.addAttribute('rotateOrder', node.inputRotateOrder)

        return [node.outputTranslate, node.outputRotate, node.outputScale]

class MultiplyVectorMatrix(Vector):
    def create(self, inputVector=(1,0,0), inputMatrix=(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1)):
        node = self.createNode('vectorProduct')
        node.operation.set(3)

        self.addAttribute('inputVector', node.input1, inputVector)
        self.addAttribute('inputMatrix', node.matrix, inputMatrix)

        return node.output

class InverseMatrix(Matrix):
    def create(self, input):
        node = self.createNode('inverseMatrix')
        self.addAttribute('input', node.inputMatrix, input)
        return node.outputMatrix

class Transpose(Matrix):
    def create(self, input):
        node = self.createNode('transposeMatrix')
        self.addAttribute('input', node.inputMatrix, input)
        return node.outputMatrix

class Matrix4x4(Matrix):

    def create(self, *args):

        if len(args) != 16:
            raise ValueError('Matrix4x4 requires exactly 16 float inputs')

        node = self.createNode('fourByFourMatrix')

        index = 0
        for i in range(4):
            for j in range(4):
                name = 'in%s%s' % (str(i), str(j))
                self.addAttribute(name, node.attr(name), args[index])
                index += 1

        return node.output


#### Quaternion MATH ####

class AddQuaternion(Quaternion):
    def create(self, input1, input2):
        node = self.createNode('quatAdd')
        self.addAttribute('input1', node.input1Quat, input1)
        self.addAttribute('input2', node.input2Quat, input2)
        return node.outputQuat

class MultiplyQuaternion(Quaternion):
    def create(self, input1, input2):
        node = self.createNode('quatProd')
        self.addAttribute('input1', node.input1Quat, input1)
        self.addAttribute('input2', node.input2Quat, input2)
        return node.outputQuat

class InverseQuaternion(Quaternion):
    def create(self, input):
        node = self.createNode('quatInvert')
        self.addAttribute('input1', node.inputQuat, input)
        return node.outputQuat

class Conjugate(Quaternion):
    def create(self, input):
        node = self.createNode('quatConjugate')
        self.addAttribute('input1', node.inputQuat, input)
        return node.outputQuat

class QuaternionNegate(Quaternion):
    def create(self, input):
        node = self.createNode('quatNegate')
        self.addAttribute('input1', node.inputQuat, input)
        return node.outputQuat

class QuaternionNormalize(Quaternion):
    def create(self, input):
        node = self.createNode('quatNormalize')
        self.addAttribute('input1', node.inputQuat, input)
        return node.outputQuat

class EulerToQuaternion(Quaternion):
    def create(self, input, rotateOrder=0):
        node = self.createNode('eulerToQuat')
        self.addAttribute('input', node.inputRotate, input)
        self.addAttribute('rotateOrder', node.inputRotateOrder, rotateOrder)

        return node.outputQuat

class QuaternionToEuler(Vector):
    def create(self, input, rotateOrder=0):
        node = self.createNode('quatToEuler')
        self.addAttribute('input', node.inputQuat, input)
        self.addAttribute('rotateOrder', node.inputRotateOrder, rotateOrder)
        return node.outputRotate


#### Function Directory ####

__functions__ = {
    'multiply': {
        'float': MultiplyFloat,
        'vector': Dot,
        'quaternion': MultiplyQuaternion,
        'matrix': MultiplyMatrix,
        ('float', 'vector'): MultiplyFloatVector,
        ('vector', 'matrix'): MultiplyVectorMatrix
    },
    'add': {
        'float': AddFloat,
        'vector': AddVector,
        'matrix': AddMatrix,
        'quaternion': AddQuaternion
    },
    'subtract': {
        'float': SubtractFloat,
        'vector': SubtractVector
    },
    'divide': {
        'float': DivideFloat
    },
    'pow': Pow,
    'sqrt': Sqrt,
    'abs': Abs,
    'degrees': Degrees,
    'radians': Radians,
    'round': Round,
    'floor': Floor,
    'ceil': Ceil,
    'negate': {
        'float': NegateFloat,
        'vector': VectorNegate,
        'quaternion': QuaternionNegate
    },
    'average': {
        'float': FloatAverage,
        'vector': VectorAverage
    },
    'distance': {
        'vector': VectorDistance,
        'matrix': MatrixDistance
    },
    'normalize': {
        'vector': VectorNormalize,
        'quaternion': QuaternionNormalize
    },
    'cross': Cross,
    'dot': Dot,
    'length': Length,
    'decompose': DecomposeMatrix,
    'compose': ComposeMatrix,
    'inverse': {
        'matrix': InverseMatrix,
        'quaternion': InverseQuaternion
    },
    'transpose': Transpose,
    'eulerToQuat': EulerToQuaternion,
    'quatToEuler': QuaternionToEuler,
    'conjugate': Conjugate,
    'matrix4x4': Matrix4x4
}


#### TESTS ####

class DataTypeTests(unittest.TestCase):

    def test_add(self):
        self.assertEquals(Add(1.0, 2.0, -1.0, 4.0).get(), 6.0)
        self.assertEquals(Add([0.0,1.0,0.0], [1.0,0.0,1.0]).get(), (1.0,1.0,1.0))
        self.assertEquals(Add([1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1], [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]).get(),
                          (2,0,0,0,0,2,0,0,0,0,2,0,0,0,0,2))

    def test_sub(self):
        self.assertEquals(Subtract(1.0, 2.0, -3.0).get(), 2.0)
        self.assertEquals(Subtract([0.0,1.0,0.0], [1.0,0.0,1.0]).get(), (-1.0,1.0,-1.0))

    def test_multiply(self):
        self.assertEquals(Multiply(2.0, 4.0).get(), 8.0)
        self.assertEquals(Multiply([1, 0, 0], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]).get(), (1, 0, 0))
        self.assertEquals(Multiply([1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1], [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1]).get(),
                          (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1))

    def test_divide(self):
        self.assertEquals(Divide(2.0, 4.0).get(), 0.5)

    def test_pow(self):
        self.assertEquals(Pow(2.0, 2.0).get(), 4.0)
        self.assertEquals(Pow(2.0).get(), 4.0)
        self.assertEquals(Sqrt(4.0).get(), 2.0)

    def test_abs(self):
        self.assertEquals(Abs(1.0).get(), 1.0)
        self.assertEquals(Abs(-1.0).get(), 1.0)

    def test_neg(self):
        self.assertEquals(Negate(1.0).get(), -1.0)
        self.assertEquals(Negate(-1.0).get(), 1.0)
        self.assertEquals(Negate([1.0, 1.0, 1.0]).get(), (-1.0,-1.0,-1.0))

    def test_average(self):
        self.assertEquals(Average(1.0, 2.0, 3.0).get(), 2.0)
        self.assertEquals(Average([0,1,0], [1,0,1]).get(), (0.5,0.5,0.5))

    def test_degrees_radians(self):
        self.assertAlmostEquals(Radians(90.0).get(), 1.5708, places=3)
        self.assertAlmostEquals(Degrees(3.14159).get(), 180.0, places=3)

    def test_oneminus(self):
        self.assertEquals(OneMinus(1.0).get(), 0.0)

    def test_sin(self):
        import math
        self.assertAlmostEquals(Sin(45.0, degrees=True).get(), 0.70710678118, places=3)
        self.assertAlmostEquals(Sin(math.pi / 2.0).get(), 1.0, places=3)

    def test_cos(self):
        import math
        self.assertAlmostEquals(Cos(45.0, degrees=True).get(), 0.70710678118, places=3)
        self.assertAlmostEquals(Cos(math.pi / 2.0).get(), 0.0, places=3)

    def test_tan(self):
        import math
        self.assertAlmostEquals(Tan(45.0, degrees=True).get(), 1.0, places=3)
        self.assertAlmostEquals(Tan(math.pi).get(), 0.0, places=3)

    def test_cross(self):
        self.assertEquals(Cross([0.0,1.0,0.0], [1.0,0.0,0.0]).get(), (0.0,0.0,-1.0))

    def test_dot(self):
        self.assertEquals(Dot([0.0,1.0,0.0], [1.0,0.0,0.0]).get(), 0.0)

    def test_distance(self):

        import pymel.core as pmc
        loc1 = pmc.spaceLocator()
        loc2 = pmc.spaceLocator()
        loc2.tx.set(10.0)

        self.assertEquals(Distance(loc1.translate, loc2.translate).get(), 10.0)
        self.assertEquals(Distance(loc1.worldMatrix, loc2.worldMatrix).get(), 10.0)

    def test_length(self):
        self.assertAlmostEquals(Length([1,1,0]).get(), 1.41421356237, places=3)

    def test_normalize(self):
        self.assertEquals(Normalize([0, 5, 0]).get(), (0, 1, 0))

    def test_round(self):
        self.assertEquals(Round(0.49).get(), 0.0)
        self.assertEquals(Round(0.51).get(), 1.0)
        self.assertEquals(Floor(0.5).get(), 0.0)
        self.assertEquals(Ceil(0.5).get(), 1.0)


    def test_decompose(self):
        loc = pmc.spaceLocator()
        loc.setTranslation([1,2,3])
        loc.setRotation([90,90,90])
        loc.setScale([1,2,3])

        self.assertEquals(Decompose(loc.worldMatrix).translate.get(), (1,2,3))
        self.assertEquals(Decompose(loc.worldMatrix).rotate.get(), (90,90,90))
        self.assertEquals(Decompose(loc.worldMatrix).scale.get(), (1,2,3))

if __name__ == '__main__':
    unittest.main()