#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ncaplite import ncaplite
from ncaplite import network_interface
from ncaplite import discovery_services
from ncaplite import transducer_data_access_services
from ncaplite import simple_json_codec
import simple_transducer_service
import logging
import logging.config
import sys
import time

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    logger.info("Running Simple NCAP Server Demo...")

    config_file_path = 'ncapconfig.xml'
    roster_path = 'roster.xml'

    tdisco = simple_transducer_service.TimDiscoverySimple()

    ncap = ncaplite.NCAP()
    ncap.load_config(config_file_path)
    network_if = network_interface.NetworkClient(
            ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
    network_if.codec = simple_json_codec.SimpleJsonCodec()
    ncap.register_network_interface(network_if)
    discovery = discovery_services.DiscoveryServices()
    discovery.open_roster(roster_path)
    ncap.register_discovery_service(discovery)
    discovery.register_transducer_access_service(tdisco)

    ncap.start()
    logger.info("NCAP STARTED...")

    time.sleep(10)

    ncap.stop()

if __name__ == '__main__':
    main()
