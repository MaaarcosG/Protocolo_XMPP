import sleekxmpp

import logging

from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
from sleekxmpp.plugins.xep_0096 import stanza, File

class RegistrerUser(ClientXMPP):

    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("register", self.register_user)

        self.register_plugin('xep_0030')
        self.register_plugin('xep_0004')
        self.register_plugin('xep_0066')
        self.register_plugin('xep_0077') 

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        self.disconnect()

    def register_user(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
        
        try:
            #print('ENTRO AL TRY')
            resp.send(now=True)
            print('Se creo correctamente el usuario: %d' % self.boundjid.user)
        except IqError as e:
            print("Error: %s" % e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print("No response from server.")
            self.disconnect()
