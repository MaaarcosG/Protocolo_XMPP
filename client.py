import sleekxmpp

import logging
import threading

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
from sleekxmpp.plugins.xep_0096 import stanza, File

class Client(ClientXMPP):
    def __init__(self, jid, password, username):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler('message', self.message)

        self.user = username
        self.received = set()
        self.contacts = []

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0096') # File transfer 
        self.register_plugin('xep_0047', {
            'auto_accept': True
        })

    def session_start(self, event):
        try:
            self.send_presence()
            roster = self.get_roster()
            for r in roster['roster']['items'].keys():
                self.contacts.append(r)   
        except IqError as e:
            print("Error: %s" % e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print("El server se ha tardado")
            self.disconnect()
    
    def logout(self):
        self.disconnect(wait=True)

    def message(self, msg):
        pass
    
    def list_user(self):
        user = self.Iq()
        user['type'] = 'set'
        user['id'] = 'search_result'
        user['to'] = 'search.redes2020.xyz'
        user['from'] = self.boundjid.bare

        items = ET.fromstring("<query xmlns='jabber:iq:search'> \
                                <x xmlns='jabber:x:data' type='submit'> \
                                    <field type='hidden' var='FORM_TYPE'> \
                                        <value>jabber:iq:search</value> \
                                    </field> \
                                    <field var='Username'> \
                                        <value>1</value> \
                                    </field> \
                                    <field var='search'> \
                                        <value>*</value> \
                                    </field> \
                                </x> \
                              </query>")

        user.append(items)
        try:
            usr_list = user.send()
            print(usr_list)

        except IqError as err:
            print('No se pueden mostrar: %s' % err)

        except IqTimeout:
            print('Servidor tarda mucho en responder...')