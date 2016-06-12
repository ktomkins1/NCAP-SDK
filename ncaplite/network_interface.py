"""
.. module:: network_interface.py
   :platform: Unix, Windows
   :synopsis: Defines the netowrk interface for ncaplite (e.g. XMPP).

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""

import sys
import sleekxmpp
import ast
import ieee1451types as ieee1451

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input


class DefaultCodec():
    """The default codec for IEEE1451-1 messages"""
    def encode(self, msg):
        """ Encode a response returned by a IEEE1457-1 function into
        a properly formatted string for sending via the
        network interface """
        x = msg

        x = [[i.source.value, i.code.value]
             if type(i) is ieee1451.Error else i for i in x]

        x = [i.to_tuple()
             if type(i) is ieee1451.ArgumentArray else i for i in x]

        # make lists and tuples semicolon delimited
        x = [';'.join(map(str, i)) if((type(i) is list) or (type(i) is tuple))
             else i for i in x]

        # make x a tuple
        x = tuple(x)
        # turn into a string
        x = str(x)
        # remove all superfluous chars and whitespace from string
        x = x.replace("'", "")
        x = x.replace("(", "")
        x = x.replace(")", "")
        x = "".join(x.split()).rstrip(',')
        return x
        return ""

    def decode(self, msg):
        """ Decode an inbound message from the network interface
        into arguments for an IEEE1457-1 request"""
        ml = msg.split(",")
        for n, i in enumerate(ml):
            if(';' in i):
                y = i.split(';')
                ml[n] = [self.tryeval(i) for i in y]
            else:
                ml[n] = self.tryeval(i)
        return(tuple(ml))

    def tryeval(self, val):
        """ Try to evalauate the input as python literal.
        Helper function for parsing. """
        try:
            val = ast.literal_eval(val)
        except ValueError:
            pass
        return val


class NetworkClient(sleekxmpp.ClientXMPP):
    """
    A client that implements the 1451-4 interface
    using sleekxmpp. This will be probably be abstracted
    away more using an ABC later.

    """

    def __init__(self, jid, password, broker_address=tuple()):

        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.device = None
        self.releaseMe = False
        self.beServer = True
        self.clientJID = None

        self.register_plugin('xep_0030')  # Service Discovery
        self.register_plugin('xep_0004')  # Data Forms
        self.register_plugin('xep_0060')  # PubSub
        self.register_plugin('xep_0199')  # XMPP Ping
        self.broker_address = broker_address
        self.codec = DefaultCodec()

    def run(self):
        # Connect to the XMPP server and start processing XMPP stanzas.
        if self.connect(self.broker_address, reattempt=False):
            # self.process(block=True)
            self.process()
        else:
            print("Unable to connect.")

    def parse_inbound(self, msg):
        """Use the codec bound to this object to
        decode/parse an inbound message"""
        return self.codec.decode(msg)

    def parse_outbound(self, msg):
        """Use the codec bound to this object to
        encode/parse an outbound message"""
        return self.codec.encode(msg)
