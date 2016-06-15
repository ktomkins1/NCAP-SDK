"""
.. module:: ieee1451types
   :platform: Unix, Windows
   :synopsis: Defines the common data types for IEEE1451
   used by ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
from enum import Enum


class TimeRepresentation(object):
    """Defines the IEEE1451.0 TimeRepresentation"""
    def __init__(self, secs, nsecs):
        self.secs = secs
        self.nsecs = nsecs

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        """Override equality operation."""
        return self.__dict__ == other.__dict__

    def __cmp__(self, other):
        """Override comparison operation."""
        return self.__dict__ == other.__dict__

    def serializable(self):
        """Return the TimeInstance in a serializable format"""
        return {type(self).__name__: self.__dict__}

    @staticmethod
    def from_serializable(s):
        """Initialize the object from the serializable format"""
        d = s['TimeRepresentation']
        return TimeInstance(**d)


class TimeDuration(TimeRepresentation):
    """Defines the IEEE1451.0 TimeDuration"""
    def __init__(self, secs, nsecs):
        self.secs = secs
        self.nsecs = nsecs

    @staticmethod
    def from_serializable(s):
        """Initialize the object from the serializable format"""
        d = s['TimeDuration']
        return TimeDuration(**d)


class TimeInstance(TimeRepresentation):
    """Defines the IEEE1451.0 TimeInstance"""
    def __init__(self, secs, nsecs):
        self.secs = secs
        self.nsecs = nsecs

    @staticmethod
    def from_serializable(s):
        """Initialize the object from the serializable format"""
        d = s['TimeInstance']
        return TimeInstance(**d)


class ErrorSource (Enum):
    """Defines the IEEE1451 Error Source Enumerations."""
    ERROR_SOURCE_LOCAL_0 = 0
    ERROR_SOURCE_LOCAL_X = 1
    ERROR_SOURCE_REMOTE_X = 2
    ERROR_SOURCE_REMOTE_0 = 3
    ERROR_SOURCE_APPLICATION = 4


class ErrorCode(Enum):
    """Defines the IEEE1451 Error Code Enumerations"""
    NO_ERROR = 0
    INVALID_COMMID = 1
    UNKNOWN_DESTID = 2
    TIMEOUT = 3
    NETWORK_FAILURE = 4
    NETWORK_CORRUPTION = 5
    MEMORY = 6
    QOS_FAILURE = 7
    MCAST_NOT_SUPPORTED = 8
    UNKNOWN_GROUPID = 9
    UNKNOWN_MODULEID = 10
    UNKNOWN_MSGID = 11
    NOT_GROUP_MEMBER = 12
    ILLEGAL_MODE = 13
    LOCKED_RESOURCE = 14
    FATAL_TEDS_ERROR = 15
    NON_FATAL_TEDS_ERROR = 16
    CLOSE_ON_LOCKED_RESOURCE = 17
    LOCK_BROKEN = 18
    NETWORK_RESOURCE_EXCEEDED = 19
    MEMORY_RESOURCE_EXCEEDED = 20


class Error(object):
    """Defines a container class for IEEE1451.0 Errors"""
    def __init__(self, source, code):
        self.source = source
        self.code = code

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        """Override equality operation."""
        return self.__dict__ == other.__dict__

    def __cmp__(self, other):
        """Override comparison operation."""
        return self.__dict__ == other.__dict__


class TypeCode(Enum):
    """IEEE1451.0 TypCode Definitions"""
    UNKNOWN_TC = 0
    UINT8_TC = 1
    UINT16_TC = 2
    UINT32_TC = 3
    FLOAT32_TC = 4
    FLOAT64_TC = 5
    STRING_TC = 6
    OCTET_TC = 7
    BOOLEAN_TC = 8
    TIME_INSTANCE_TC = 9
    TIME_DURATION_TC = 10
    QOS_PARAMS_TC = 11
    UINT8_ARRAY_TC = 12
    UINT16_ARRAY_TC = 13
    UINT32_ARRAY_TC = 14
    FLOAT32_ARRAY_TC = 15
    FLOAT64_ARRAY_TC = 16
    STRING_ARRAY_TC = 17
    OCTET_ARRAY_TC = 18
    BOOLEAN_ARRAY_TC = 19
    TIME_INSTANCE_ARRAY_TC = 20
    TIME_DURATION_ARRAY_TC = 21

    def __str__(self):
        """Override __str__ method to return just the name."""
        return self._name_


class Argument(object):
    """Defines the IEEE1451 Argument generic data container type"""
    def __init__(self, type_code=TypeCode.UNKNOWN_TC, value=None):
        self.value = value
        self.type_code = type_code

    def __eq__(self, other):
        """Override equality operation."""
        return self.__dict__ == other.__dict__

    def __cmp__(self, other):
        """Override comparison operation."""
        return self.__dict__ == other.__dict__

    def __str__(self):
        """Override to __str__ to return dict as string"""
        return str(self.__dict__)

    def serializable(self):
        """Return the Argument in a serializable format"""
        return {'type_code': str(self.type_code), 'value': self.value}

    @staticmethod
    def from_serializable(s):
        """Initialize an argument from it's serializable format"""
        tc = TypeCode[s['type_code']]
        val = s['value']
        return Argument(type_code=tc, value=val)


