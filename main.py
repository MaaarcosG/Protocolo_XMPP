from Registro import *
from xmpp import *

DOMAIN = '@redes2020.xyz'

menu_logging = '''
1. Registrar Usuario
2. Login
0. Salir 
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
0. Cerrar
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
            register = RegistrerUser(jid, password)
            if register.connect():
                register.process()
                print('Inicio de Sesion Correctamente')
                login_check = True
            else:
                print('Error al Iniciar Sesion!')
        else:
            print('Ya esta loggeado, se pasa a la siguiente opcion...')
            
    if(opcion=='2'):
        if not login_check:
            print('<-------INICIAR SESION------->')
            username = input('Ingrese usuario: ')
            password = input('Ingrese contraseña: ')
            jid = username + DOMAIN
            client = Client(jid, password, username)
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
        if login_check:
            client.list_user()
        else:
            print('No esta dentro del servidor...')