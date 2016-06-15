"""
.. module:: simple_json_codec
   :platform: Unix, Windows
   :synopsis: This a simple json codec for encoding / decoding IEEE1451
              requests and responses for the network interface.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
# -*- coding: utf-8 -*-
import ieee1451types as ieee1451
import json


class SimpleJsonCodec(object):

    def __init__(self):
        self.special_args = {"timeout": ieee1451.TimeDuration}

    def encode(self, msg):
        """Encode a message in serializable format to a JSON encoded string
        to be used by the network interface

        Args:
            msg: a message to be encoded which must be of the format
        [message_id, args ] where message_id is the name of the request
        or response and args is a dictionary of arguments in serializable
        format. EG

        ['7217', {
                'ncap_id': 1234,
                'tim_id': 01,
                'channel_id': 01,
                'timeout': {'TimeDuration': {'secs': 0, 'nsecs': 1000}},
                'sampling_mode': 0,
                'data_value': {'ArgumentArray': [
                                {'type_code': 'UINT16_TC',
                                 'value': 1024,
                                 'name': 'ADC1234'}
                                 ]
                                }
                }
        ]


        Returns:
            encoded: A JSON encoded string

        """
        s = self.to_serializable(msg)
        encoded = json.dumps(s)
        return encoded

    def decode(self, s):
        """Decode an inbound message from the network interface
        into arguments for an IEEE1457-1 request.

        Args:
            s: A JSON encoded string to be decoded

        Returns:
            decoded: The original message as a list in the fromat
            message_id, args ] where message_id is the name of the request
            or response and args is a dictionary of arguments. Any arguments
            which are complex IEEE1451 types shall have been decoded into
            instances of their original class.
        """
        msg = json.loads(s)
        decoded = self.from_serializable(msg)
        return decoded

    def to_serializable(self, msg):
        """Convert a message to serializable format.

        Args:
            msg: a message to be encoded which must be of the format
            [message_id, args ] where message_id is the name of the request
            or response and args is a dictionary of arguments which can include
            complex ieee1451Types.

        Returns:
            A list of format [message_id, args ] where message_id is the name
            of the request or response and args is a dictionary of arguments
            where complex ieee1451 any types have been converted to a
            serializable format comprised of built-in types
        """
        d = dict()  # careful not to modify the original
        for key, val in iter(msg[1].items()):
            serializable = getattr(val, "serializable", None)
            if(callable(serializable)):
                s = serializable()
                d[key] = s
            else:
                d[key] = val
        return [msg[0], d]

    def from_serializable(self, s):
        """Convert a message from serializable format to standard format.

        Args:
            s: a message to be deserialized which must be of the format
            [message_id, args ] where message_id is the name of the request
            or response and args is a dictionary of arguments in serializable
            format.
        Returns:
        The deserialized message as a list in the fromat
        [message_id, args ] where message_id is the name of the request
        or response and args is a dictionary of arguments. Any arguments
        which are complex IEEE1451 types shall have been deserialized into
        instances of their original class.
        """
        d = dict()  # careful not to modify the original
        for key, val in iter(s[1].items()):
            if isinstance(val, dict):
                class_name = str(val.keys()[0])
                c = getattr(ieee1451, class_name)
                from_serializable = getattr(c, "from_serializable", None)
                if callable(from_serializable):
                    d[key] = from_serializable(s[1][key])
                else:
                    d[key] = val
            else:
                d[key] = val
        return [s[0], d]

if __name__ == '__main__':
    print(str(type(SimpleJsonCodec)))

