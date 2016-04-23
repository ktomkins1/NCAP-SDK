"""
.. module:: discovery_services
   :platform: Unix, Windows
   :synopsis: Defines Discovery Services for ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""

import xml.etree.ElementTree as ET
import os

class DiscoveryServices(object):

    def __init__(self, roster_path):
        """
        """
        self.client_list=[]
        self.roster_path=roster_path
        with open(self.roster_path, 'r') as f:
            self.tree = ET.parse(self.roster_path)

    def ncap_client_join(self, client_id):

        """
        Checks to see if user is registered.
        Registers the user if a request is recieved.
        Unsubcribes if reques is recieved.

        returns FALSE for unregistered, TRUE for registered.
        """
        print("ncap_client_join: "+str(client_id))
        on_roster=0

        root = self.tree.getroot()

        # Setting our list to an empty array
        jid = []

        #We need to find all of our users in our roster and then we can find the JID attribute
        for user in root.findall('user'):
            jid.append(user.find('jid').text)


        # Check to see if the jid is in our list. If it is, we will respond to the message.
        try:
            jid.index(client_id)
            on_roster = 1
        except:
            # The .index function throws an error if there is no match, so we will use this as
            #our non-subscribed option.
            on_roster = -1
            print('Subscription Request Recieved')
            newuser = ET.Element("user")
            newuser.text = '\n'
            root.append(newuser)
            newuser.set('subscription', 'true')
            jabber=ET.Element("jid")
            newuser.append(jabber)
            jabber.text='%s' %(client_id)
            #with open(self.roster_path, 'w') as f:
            #    tree.write(f)


        return (on_roster)*-1

    def ncap_client_unjoin(self, client_id):
        """
        Checks to see if user is registered.
        Unregisters the user if a request is recieved.

        returns FALSE for unregistered, TRUE for registered.
        """
        print("ncap_client_unjoin: "+str(client_id))
        on_roster = 0
        # with open(self.roster_path, 'r') as f:
        #     tree = ET.parse(f)

        root = self.tree.getroot()

        # Setting our list to an empty array
        jid = []

        #find all of our users in our roster and then we can find the JID attribute
        for user in root.findall('user'):
            jid.append(user.find('jid').text)

        print(jid)
        # Check to see if the jid is in our list. If it is, we will respond to the message.
        try:
            on_roster = 1
            jid.index(client_id)
            print("unjoin: on roster")
        except:
            on_roster = -1
            print("unjoin: not on roster")

        if on_roster >= 0:
            print('unjoin: Request Recieved')
            # find all of our users in roster and then find the JID attribute
            for user in root.findall('user'):
                test12 = (user.find('jid').text)
                if test12 == client_id:
                    print("found:" + str(test12))
                    root.remove(user)
            self.tree = ET.ElementTree(root)
            # os.remove(self.roster_path)
            # with open(self.roster_path, 'w') as f:
            #     tree.write(f)

            return on_roster
