"""
.. module:: ieee1451types
   :platform: Unix, Windows
   :synopsis: Defines the common data types for IEEE1451
   used by ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
from collections import namedtuple

TimeRepresentation = namedtuple('TimeRepresentation',['secs','nsecs'])
TimeDuration = namedtuple('TimeDuration',['secs','nsecs'])
