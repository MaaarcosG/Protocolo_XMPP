import sleekxmpp
import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase



class Client(ClientXMPP):
    def __init__(self, username, password):
        print('Entry')
        ClientXMPP.__init__(self, username, password)
        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('message', self.message)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # Multi-User Chat (MUC)
        self.register_plugin('xep_0096') # File transfer

    def session_start(self, event):
        try:
            self.get_roster()
            print(self.get_roster())
        except IqError as err:
            logging.error('Error obteniendo el roster')
            logging.error(err.iq['error']['condition'])
            self.disconnect()
        except IqTimeout:
            logging.error('Servidor tarda mucho en responder...')
            self.disconnect

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply('Thanks for sending:\n%(body)s' % msg).send()
    

if __name__ == '__main__':
    DOMAIN = '@redes2020.xyz'
    USER = 'MarcosPruebas'
    PASS = 'marcos1234'
    
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(message)s')
    
    clientxmpp = Client(USER+DOMAIN, PASS)
    clientxmpp.connect()
    clientxmpp.process(block=True)



        