'''

This module contains the foundation for other modules.


NOTES
- DgData can represent any attribute or common datatype
- DgArrays contain DgData, but themselves are DgData

- DgData takes in attributes, data or DgData, and converts them all to DgData
- DgData then sends that through a build process that yields the new data
- It is important that the data stored with DgData is in its raw state, so it cannot itself be DgData
- The same is true for arrays, the contents will always be raw

Challenges
- Dealing with Compound attributes (Seperate datatype that cannot be connected?)
- 

'''

import pymel.core as pmc

class DgData(object):
    _type = None
    _maxInputs = None
    _defaultInputs = None

    def __new__(cls, *args, **kwargs):
        '''
        We override __new__ in order to return the correct object type.
        '''

        if cls == DgData:

            if len(args) > 1:
                raise ValueError('%s only accepts one input argument.' % cls.__name__)
            if len(args) == 0:
                raise ValueError('%s requires one input argument.' % cls.__name__)

            data = args[0]
            type = getType(data)

            return type.__new__(type, data, *args, **kwargs)

        else:
            return object.__new__(cls, *args, **kwargs)

    def __init__(self, *inputs, **settings):

        # Enforce max inputs
        if self._maxInputs and len(inputs) > self._maxInputs:
            raise ValueError('Input limit reached, %s accepts at most %s inputs.' % (self.__name__, self._maxInputs))

        # Add default inputs if any inputs were omitted
        if self._defaultInputs != None:
            new_inputs = []
            defaultInputs = self._defaultInputs if isinstance(self._defaultInputs, list) else [self._defaultInputs]
            for i, input in enumerate(defaultInputs):
                if len(inputs) <= i:
                    new_inputs.append(input)
                else:
                    new_inputs.append(inputs[i])
            inputs = new_inputs

        # Convert any strings to PyNodes
        inputs = [pmc.PyNode(input) if isinstance(input, basestring) else input for input in inputs ]

        self._data = self.create(*inputs, **settings)

    def create(self, *inputs, **settings):
        ''' 
        This is where we determine the 'data' for the class.
        The arguments here will be DgData instances inputted on init.
        The return should be the resulting data.
        
        For basic classes, this will just pass the inputs.
        For things like functions and constants, nodes will be created here.
        
        Here it is important that the arguments are the inputs, the kwargs are the settings.
        '''
        return inputs[0]

    def __str__(self):
        return self.name()

    def __mul__(self, other):
        return self._wrapWithInput(getFunction('multiply', self.type()))

    def __div__(self, other):
        return self._wrapWithInput(getFunction('divide', self.type()))

    def __add__(self, other):
        return self._wrapWithInput(getFunction('add', self.type()))

    def __sub__(self, other):
        return self._wrapWithInput(getFunction('subtract', self.type()))

    def type(self):
        return self._type

    def data(self):
        return self._data

    def name(self):
        return type(self).__name__

    def isAttr(self):
        return isinstance(self.data(), pmc.general.Attribute)

    def get(self):
        return self.data().get() if self.isAttr() else self.data()

    def set(self, value):
        self._assertSameType(value)
        if self.isAttr():
            self.data().set(value)
        else:
            self._data = value

    def connect(self, other):
        ''' This provides the ability to easily connect with other attributes. '''

        self._assertSameType(other)

        if isinstance(other, DgData) and other.isAttr():
            other = other.data()
        elif isinstance(other, pmc.general.Attribute):
            pass
        elif isinstance(other, basestring):
            other = pmc.PyNode(other)
        else:
            raise ValueError('Connection must be to an attribute.')

        if self.isAttr():
            self.data().connect(other)
        else:
            other.set(self.data())

    def addAttribute(self, name, attribute):
        self.__dict__[name] = attribute

    def createNode(self, *args, **kwargs):
        pass

    def _assertSameType(self, other):
        other_type = getType(other)
        if other_type == type(self):
            return True
        else:
            raise TypeError('%s is incompatable with %s' % (str(other), self.name()))

    def _wrapWithInput(self, function):
        def wrapped_function(*args, **kwargs):
            return function(self, *args, **kwargs)
        return wrapped_function


# Todo should this be removed?
class DgTypedData(DgData):
    ''' An intermediate type that removes DgData's input filtering. '''
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls, *args, **kwargs)


class ArrayData(DgTypedData):

    def get(self):
        pass

    def set(self, value):
        self._assertSameType(value)
        if self.isAttr():
            for i, child in enumerate(self.getChildren()):
                child_data = DgData(child)
                child_data.set(value[i])
                self._data[i] = child_data
        else:
            self._data = value

    def getChildren(self):
        pass

    def connect(self, other):
        pass

    def __getitem__(self, item):
        pass

    def __len__(self):
        pass


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

def getType(data):
    ''' Determines the type of the input data.'''

    if isinstance(data, DgData):
        return type(data)

    if isinstance(data, int) or isinstance(data, float):
        return Float

    # If this is a compound object, just use its data (this way we can determine quaternions)
    try:
        if data.getChildren():
            data = data.getChildren()
    except (RuntimeError, AttributeError):
        pass

    # If data is a list, check what array type it is
    if isinstance(data, list) or isinstance(data, tuple):

        # Determine types of contents
        content_types = []
        for item in data:
            item_type = getType(item)
            if item_type not in content_types:
                content_types.append(item_type)

        if len(content_types) == 1 and content_types[0] == Float:

            length = len(data)
            if length == 3:
                return Vector
            elif length == 4:
                return Quaternion
            elif length == 16:
                return Matrix
            else:
                return ArrayData

        elif len(content_types) > 1:
            return ArrayData

    # If its a string or PyMel object, determine the attribute type
    if isinstance(data, str) or isinstance(data, pmc.general.Attribute):

        if not pmc.objExists(data):
            raise TypeError('Attribute: %s does not exist' % str(data))

        data = pmc.PyNode(data)
        maya_type = data.type()

        if maya_type in ['byte', 'long', 'enum', 'float', 'doubleLinear', 'doubleAngle', 'double', 'bool']:
            return Float
        elif maya_type == 'matrix':
            return Matrix
        elif maya_type in ['double3', 'float3']:
            return Vector
        elif maya_type == 'TdataCompound':
            return Compound
        elif maya_type == None:
            try:
                data.set(1, type='float')
                return Num
            except RuntimeError: pass
            try:
                data.set([0,0,0], type='float3')
                return Vector
            except RuntimeError: pass
            try:
                data.set([0,0,0,0], type='TdataCompound')
                return Quaternion
            except RuntimeError: pass
            try:
                data.set([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], type='matrix')
                return Matrix
            except RuntimeError: pass

    raise TypeError('Could not determine dataType for %s' % str(data))

