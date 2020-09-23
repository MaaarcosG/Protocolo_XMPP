import sleekxmpp
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase
from sleekxmpp.plugins.xep_0096 import stanza, File

class RegistrerUser(ClientXMPP):

    def __init__(self, jid, password, name):
        ClientXMPP.__init__(self, jid, password)
        self.name = name
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
        resp['register']['name'] = self.name
        
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
            
class Client(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler('message', self.message)

        self.user = jid[0:-14]
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
            #print('Entro al entry, funcion')
            self.send_presence()
            roster = self.get_roster()
            #print(roster)
            for r in roster['roster']['items'].keys():
                self.contacts.append(r)  
                #print(self.contacts) 
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
        usr_list = user.send()
        data = []
        temp = []
        cont = 0
        for i in usr_list.findall('.//{jabber:x:data}value'):
            cont += 1
            txt = ''
            if i.text == None:
                txt = 'None'
            else:
                txt = i.text
            
            temp.append(txt)
            if cont == 4:
                cont = 0
                data.append(temp)
                temp = []

        return data
    
    def add_user(self, jid):
        self.send_presence_subscription(pto=jid)
    
    def info_user(self, jid):
        user = self.Iq()
        user['type'] = 'set'
        user['id'] = 'search_result'
        user['to'] = 'search.redes2020.xyz'
        user['from'] = self.boundjid.bare

        items = ET.fromstring("<query xmlns='jabber:iq:search'>\
                    <x xmlns='jabber:x:data' type='submit'>\
                    <field type='hidden' var='FORM_TYPE'>\
                        <value>jabber:iq:search</value>\
                    </field>\
                    <field var='Username'>\
                        <value>1</value>\
                    </field>\
                    <field var='search'>\
                        <value>"+jid+"</value>\
                    </field>\
                </x>\
                </query>")

        user.append(items)
        info = user.send()
        #print(info['value'])
        data = []
        temp = []
        cont = 0
        for i in info.findall('.//{jabber:x:data}value'):
            cont += 1
            txt = ''
            if i.text == None:
                txt = 'None'
            else:
                txt = i.text
            
            temp.append(txt)
            if cont == 4:
                cont = 0
                data.append(temp)
                temp = []

        return data

    def delete(self):
        account = self.make_iq_set(ito='redes2020.xyz', ifrom=self.boundjid.user)
        items = ET.fromstring("<query xmlns='jabber:iq:register'> <remove/> </query>")
        account.append(items)
        res = account.send()
        if res['type'] == 'result':
            print('Cuenta Eliminada correctamente')
        
