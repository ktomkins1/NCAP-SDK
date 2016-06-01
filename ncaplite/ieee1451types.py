"""
.. module:: ieee1451types
   :platform: Unix, Windows
   :synopsis: Defines the common data types for IEEE1451
   used by ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
from collections import namedtuple
from enum import Enum

TimeRepresentation = namedtuple('TimeRepresentation',['secs','nsecs'])
TimeDuration = namedtuple('TimeDuration',['secs','nsecs'])
Error   = namedtuple('Error', ['source','code'])

class ErrorSource (Enum):
    """Defines the IEEE1451 Error Source Enumerations."""
    ERROR_SOURCE_LOCAL_0          = 0
    ERROR_SOURCE_LOCAL_X          = 1
    ERROR_SOURCE_REMOTE_X         = 2
    ERROR_SOURCE_REMOTE_0         = 3
    ERROR_SOURCE_APPLICATION      = 4

class ErrorCode(Enum):
    """Defines the IEEE1451 Error Code Enumerations"""
    NO_ERROR                    = 0
    INVALID_COMMID              = 1
    UNKNOWN_DESTID              = 2
    TIMEOUT                     = 3
    NETWORK_FAILURE             = 4
    NETWORK_CORRUPTION          = 5
    MEMORY                      = 6
    QOS_FAILURE                 = 7
    MCAST_NOT_SUPPORTED         = 8
    UNKNOWN_GROUPID             = 9
    UNKNOWN_MODULEID            = 10
    UNKNOWN_MSGID               = 11
    NOT_GROUP_MEMBER            = 12
    ILLEGAL_MODE                = 13
    LOCKED_RESOURCE             = 14
    FATAL_TEDS_ERROR            = 15
    NON_FATAL_TEDS_ERROR        = 16
    CLOSE_ON_LOCKED_RESOURCE    = 17
    LOCK_BROKEN                 = 18
    NETWORK_RESOURCE_EXCEEDED   = 19
    MEMORY_RESOURCE_EXCEEDED    = 20
