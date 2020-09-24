import tableprint as tp
from PIL import Image  

import sleekxmpp
import threading
import base64

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
        self.add_event_handler("alert", self.alert)
        self.add_event_handler('wait_presence', self.wait_presence)
        self.add_event_handler('new_user_add', self.new_user_add)
        self.add_event_handler('online', self.online)

        self.user = jid[0:-14]
        self.received = set()
        self.contacts = []
        self.presedence = threading.Event()
        self.rooms = {}
        self.counter = 1

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

    # sign in, in the server
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

    # disconnect to server
    def logout(self):
        print('Clossing XMPP Connection')
        self.disconnect(wait=False)
    
    def alert(self):
        self.get_roster()

    def wait_presence(self, presences):
        if(presences['show'] != "" and presences['from'].bare != self.boundjid.bare):
            msg = presences['from'].bare + " changed status to:  " + presences['show']
            self.received.add(presences['from'].bare)
        
        if len(self.received) >= len(self.client_roster.keys()):
            self.presedence.set()
        else:
            self.presedence.clear()

    def message(self, msg):
        #print(msg['type'])
        if(str(msg['type']) =='chat'):
            if(len(msg['body'])>3000):
                tp.banner('<-------IMAGEN RECIBIDA------->')
                received = message['body'].encode('utf-8')
                received = base64.decodebytes(received)
                with open("imagen.jpg", "wb") as file_path:
                    file_path.write(received)
                print('-----')
            else:
                tp.banner('<-------NUEVO MENSAJE PRIVADO RECIBIDO------->')
                print('De: %s' % str(msg['from']).split('@')[0])
                print('Mensaje: %s ' % msg['body'])
                print('Siga escogiendo una opcion:')

        # message group
        elif(str(msg['type']) =='groupchat'):
            tp.banner('<-------MENSAJE EN LA SALA %s------->' % str(msg['from']).split('@')[0])
            #print(msg['from][0])
            print('De: %s' % str(msg['from']).split('@')[0])
            print('Mensaje: %s ' % msg['body'])
            print('Siga escogiendo una opcion:')

    # send meesage when the connect is successful
    def connection_correct(self):
        if self.connect():
            print('Usuario conectado correctamente: %s' % self.user)
            #self.process(block=False)
        else:
            print('No se puede conectar...!')

    # list all user, wich are on the server
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
        
        #lopps through all users and puts them into a list
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
    
    # add user in contacts
    def add_user(self, jid):
        self.send_presence_subscription(pto=jid)
    
    def new_user_add(self, presence):
        print('TE HA AGREGADO EL USUARIO: %s' % str(presence['from']))
    
    # take de information of user
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

    # delete account of sign in
    def delete(self):
        account = self.make_iq_set(ito='redes2020.xyz', ifrom=self.boundjid.user)
        items = ET.fromstring("<query xmlns='jabber:iq:register'> <remove/> </query>")
        account.append(items)
        res = account.send()
        if res['type'] == 'result':
            print('Cuenta %s Eliminada correctamente' % self.user)

    # send private message to a user 
    def private_message(self, jid, message):
        try:
            self.send_message(mto=jid+'@redes2020.xyz', mbody=message, mfrom=self.boundjid.user, mtype='chat')
            print('Mensaje enviado correctamente, destinatario: %s' % jid)
        except IqError as err:
            print("Error: %s" % err.iq['error']['text'])
        except IqTimeout:
            print("El server se ha tardado")

    # send group message in a room 
    def group_message(self, room, message):
        try:
            self.send_message(mto=room + '@conference.redes2020.xyz', mbody=message, mtype='groupchat')
            print('Mensaje enviado correctamente al ROOM: %s' % room)
        except IqError as err:
            print("Error: %s" % err.iq['error']['text'])
        except IqTimeout:
            print("El server se ha tardado")
    
    # create de room to group message
    def createRoom(self, roomId):
        status= 'READY TO GROUP'
        self.plugin['xep_0045'].joinMUC(roomId+'@conference.redes2020.xyz', self.user, pstatus=status, pfrom=self.boundjid.full, wait=True)
        self.plugin['xep_0045'].setAffiliation(roomId+'@conference.redes2020.xyz', self.boundjid.full, affiliation='owner')
        self.plugin['xep_0045'].configureRoom(roomId+'@conference.redes2020.xyz', ifrom=self.boundjid.full)
    
    # join to room, to group message
    def joinRoom(self, roomId):
        print("JOIN TO GROUP: %s" % roomId)
        status= 'READY TO GROUP'
        self.plugin['xep_0045'].joinMUC(roomId+'@conference.redes2020.xyz', self.user, pstatus=status, pfrom=self.boundjid.full, wait=True)
    
    # send message of presedence
    def presedence_msg(self, status, show):
        self.send_presence(pshow=show, pstatus=status)

    # send notificacion
    def online(self, presence):
        if ('conference' in str(presence['from']).split('@')[1]):
            user = str(presence['from']).split('@')[1].split('/')[1]
            sala = str(msg['from']).split('@')[0]
            print('SE ENCUENTRA EN: %' % (user, sala))
        else:
            if (self.boundjid.bare not in str(presence['from'])):
                user = str(presence['from']).split('@')[0]
                print('El usuario %s esta online...' % user)
    
    def new_user_add(self, presence):
        tp.banner('TE HA AGREGADO EL USUARIO: %s' % str(presence['from']))
    
    def send_file(self, body, filename):
        msg = ''
        # open de image, en another windows
        with Image.open(filename) as img:
            img.show()
        # send message to function in server
        with open(filename, 'rb') as img_file:
            msg = base64.b64encode(img_file.read()).decode('utf-8')
        try:
            self.send_message(mto=body+'@redes2020.xyz', mbody=msg, mtype="chat")
        except IqError as err:
            print("Error: %s" % err.iq['error']['text'])
        
        except IqTimeout:
            print("El server se ha tardado")
        

            

        


    
        
