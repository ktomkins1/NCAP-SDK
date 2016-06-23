"""
.. module:: discovery_services
   :platform: Unix, Windows
   :synopsis: Defines Discovery Services for ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""

import xml.etree.ElementTree as ET
import ieee1451types as ieee1451

class DiscoveryServices(object):
    """This class defines the discover services offered by an NCAP.

    .. note::
        Currently the join / unjoin functions use the xmpp roster but
        in reality I don't think these two things should be coupled. We
        need more clarification on the purpose of Join / Unjoin in the
        standard.
    """

    def __init__(self):
        """
        """
        self.client_list = []

    def open_roster(self, roster_path):
        """ Open roster file.
        """
        self.roster_path = roster_path
        with open(self.roster_path, 'r') as f:
            self.tree = ET.parse(self.roster_path)

    def register_transducer_access_service(self, transducer_access):
        """Register a TimDiscovery service object with the\
        TransducerDataAccessServices object."""
        self.transducer_access = transducer_access

    def ncap_client_join(self, client_id):

        """
        Checks to see if user is registered.
        Registers the user if a request is recieved.
        Unsubcribes if reques is recieved.

        returns FALSE for unregistered, TRUE for registered.
        """
        on_roster = 0

        root = self.tree.getroot()

        # Setting our list to an empty array
        jid = []

        # We need to find all of our users in our roster
        # and then we can find the JID attribute
        for user in root.findall('user'):
            jid.append(user.find('jid').text)

        # Check to see if the jid is in our list.
        # If it is, we will respond to the message.
        try:
            jid.index(client_id)
            on_roster = 1
        except:
            # The .index function throws an error if there is no match,
            # so we will use this as our non-subscribed option.
            on_roster = -1
            newuser = ET.Element("user")
            newuser.text = '\n'
            root.append(newuser)
            newuser.set('subscription', 'true')
            jabber = ET.Element("jid")
            newuser.append(jabber)
            jabber.text = '%s' % (client_id)
            # with open(self.roster_path, 'w') as f:
            #    tree.write(f)

        return ((on_roster)*-1, )

    def ncap_client_unjoin(self, client_id):
        """
        Checks to see if user is registered.
        Unregisters the user if a request is recieved.

        returns FALSE for unregistered, TRUE for registered.
        """
        on_roster = 0
        # with open(self.roster_path, 'r') as f:
        #     tree = ET.parse(f)

        root = self.tree.getroot()

        # Setting our list to an empty array
        jid = []

        # find all of our users in our roster and
        # then we can find the JID attribute
        for user in root.findall('user'):
            jid.append(user.find('jid').text)

        # Check to see if the jid is in our list.
        # If it is, we will respond to the message.
        try:
            on_roster = 1
            jid.index(client_id)
        except:
            on_roster = -1

        if on_roster >= 0:
            # find all of our users in roster and then find the JID attribute
            for user in root.findall('user'):
                test12 = (user.find('jid').text)
                if test12 == client_id:
                    root.remove(user)
            self.tree = ET.ElementTree(root)
            # os.remove(self.roster_path)
            # with open(self.roster_path, 'w') as f:
            #     tree.write(f)

            return (on_roster, )

    def ncap_tim_discover(self, ncap_id):
        """
        :param ncap_id: the ncap id number
        :return:
            error_code: the error code of type ieee1451types.Error
            num_of_tim: the number of TIMs connected to the ncap (UINT16)
            tim_ids: the list of tim ids for the connected tims
        """
        error_code = ieee1451.Error(
            ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
            ieee1451.ErrorCode.NO_ERROR)

        comrep = self.transducer_access.report_comm_module()

        comm_ids = comrep['module_ids']
        error_code = comrep['error_code']

        tim_ids = []
        for id in comm_ids:
            timrep = self.transducer_access.report_tims(id)
            error_code = timrep['error_code']
            tim_ids = tim_ids + timrep['tim_ids']

        num_of_tim = len(tim_ids)

        result = {'error_code': error_code,
                  'num_of_tim': num_of_tim,
                  'tim_ids': tim_ids}

        return result

    def ncap_transducer_discover(self, ncap_id, tim_id):
        """
        :param ncapId: the ncap id to query
        :param timId: the tim id to query
        :return:
            error_code: the error code of type ieee1451types.Error
            ncap_id: the queried ncap id
            tim_id: the tim id to queried for transducer channels
            num_of_transducer_channels: the number of connected transducer channels reported in the id list
            transducer_channel_ids: the list of transducer channel ids for the queried tim
            transducer_channel_names: the list of transducer channel names for the queried tim
        """
        error_code = ieee1451.Error(
            ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
            ieee1451.ErrorCode.NO_ERROR)

        chanrep = self.transducer_access.report_channels(tim_id)

        error_code = chanrep['error_code']
        trans_channel_ids = chanrep['channel_ids']
        num_trans_channels = len(trans_channel_ids)
        channel_names = chanrep['channel_names']

        result = {'error_code': error_code,
                  'ncap_id': 1234,
                  'tim_id': tim_id,
                  'num_of_transducer_channels': num_trans_channels,
                  'trans_channel_ids': trans_channel_ids,
                  'trans_channel_names': channel_names}

        return result
