
import pymel.core as pmc


def getDgDataType(data):
    ''' Determines the type of the input data.'''

    from general import DgData, DgArray
    from datatypes import Float, Vector, Matrix, Quaternion

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
            item_type = getDgDataType(item)
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
                return DgArray

        elif len(content_types) > 1:
            return DgArray

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
            except RuntimeError:
                pass
            try:
                data.set([0, 0, 0], type='float3')
                return Vector
            except RuntimeError:
                pass
            try:
                data.set([0, 0, 0, 0], type='TdataCompound')
                return Quaternion
            except RuntimeError:
                pass
            try:
                data.set([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], type='matrix')
                return Matrix
            except RuntimeError:
                pass

    raise TypeError('Could not determine dataType for %s' % str(data))



def getOperation(operation_name, *args, **kwargs):
    import functions

    operation = None
    reversed = False

    if operation_name not in functions.__functions__:
        raise ValueError('Operations "%s" not found.' % operation_name)

    value = functions.__functions__[operation_name]
    if not isinstance(value, dict):
        operation = value

    if operation == None:

        dataTypes = []
        for arg in args:
            dataType = getDgDataType(arg).type()
            if dataType not in dataTypes:
                dataTypes.append(dataType)

        dataTypes = tuple(dataTypes) if len(dataTypes) > 1 else dataTypes[0]

        if dataTypes in value:
            operation = value[dataTypes]

        if operation == None:

            dataTypes = dataTypes[::-1]

            if dataTypes in value:
                operation = value[dataTypes]
                reversed = True

    if operation == None:
        raise TypeError('%s does not support input dataType "%s".' % (operation, dataTypes))

    return operation(*args[::-1], **kwargs) if reversed else operation(*args, **kwargs)


def addConnection(source, destination):
    '''
    This allows for a variety of inputs to be connected to a destination plug.
    '''

    from general import DgData
    from datatypes import Matrix

    # First off, the source and destination must be the same type
    sourceType = getDgDataType(source)
    destinationType = getDgDataType(destination)
    if sourceType != destinationType:
        raise TypeError('Source "%s" cannot be connected to destination "%s"' % (source, destination))

    # Convert from DgData
    source = source.data() if isinstance(source, DgData) else source
    destination = destination.data() if isinstance(destination, DgData) else destination

    # Convert strings to PyNodes
    source = pmc.PyNode(source) if isinstance(source, basestring) else source
    destination = pmc.PyNode(destination) if isinstance(destination, basestring) else destination

    if sourceType.isArray():
        if sourceType == Matrix and isinstance(destination, list):
            raise TypeError('Matrix sources must be set with attributes not lists.')

        if isinstance(source, list) and isinstance(destination, list):
            for i in range(len(source)):
                addConnection(source[i], destination[i])

        elif isinstance(source, pmc.general.Attribute) and isinstance(destination, pmc.general.Attribute):
            source.connect(destination)

        elif isinstance(source, pmc.general.Attribute):
            for i, child in enumerate(source.getChildren()):
                addConnection(child, destination[i])

        elif isinstance(source, list):
            for i, child in enumerate(destination.getChildren()):
                addConnection(source[i], child)

        else:
            raise TypeError('Could not add connection for %s and %s' % (source, destination))

    else:

        # The source however can be many types, so we need to determine whether it is an attribute or value
        source = source.data() if isinstance(source, DgData) else source
        if isinstance(source, basestring):
            pmc.PyNode(source).connect(destination)
        elif isinstance(source, pmc.general.Attribute):
            source.connect(destination)
        else:
            destination.set(source)
















