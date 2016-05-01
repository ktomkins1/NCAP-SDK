#!/usr/bin/python


from ncaplite import ncaplite
from ncaplite import network_interface
from ncaplite import discovery_services
from ncaplite import transducer_data_access_services
import simple_transducer_service


if __name__ == '__main__':

    print("Starting Simple NCAP Demo...")

    config_file_path = 'ncapconfig.xml'

    # create an ncap instance
    ncap = ncaplite.NCAP(12345)

    # load the ncapconfig.xml into the ncap instance
    ncap.load_config(config_file_path)

    # create a network interface instance
    network_if = network_interface.NetworkClient(
            ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))

    # register the network interface with the ncap
    ncap.register_network_interface(network_if)

    # create a discovery services instance
    discovery = discovery_services.DiscoveryServices(
                                                    ncap.roster_file_path)

    # register the discovery service instance with the ncap
    ncap.register_discovery_service(discovery)

    # instantiate a user-defined transducer services object (1451.0)
    tdaccs = simple_transducer_service.TransducerAccessSimple()

    # instantiate a transducer data access services object
    tdas = transducer_data_access_services.\
        TransducerDataAccessServices()

    # register the transducer service instance
    # with the transducer data access service instance
    tdas.register_transducer_access_service(tdaccs)

    # register the transducer data access service with the ncap
    ncap.register_transducer_data_access_service(tdas)

    # start the ncap server
    ncap.start()
