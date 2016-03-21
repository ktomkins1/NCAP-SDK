"""
.. module:: network_interface.py
   :platform: Unix, Windows
   :synopsis: Defines the netowrk interface for ncaplite (e.g. XMPP).

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""

import sys
import sleekxmpp


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
        self.device=None
        self.releaseMe=False
        self.beServer=True
        self.clientJID=None

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0199') # XMPP Ping
        self.broker_address=broker_address

    def run(self):
        # Connect to the XMPP server and start processing XMPP stanzas.
        if self.connect(self.broker_address,reattempt=False):
            # If you do not have the dnspython library installed, you will need
            # to manually specify the name of the server if it does not match
            # the one in the JID. For example, to use Google Talk you would
            # need to use:
            #
            # if xmpp.connect(('talk.google.com', 5222)):
            #     ...
            #self.process(block=True)
            self.process()
            print("Done")
        else:
            print("Unable to connect.")
