from client import Client, RegistrerUser
from tabulate import tabulate

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
# Para mostrar el menu correspondiente
login_check = False

while flag:
    if not(login_check):
        opcion = input(menu_logging)
    else:
        opcion = input(menu_interaction)
    
    if(opcion=='1'):
        if not login_check:
            print('<-------REGISTRO DE USUARIO------->')
            name = input('Ingrse el Nombre: ')
            username = input('Ingrese usuario: ')
            password = input('Ingrese contraseña: ')
            jid = username + DOMAIN
            register = RegistrerUser(jid, password, name)
            if register.connect():
                register.process()
                print('Inicio de Sesion Correctamente')
                login_check = False
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
                login_check
    
    if(opcion=='3'):
        print('<-------MOSTRAR USUARIOS CONECTADOS------->')
        if login_check:
            list_user = client.list_user()
            table = tabulate(list_user, headers=['Email', 'JID', 'Username', 'Name'], tablefmt='grid')
            print(table)
        else:
            print('No esta dentro del servidor...')
    
    if(opcion=='4'):
        print('<-------AGREGAR UN USUARIO------->')
        if login_check:
            user_add = input('Ingrese el usuario: ')
            client.add_user(user_add)
    
    if(opcion=='5'):
        print('<-------MOSTRAR DETALLE DE CONTACTOS------->')
        if login_check:
            user_info = input('Ingrese el usuario: ')
            information = client.info_user(user_info)
            table = tabulate(information, headers=['Email', 'JID', 'Username', 'Name'], tablefmt='grid')
            print(table)

    if(opcion=='11'):
        print('<-------ELIMINAR CUENTA ACTUAL------->')
        if login_check:
            client.delete()
            opcion = '0'

    #if(opcion=='12' or opcion =='0'):
    if(opcion=='12'):
        if client.connect():
            client.logout()
            login_check
        print('Feliz Día, Vuelva Pronto')
        flag = False
    
    if(opcion=='0'):
        print('Vuelva Pronto')
        exit()