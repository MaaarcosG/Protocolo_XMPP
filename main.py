import tableprint as tp

from client import Client, RegistrerUser
from tabulate import tabulate

DOMAIN = '@redes2020.xyz'

menu_logging = '''
1. Registrar Usuario
2. Login
0. Salir 
Escoga una opcion:
'''

menu_interaction = '''
3. Mostrar los Usuarios
4. Agregar un usuario a los contactos
5. Mostrar detalles de contacto de un usuario
6. Mensaje Directo (Privado)
7. Conversacion Grupal
8. Definir mensaje de presencia
9. Enviar archivos
10. Eliminar cuenta (SESION INICIADA) 
11. Cerrar
Escoga una opcion:
'''

states = {
    '1': 'chat',
    '2': 'away',
    '3': 'xa',
    '4': 'dnd'
}
flag = True
# Para mostrar el menu correspondiente
login_check = False

while flag:
    if not(login_check):
        tp.banner('Bienvenido al Server %s' % DOMAIN)
        opcion = input(menu_logging)
    else:
        tp.banner('<-------¿Que desea Realizar?------->')
        opcion = input(menu_interaction)
    
    if(opcion=='1'):
        if not login_check:
            tp.banner('<-------REGISTRO DE USUARIO------->')
            name = input('Ingrese el Nombre: ')
            username = input('Ingrese usuario: ')
            password = input('Ingrese contraseña: ')
            jid = username + DOMAIN
            register = RegistrerUser(jid, password, name)
            if register.connect():
                register.process(block=True)
                login_check = False
            else:
                print('Error al Iniciar Sesion!')
            
    if(opcion=='2'):
        if not login_check:
            tp.banner('<-------INICIAR SESION------->')
            username = input('Ingrese usuario: ')
            password = input('Ingrese contraseña: ')
            jid = username + DOMAIN
            client = Client(jid, password)
            if client.connect():
                client.process()
                client.connection_correct()
                login_check = True
            else:
                print('Error al Iniciar Sesion!')
        else:
            if client.connect():
                client.logout()
                login_check
    
    if(opcion=='3'):
        tp.banner('<-------MOSTRAR USUARIOS CONECTADOS------->')
        if login_check:
            list_user = client.list_user()
            table = tabulate(list_user, headers=['Email', 'JID', 'Username', 'Name'], tablefmt='fancy_grid')
            print(table)
        else:
            print('No esta dentro del servidor...')
    
    if(opcion=='4'):
        tp.banner('<-------AGREGAR UN USUARIO------->')
        if login_check:
            user_add = input('Ingrese el usuario: ')
            client.add_user(user_add)
    
    if(opcion=='5'):
        tp.banner('<-------MOSTRAR DETALLE DE CONTACTOS------->')
        if login_check:
            user_info = input('Ingrese el usuario: ')
            information = client.info_user(user_info)
            table = tabulate(information, headers=['Email', 'JID', 'Username', 'Name'], tablefmt='fancy_grid')
            print(table)
    
    if(opcion=='6'):
        tp.banner('<-------ENVIAR MENSAJE PRIVADO------->')
        if login_check:
            destination = input('Ingrese el usuario, a quien le mandara mensaje: ')
            message = input('Mensaje a Enviar: ')
            client.private_message(destination, message)

    if(opcion=='7'):
        tp.banner('<-------MENSAJES GRUPALES------->')
        if login_check:
            opcion_rooms = input('1. Unirte\n2. Crear una Sala\n3. Enviar mensaje Grupal \nEscoga una opcion: ')
            if(opcion_rooms=='1'):
                room = input('Ingrese el room: ')
                client.joinRoom(room)

            elif(opcion_rooms=='2'):
                room = input('Ingrese el room ha crear: ')
                client.createRoom(room)
            
            elif(opcion_rooms=='3'):
                room = input('Ingrese el room: ')
                message = input('Ingrese el mensaje: ')
                client.group_message(room, message)
            else:
                print('No esta dentro de un grupo actualmente....')
    if(opcion=='8'):
        tp.banner('LOSIENTO IMPLEMENTACIÓN EN PROCESO....!')
        login_check = True
    
    if(opcion=='9'):
        if login_check:
            tp.banner('<-------ENVIO DE IMAGENES------->')
            user = input('Ingrese el usuario: ')
            file_path = input('File Path: ')
            client.send_file(user, file_path)

    if(opcion=='10'):
        tp.banner('<-------ELIMINAR CUENTA ACTUAL------->')
        if login_check:
            client.delete()
            opcion = '0'

    #if(opcion=='12' or opcion =='0'):
    if(opcion=='11'):
        if client.connect():
            client.logout()
            login_check
        print('Feliz Día, Vuelva Pronto')
        flag = False
    
    if(opcion=='0'):
        print('Vuelva Pronto')
        print('Cerrando Programa')
        exit()