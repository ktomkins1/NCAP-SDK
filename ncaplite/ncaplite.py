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
import logging
import xml.etree.ElementTree as ET
import thread

logger = logging.getLogger(__name__)


class NCAP(object):
    """ This class defines an NCAP instance.

    Typically, an NCAP will be instantiated first
    prior to calling upon the other 1451-1 services in the SDK.

    """

    def __init__(self, name="NCAP"):
        """

        :param ncap_config: NCAP configuration file path
        :return:
        """
        self.id = 0  # EUI64
        self.type = "server"
        self.name = name
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
        """

        :param config_file_path:
        :return:
        """
        logger.debug('NCAP.load_config')
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
        """Register a NetworkInterface object with the NCAP

        :param network_interface:
        :return:
        """
        logger.debug('NCAP.register_network_interface')
        self.network_interface = network_interface
        self.network_interface.add_event_handler(
                            "session_start", self.on_network_if_session_start)
        self.network_interface.add_event_handler(
                                        "message", self.on_network_if_message)

    def register_discovery_service(self, discovery):
        """Register a DiscoveryService object with the NCAP

        :param discovery:
        :return:
        """
        logger.debug('NCAP.register_network_interface')
        self.discovery_service = discovery
        self.message_handlers[7108] = self.discovery_service.ncap_client_join
        self.message_handlers[7109] = self.discovery_service.ncap_client_unjoin
        self.message_handlers[716] = self.discovery_service.ncap_tim_discover
        self.message_handlers[717] = self.discovery_service.ncap_transducer_discover

    def register_transducer_data_access_service(self, transducer_access):
        """Register a TransducerDataAccessService object with the NCAP

        :param transducer_access:
        :return:
        """
        logger.debug('NCAP.register_transducer_data_access_service')
        self.transducer_access = transducer_access
        self.message_handlers[7211] = self.transducer_access.\
            read_transducer_sample_data_from_a_channel_of_a_tim
        self.message_handlers[7217] = self.transducer_access.\
            write_transducer_sample_data_to_a_channel_of_a_tim

    def register_teds_access_service(self, teds_access):
        """Register a TedsAccessService object with the NCAP

        :param teds_access:
        :return:
        """
        logger.debug('NCAP.register_teds_access_service')
        self.teds_access = teds_access
        self.message_handlers[732] = self.teds_access.\
            read_transducer_channel_teds
        self.message_handlers[733] = self.teds_access.\
            read_user_transducer_name_teds

    def start(self):
        logger.debug('NCAP.start')
        self.network_interface.run()

    def stop(self):
        logger.debug('NCAP.stop')
        self.network_interface.disconnect()

    def on_network_if_message(self, msg):
        """
        Callback for network interface message
        :return:
        """
        logger.debug('NCAP.on_network_if_message')
        if msg['type'] in ('chat', 'normal'):
            if self.type == "server":
                self.handle_message(msg)

    def on_network_if_session_start(self, event):
        """
        Callback for start of new session on the network interface
        :return:
        """
        logger.debug('NCAP.on_network_if_session_start')
        self.network_interface.send_presence()
        self.network_interface.get_roster()

    def handle_message(self, msg):
        """
        Dispatcher for handling messages

        Args:
            msg: a message passed down from the NetworkClient
        """
        logger.debug('NCAP.handle_message')
        sender = ('from', msg['from'])
        request = self.network_interface.parse_inbound(msg['body'])

        logger.debug('NCAP.handle_message: '+str(request))
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
        try:
            logger.debug('NCAP.handler_thread')

            if type(request) == list:
                result = function(**request[1])
                response = [request[0], result]
                msg = self.network_interface.parse_outbound(response)
            else:
                response = function(*request[1:])
                msg = str(request[0]) + \
                    ',' + self.network_interface.parse_outbound(response)

            logger.debug('NCAP.handler_thread response: '+str(msg))

            self.network_interface.send_message(
                            mto=str(sender_info[1]), mbody=msg, mtype='chat')
        except Exception as e:
           logger.error("NCAP.handler_thread Exception: "+str(e))