class ArgumentArray(object):
    """Defines ArgumentArray from 1451.0 standard"""

    def __init__(self):
        self.arguments = dict()
        self.indicies = dict()

    def __eq__(self, other):
        """Override equality operation."""
        return self.__dict__ == other.__dict__

    def __cmp__(self, other):
        """Override comparison operation."""
        return self.__dict__ == other.__dict__

    def __str__(self):
        """Override __str__ method."""
        return str(self.serializable())

    def get_by_name(self, name):
        index = self.indicies[name]
        value = self.arguments[index]
        return value

    def get_by_index(self, index):
        value = self.arguments[index]
        return value

    def put_by_name(self, name, value):
        idx = self.next_index()
        self.arguments[idx] = value
        self.indicies[name] = idx
        return 0

    def put_by_index(self, index, value):
        self.arguments[index] = value
        return 0

    def string_to_index(self, name, value):
        return self.indicies[name]

    def get_names(self, name, value):
        return self.indicies.keys()

    def get_indexes(self, name, value):
        return self.arguments.keys()

    def size(self):
        return len(self.arguments)

    def next_index(self):
        """return the lowest free index value"""
        tmp = self.arguments.keys()
        for idx in range(len(tmp)+1):
            if idx not in tmp:
                return idx

    def to_tuple(self):
        """Convert values in ArgumentArray to tuple"""
        result = []
        s = sorted(self.arguments.items(), key=lambda t: t[0])
        [result.append(entry[1].value) for entry in s]
        return tuple(result)

    def serializable(self):
        """Return the ArgumentArray in a serializable format"""
        s = sorted(self.arguments.items(), key=lambda t: t[0])
        arglist = []
        result = {type(self).__name__: arglist}
        for entry in s:
            name = self.find_name_by_index(entry[0])
            if(name is None):
                name = ""
            arg = entry[1].serializable()
            arg['name'] = name
            result[type(self).__name__].append(arg)
        return result

    @staticmethod
    def from_serializable(s):
        """Initialize the object from the serializable format"""
        aa = ArgumentArray()
        for i, sarg in enumerate(s['ArgumentArray']):
            arg = Argument.from_serializable(sarg)
            aa.put_by_index(i, arg)
            if sarg['name']:
                aa.indicies[sarg['name']] = i
        return aa

    def find_name_by_index(self, idx):
        """If an item has a name, find it by index"""
        result = None
        for key, value in iter(self.indicies.items()):
            if value == idx:
                result = key
        return result
