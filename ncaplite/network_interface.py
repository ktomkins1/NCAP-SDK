"""
.. module:: network_interface.py
   :platform: Unix, Windows
   :synopsis: Defines the netowrk interface for ncaplite (e.g. XMPP).

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""

import sys
import sleekxmpp
import ast

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input


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

    def run(self):
        # Connect to the XMPP server and start processing XMPP stanzas.
        if self.connect(self.broker_address, reattempt=False):
            # self.process(block=True)
            self.process()
            print("Done")
        else:
            print("Unable to connect.")

    @staticmethod
    def tryeval(val):
        """ Try to evalauate the input as python literal.
        Helper function for parsing. """
        try:
            val = ast.literal_eval(val)
        except ValueError:
            pass
        return val

    @staticmethod
    def parse_inbound(msg):
        """ Parse an inbound message from the network interface
        into a tuple of arguments for an IEEE1457-1 function """
        ml = msg.split(",")
        for n, i in enumerate(ml):
            if(';' in i):
                y = i.split(';')
                ml[n] = [NetworkClient.tryeval(i) for i in y]
            else:
                ml[n] = NetworkClient.tryeval(i)
        return(tuple(ml))

    @staticmethod
    def parse_outbound(msg):
        """ Parse a tuple returned by a IEEE1457-1 function into
        a properly formatted string for sending via the
        network interface """
        x = msg
        # make lists semicolon delimited
        x = [';'.join(map(str, i)) if type(i) is list else i for i in x]
        # make x a tuple
        x = tuple(x)
        # turn into a string
        x = str(x)
        # remove all superfluous chars and whitespace from string
        x = x.replace("'", "")
        x = x.replace("(", "")
        x = x.replace(")", "")
        x = "".join(x.split())
        return x
