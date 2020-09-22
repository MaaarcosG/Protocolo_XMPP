from client import *
from register import *

DOMAIN = '@redes2020.xyz'

menu_logging = '''
1. Registrar Usuario
2. Login
0. Salir 
'''

menu_interaction = '''
3. Mostrar los Usuarios
4. Agregar un usuario a los contactos
5. Mostrar detalles de contacto de un usuario
6. Mensaje Directo (Privado)
7. Conversacion Grupal
8. Definir mensaje de presencia
9. Enviar/Recibir notificaciones
10. Enviar/Recibir archivos
11. Eliminar cuenta (SESION INICIADA) 
12. Cerrar
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
    
    if(opcion=='3'):
        print('<-------MOSTRAR USUARIOS CONECTADOS------->')
        if login_check:
            client.list_user()
        else:
            print('No esta dentro del servidor...')