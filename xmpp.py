import sleekxmpp
import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase

class Client(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, user):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

        #some variables
        self.user = user

        self.receive = set()
        self.contacts = []

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # Multi-User Chat (MUC)
        self.register_plugin('xep_0096') # File transfer
        self.register_plugin('xep_0065')
        self.register_plugin('xep_0047', {
            'auto_accept': True
        })

        if self.connect():
            print('Sesion Iniciada con el Usuario: %s' % self.user)
            self.process(block=False)
        else:
            print('No es posible conectar con el Server')
    
    def session_start(self, event):
        try:
            print('entro al try')
            self.send_presence()
            roster = self.get_roster()
            for r in roster['roster']['items'].keys():
                self.contacts.append(r)
        except IqError as err:
            print('Error: %s' % err.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print('El servidor tarda en conectar')
            self.disconnect()
    
    def message(self, message):
        user = str(message['from'].user) + '@' + str(message['from'].domain)
        print(user, message['body'])
    
    def logout(self):
        self.disconnect(wait=False)
    
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
            cont = 0
            data = []
            for i in usr_list.findall('.//{jabber:x:data}value'):
                cont += 1
                user_data = ''
                if i.text != None:
                    user_data = i.text
                data.append(user_data)
                if cont == 4:
                    cont = 0
                    print ("|Email: ", data[0], " |JID: ", data[1], " |Username: ", data[2], " |Name: ", data[3])
                    data = []

        except IqError as err:
            print('No se pueden mostrar: %s' % err)
        except IqTimeout:
            print('Servidor tarda mucho en responder...')


        