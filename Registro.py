import sleekxmpp
import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

class RegistrerUser(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('register', self.register)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        self.disconnect()
    
    def register(self, iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password
        
        try:
            res.send(now=True)
            print('Se creo correctamente el usuario: %d' % self.boundjid.user)
            
        except IqError as err:
            print('Error %s' % err.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print('Sin respuesta del server...')
            self.disconnect

    