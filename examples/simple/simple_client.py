#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ncaplite import ncaplite
from ncaplite import network_interface
from ncaplite import discovery_services
from ncaplite import transducer_data_access_services
from ncaplite import transducer_services_base
from ncaplite import ieee1451types as ieee1451
from ncaplite import simple_json_codec
from ncaplite import teds_access_services
from ncaplite import teds_support
import time
import logging
import logging.config
import sys

logger = logging.getLogger(__name__)

def client_on_data(msg):
    logger.info(msg['body'])

def custom_handler_thread(self, request, sender_info, function):
        """handler_thread generalizes the actions taken by the thread
        created by the handle_message function."""
        try:
            logger.debug('NCAPClient.handler_thread')
            if type(request) == list:
                #result = function(**request[1])
              logger.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
              logger.info(str(request))
            else:
                logger.info("==============================================")
                logger.info(str(request))
                #result = function(*request[1:])
        except Exception as e:
           logger.error("NCAP.handler_thread Exception: "+str(e))


def on_tim_discovery_response(response):
    if response['error_code'] == ieee1451.ErrorCode.NO_ERROR:
        print(response)

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    logger.info("Running Simple NCAP Client Demo...")

    #create client

    ncap_client = ncaplite.NCAP()
    ncap_client.load_config("clientconfig.xml")
    ncap_client.type = "client"
    client_jid = 'unittest@ncaplite.loc'
    client_password = 'mypassword'
    client_if = network_interface.NetworkClient(
        client_jid, client_password, (ncap_client.broker_ip, ncap_client.broker_port))
    client_if.codec = simple_json_codec.SimpleJsonCodec()
    ncap_client.register_network_interface(client_if)

    # monkey-patch the custom message handlers
    ncap_client.on_network_if_message = client_on_data
    #ncap_client.handler_thread = custom_handler_thread

    #start client
    ncap_client.start()
    time.sleep(.5)

    #discover tims
    request = [716, {'ncap_id': 1234,}]

    msg = ncap_client.network_interface.codec.encode(request)
    ncap_client.network_interface.send_message(
                                mto="ncap@ncaplite.loc", mbody=msg, mtype='chat')
    time.sleep(10)



    #discover tims

    #discover channels

    #get teds

    #read data

    #write data

    ncap_client.stop()

if __name__ == '__main__':
    main()
