# -*- coding: utf-8 -*-

"""
.. module:: ncaplite
   :platform: Unix, Windows
   :synopsis: This module defines the top-level NCAP object to be
              used in the user application.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
# - Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.

import xml.etree.ElementTree as ET
import thread


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
        self.id = id  # EUI64
        self.type = "server"
        self.name = "mr. ncap"
        self.model_number = 0
        self.serial_number = 0
        self.manufacturer_id = 0
        self.physical_address = 0
        self.protocol_address = 0
        self.client_list = {}
        self.server_list = {}
        self.server_client_join_list = {}
        self.roster_file_path = 'roster.xml'
        self.message_handlers = {}

    def load_config(self, config_file_path='ncapconfig.xml'):

        tree = ET.parse(config_file_path)
        root = tree.getroot()
        self.roster_file_path = root.find('roster_path').text
        self.broker_ip = root.find('broker_address').find('address').text
        self.broker_port = int(root.find('broker_address').find('port').text)
        self.jid = root.find('ncap_identification').find('jid').text
        self.password = root.find('ncap_identification').find('password').text
        self.id = int(root.find('ncap_identification').find('ncap_id').text)
        self.type = root.find('ncap_identification').find('ncap_type').text
        self.model_number = int(root.find('ncap_identification').
                                find('model_number').text)
        self.serial_number = int(root.find('ncap_identification').
                                 find('serial_number').text)
        self.manufacturer_id = int(root.find('ncap_identification').
                                   find('manufacturer_id').text)

    def register_network_interface(self, network_interface):
        self.network_interface = network_interface
        self.network_interface.add_event_handler(
                            "session_start", self.on_network_if_session_start)
        self.network_interface.add_event_handler(
                                        "message", self.on_network_if_message)

    def register_discovery_service(self, discovery):
        print('Registered Discovery Service')
        self.discovery_service = discovery

        self.message_handlers[7108] = self.discovery_service.ncap_client_join
        self.message_handlers[7109] = self.discovery_service.ncap_client_unjoin

    def register_transducer_data_access_service(self, transducer_access):
        print('Registered Transducer Data Access Service')
        self.transducer_access = transducer_access
        self.message_handlers[7211] = self.transducer_access.\
            read_transducer_sample_data_from_a_channel_of_a_tim
        self.message_handlers[7212] = self.transducer_access.\
            read_transducer_block_data_from_a_channel_of_a_tim
        self.message_handlers[7213] = self.transducer_access.\
            read_transducer_sample_data_from_multiple_channels_of_a_tim
        self.message_handlers[7214] = self.transducer_access.\
            read_transducer_block_data_from_multiple_channels_of_a_tim
        self.message_handlers[7217] = self.transducer_access.\
            write_transducer_sample_data_to_a_channel_of_a_tim
        self.message_handlers[7218] = self.transducer_access.\
            write_transducer_block_data_to_a_channel_of_a_tim

    def start(self):
        print("NCAP Started")
        self.network_interface.run()

    def stop(self):
        print("NCAP Stoped")
        self.network_interface.disconnect()

    def on_network_if_message(self, msg):
        """
        Callback for network interface message
        :return:
        """
        if msg['type'] in ('chat', 'normal'):
            if self.type == "server":
                print("Server got normal chat msg: "+str(msg))
                self.handle_message(msg)
            else:
                print("Client got normal chat msg: "+str(msg))
        else:
            print("Got unknown message type: "+str(msg))

    def on_network_if_session_start(self, event):
        """
        Callback for start of new session on the network interface
        :return:
        """
        announce = "Network Session Start."
        self.network_interface.send_presence()
        self.network_interface.get_roster()
        print(announce)

    def handle_message(self, msg):
        """
        Dispatcher for handling messages

        Args:
            msg: a message passed down from the NetworkClient
        """
        sender = ('from', msg['from'])
        request = self.network_interface.parse_inbound(msg['body'])

        # deal w/ the special case for join/unjoin
        if request[0] in [7108, 7109]:
            request = (request[0], sender[1])

        print("Request :" + str(request))
        thread.start_new_thread(self.handler_thread,
                                (request,
                                 sender,
                                 self.message_handlers[request[0]])
                                )

    def handler_thread(self, request, sender_info, function):
        """handler_thread generalizes the actions taken by the thread
        created by the handle_message function. We call the appropriate
        1451-1 service with the appropriate arguments. Once the service
        returns a response, we parse the reponse into an outgoing message
        for the network interface and send a reply to the client.

        Args:
            request:     The request passed down from handle_message
            sender_info: The information about where to send the reply
                         via the network interface.
            function:    The function to be called which provides the
                         appropriate 1451-1 service.
        """
        response = function(*request[1:])
        msg = str(request[0]) + \
            ',' + self.network_interface.parse_outbound(response)
        self.network_interface.send_message(
                        mto=str(sender_info[1]), mbody=msg, mtype='chat')
