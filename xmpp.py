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
            print('Se creo correctamente el usuario: %d' % self.boundjid.user)
            log = logging.getLogger('XMPP')
            log.info('Usuario: %d' % boundjid.user)

        except IqError as err:
            logging.error('No se puede registrar...')
            print('Error %s' % err.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error('Sin respuesta del server...')
            self.disconnect
        


class Client(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.user = jid[0:-14]

        self.dominio = jid[-13:]

        self.add_event_handler('session_start', self.session_start)
        self.add_event_handler('message', self.message)

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
            log = logging.getLogger('XMPP')
            self.get_roster()
        except IqError as err:
            print('Error %s' % err.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            print('Servidor tarda mucho en responder...')
            self.disconnect

    def logout(self):
        self.disconnect(wait=False)

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply('Thanks for sending:\n%(body)s' % msg).send()
    
    def list_user(self):
        user = self.Iq()
        user['type'] = 'set'
        user['id'] = 'search_result'
        user['to'] = 'search.redes2020.xyz'
        
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
            #print(usr_list)
        except IqError as err:
            print('No se pueden mostrar: %s' % err)
        except IqTimeout:
            print('Servidor tarda mucho en responder...')
    
    def delete(self):
        item = ET.fromstring("<query xmlns='jabber:iq:register'>\<remove/>\</query>")
        stanza = self.make_iq_set(ito='redes2020.xyz', ifrom=self.boundjid.user)
        stanza.append(item)
        stanza.send()
    
if __name__ == '__main__':
    DOMAIN = '@redes2020.xyz'
    '''
    user = 'MarcosPruebas'
    password = 'marcos1234'
    '''
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
        0. Cerrar Sesion
    '''
    flag = True
    login_check = False
    
    while flag:
        if not(login_check):
            opcion = input(menu_logging)
        else:
            opcion = input(menu_interaction)

        if(opcion=='1'):
            if not login_check:
                print('<-------REGISTRO DE USUARIO------->')
                username = input('Ingrese usuario: ')
                password = input('Ingrese contraseña: ')
                jid = username + DOMAIN
                register = RegisterUser(jid, password)
                if register.connect():
                    register.process(block=True)
                else:
                    print('Error en crear')
            else:
                print('Ya esta dentro de una sesion abierta.')

        if(opcion=='2'):
            if not login_check:
                print('<-------INICIAR SESION------->')
                username = input('Ingrese usuario: ')
                password = input('Ingrese contraseña: ')
                jid = username + DOMAIN
                client = Client(jid, password)
                if client.connect():
                    client.process()
                    print('Inicio de Sesion Correctamente')
                    login_check = True
                else:
                    print('Error al Iniciar Sesion!')
            else:
                if client.connect():
                    client.logout()
                    login_check = False

        if(opcion=='1'):
            print('<-------MOSTRAR USUARIOS CONECTADOS------->')
            users = client.list_user()
            print("Los usuarios:\n|Usuario|---|Nombre|---|Subscripción|--|Estado|\n")
            for user in users:
                print(users)
        
        if(opcion=='9'):
            print('<-------ELIMINAR CUENTA INICIADA------->')

            client.delete()

        #PARA CERRAR EL PROGRAMA
        if(opcion == '0'):
            if client.connect():
                client.logout()
                login_check = False
                print('Feliz Dia!')
                flag = False
            else:
                print('Opcion no encontrada...!')

            




        