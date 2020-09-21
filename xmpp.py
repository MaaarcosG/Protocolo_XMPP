import sleekxmpp
import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase

class RegisterUser(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('register_user', self.register_user)

        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0004') # Data forms
        self.register_plugin('xep_0066') # Out-of-band Data
        self.register_plugin('xep_0077') # In-band Registration
        self.register_plugin('xep_0199') # XMPP Ping
        self.register_plugin('xep_0045') # Multi-User Chat (MUC)
        self.register_plugin('xep_0096') # File transfer

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        self.disconnect()

    def register_user():
        res = self.Iq()
        res['type'] = 'set'
        res['register']['username'] = self.boundjid.user
        res['register']['password'] = self.password

        try:
            res.send(now=True)
        except IqError as err:
            logging.error('No se puede registrar...')
            self.disconnect()
        except IqTimeout:
            logging.error('Sin respuesta del server...')
            self.disconnect
        


class Client(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
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
    user = 'MarcosPruebas'
    password = 'marcos1234'
    
    menu_logging = '''
        1. Registrar Usuario
        2. Login
        0. Salir
        Ingrese una Opcion: 
    '''
    menu_interaction = '''
        1. Mostrar los Usuarios
        2. Agregar un usuario a los contactos
        3. Mostrar detalles de contacto de un usuario
        4. Mensaje Directo (Privado)
        5. Conversacion Grupal
        6. Definir mensaje de presencia
        7. Enviar/Recibir notificaciones
        8. Enviar/Recibir archivos
        9. Eliminar cuenta (SESION INICIADA) 
    '''
    flag = False
    opcion  = ''

    while opcion != '0':
        if not flag:
            opcion = input(menu_logging)
            
            if(opcion=='1'):
                user = input('Ingrese nombre de usuario:\n')
                password = input('Ingrese la contraseña:\n')

                register = RegisterUser(user+DOMAIN, password)

                #verificamos si se conecta
                if register.connect():
                    register.process(block=True)
                else:
                    print('No se ha podido registrar el usuario')
        
            elif(opcion=='2'):
                user = input('Ingrese nombre de usuario:\n')
                password = input('Ingrese la contraseña:\n')

                xmpp = Client(user+DOMAIN, password)

                #verificamos si se conecta
                if xmpp.connect():
                    xmpp.process()
                    print('Conexion Exitosa')
                    flag = True

                else:
                    print('No se puede conectar')




        