# -*- coding: utf-8 -*-

"""
.. module:: ncaplite
   :platform: Unix, Windows
   :synopsis: This is just a stub module while we're framing the project out.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
# - Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.


from urllib import urlopen
import xml.etree.ElementTree as ET

class NCAP(object):
    """ This class defines an NCAP instance.

    Typically, an NCAP will be instantiated first
    prior to calling upon the other 1451-1 services in the SDK.

    """

    def __init__(self, id):
        """

        :param ncap_config: NCAP configuration file path
        :return:
        """
        self.id=id #EUI64
        self.type = "server"
        self.name = "mr. ncap"
        self.model_number=0
        self.serial_number=0
        self.manufacturer_id=0
        self.physical_address=0
        self.protocol_address=0
        self.client_list={}
        self.server_lis={}
        self.server_client_join_list={}
        self.roster_file_path = 'roster.xml'
        self.network_if_msg_handlers={}


    def load_config(self, config_file_path='ncapconfig.xml'):

        tree = ET.parse(config_file_path)
        root = tree.getroot()
        self.roster_file_path=root.find('roster_path').text
        self.broker_ip=root.find('broker_address').find('address').text
        self.broker_port=int(root.find('broker_address').find('port').text)
        self.jid=root.find('ncap_identification').find('jid').text
        self.password=root.find('ncap_identification').find('password').text
        self.id=int(root.find('ncap_identification').find('ncap_id').text)
        self.type=root.find('ncap_identification').find('ncap_type').text
        self.model_number=int(root.find('ncap_identification').find('model_number').text)
        self.serial_number=int(root.find('ncap_identification').find('serial_number').text)
        self.manufacturer_id=int(root.find('ncap_identification').find('manufacturer_id').text)

    def register_network_interface(self,network_interface):
        self.network_interface = network_interface
        self.network_interface.add_event_handler("session_start", self.on_network_if_session_start)
        self.network_interface.add_event_handler("message", self.on_network_if_message)


    def start(self):
        print("NCAP Started")
        self.network_interface.run()

    def stop(self):
        print("NCAP Stoped")
        self.network_interface.disconnect()


    def  on_network_if_message(self, msg):
        """
        Callback for network interface message
        :return:
        """

        if msg['type'] in ('chat', 'normal'):
            print("Got normal chat msg: "+str(msg))
            ip=urlopen('http://icanhazip.com').read()
            msg.reply("Hi I am " + self.boundjid.full + " and I am on IP " + ip).send()
        else:
            print("Got unknown message type: "+str(msg))

    def on_network_if_session_start(self, event):
        """
        Callback for start of new session on the network interface
        :return:
        """


        announce="Network Session Start. I should announce my existance and do some bookeeeping here."
        self.network_interface.send_presence()
        self.network_interface.get_roster()
        print(announce)
