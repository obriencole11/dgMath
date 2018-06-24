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

from functools import partial

import pymel.core as pmc
import _factories

class DgData(object):
    _type = None
    _isArray = False
    _isConstant = False

    @classmethod
    def type(cls):
        return cls._type

    @classmethod
    def isArray(cls):
        return cls._isArray

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
            type = _factories.getDgDataType(data)

            return type.__new__(type, data, *args, **kwargs)

        else:
            return object.__new__(cls)

    def __init__(self, *args, **kwargs):

        # Assign the name if one is provided
        if 'name' in kwargs:
            self._name = kwargs.pop('name')
        elif 'n' in kwargs:
            self._name = kwargs.pop('n')
        else:
            self._name = type(self).__name__ or self.type()

        # Grab constant state if provided
        if 'constant' in kwargs:
            self._isConstant = True
            kwargs.pop('constant')

        _data = self.create(*args, **kwargs)

        if isinstance(_data, DgData):
            _data = _data.data()

        self.addAttribute('output', _data)

        self._data = _data

    def create(self, *args, **kwargs):

        if self.isConstant():
            return self.createConstant()
        else:
            return args[0]

    def createConstant(self):
        raise NotImplementedError('%s does not support constant creation.' % type(self).__name__)

    def __str__(self):
        return self.name()

    def isConstant(self):
        return self._isConstant

    def data(self):
        return self._data

    def name(self):
        return self._name

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

        _factories.addConnection(self.data(), other)

    def addAttribute(self, name, attributes, input=None):
        self.__dict__[name] = attributes

        attributes = attributes if isinstance(attributes, list) else [attributes]

        for attribute in attributes:
            if input != None:
                self.connectInput(input, attribute)

    def connectInput(self, source, destination):
        '''
        
        :param source: Some type of data to connect to the destination.
        :param destination: A PyNode destination attribute.
        :return: 
        '''

        if source == None:
            return None

        _factories.addConnection(source, destination)


    def createNode(self, type, **kwargs):
        node = pmc.createNode(type, **kwargs)
        name = '%s_%s' % (self.name(), type)
        node.rename(name)
        return node

    def _assertSameType(self, other):
        other_type = _factories.getDgDataType(other)
        if isinstance(self, other_type):
            return True
        else:
            raise TypeError('%s is incompatable with %s' % (str(other), self.name()))

    def _wrapWithInput(self, function):
        ''' This wraps the input function '''
        def wrapped_function(*args, **kwargs):
            return function(self, *args, **kwargs)
        return wrapped_function


class DgArray(DgData):
    _isArray = True

    def __getitem__(self, item):
        if self.isAttr():
            return self.data().getChildren()[item]
        else:
            return self.data()[item]

    def __len__(self):
        if self.isAttr():
            return self.data().numChildren()
        else:
            return len(self.data())


class Constant(object):

    def __new__(cls, *args, **kwargs):
        kwargs['constant'] = True
        return DgData(*args, **kwargs)
