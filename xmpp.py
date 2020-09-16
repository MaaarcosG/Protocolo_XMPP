import sleekxmpp
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase



class Client(sleekxmpp.ClientXMPP):
    def __init__(self, username, password, instance_name=None):
        jid = "%s/%s" % (username, instance_name) if instance_name else username 
        super(Client, self).__init__(jid, password)

        self.instance_name = instance_name
        self.add_event_handler('session_start', self.start)
        #self.add_event_handler('message', self.receive)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0045') # Mulit-User Chat (MUC)
        self.register_plugin('xep_0096') # File transfer

        self.contacts = []

        if self.connect():
            #print('You connect is ready')
            self.process(block=False)
        else:
            raise Exception ('Unable to connect')

    def start(self, event):
        self.send_presence(pshow='chat', pstatus='Disponible')
        roster = self.get_roster
        print(roster)
        for i in roster['roster']['items'].keys():
            self.contacts.append(i)
    
    def __del__(self):
        self.close 

    def close(self):
        print('Closing XMPP connection')
        self.disconnect(wait=False)
    
    def send_msg(self, recipient, body):
        message = self.Message()
        message['to'] = recipient
        message['type'] = 'chat'
        message['body'] = body

        print('Sending message: %s' % message)
        message.send()


clientxmpp = Client('MarcosGutierrez@redes2020.xyz', 'Marcos', 'redes2020.xyz')



        