


def getDgDataType(data):
    ''' Determines the type of the input data.'''

    from general import DgData, ArrayData
    from datatypes import Number, Vector, Matrix, Quaternion

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


def getFunction(operation, data):
    import functions
