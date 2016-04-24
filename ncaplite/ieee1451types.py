"""
.. module:: transducer_services_base
   :platform: Unix, Windows
   :synopsis: Defines the common data types for IEEE1451
   used by ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""


"""
http://docs.python-guide.org/en/latest/writing/structure/
http://stackoverflow.com/questions/702834/whats-the-common-practice-for-enums-in-python

struct TimeRepresentation {UInt32 secs;
   UInt32  nsecs;
};

 struct TimeDuration {
UInt32 secs;
UInt32 nsecs; };

struct TimeInstance {UInt32 secs;
UInt32
nsecs; };

enum interpretation{
PUI_SI_UNITS
PUI_RATIO_SI_UNITS
PUI_LOG10_SI_UNITS
PUI_LOG10_RATIO_SI_UNITS
PUI_DIGITAL_DATA
PUI_ARBITRARY
}

struct Units {
    UInt8 interpretation;
    UInt8 radians;
    UInt8 steradians;
    UInt8 meters;
    UInt8 kilograms;
    UInt8 seconds;
    UInt8 amperes;
    UInt8 kelvins;
    UInt8 moles;
    UInt8 candelas
    UInt8 Units Extension TEDS Access Code
};

typedef UUID Short [5];


message structure

￼￼￼￼￼￼￼￼￼￼￼Message Type
1 Byte
Type of Message
￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼Message ID
2 Byte
Functionality of the message
￼(readBlockDataFromSingleChannelOfSingleTim)
￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼Session No.
1 Byte
Identifies the current session
Initialized by Client/Server
￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼Sequence No.
2 Byte
Identifies the sequence no.
?
?
￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼Status (error flag)
1 Byte
￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼Priority
1 Byte
Gives node carrying out operation the importance of said operation to allow for
overrides of more important functions
￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼￼

"""
