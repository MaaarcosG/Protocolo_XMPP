# Protocolo_XMPP
Contains the protocol implementation using Sleekxmpp.
Made by:
- Sergio Juan Marcos Gutierrez Romero
- Carne: 17909
# Code
See the code of project [Protocolo XMPP](https://github.com/MaaarcosG/Protocolo_XMPP.git)
## Requeriments 
- Python 3.8 +
- Sleekxmpp 1.3.3
- Tabulate 0.8.7

## Install Requeriments
```bash
$ pip3 install -r requirements.txt
```

## To run client
```bash
$ python3 main.py
```

## Implemented Functions
To use the program it is simple, it shows you a menu with several options with which you can interact. It shows you the implementations made:
1. **Register new Account:** To register an account, enter your name, username and password.
2. **Log In**: Enter your username and password
3. **Show users register in the server**: Choose option 3 and it will show you all users
4. **Show specific user**: Enter the user you want to see
5. **Send private message**: The user to whom the message will be sent is entered, and the message is entered.
6. **Group conversation**
  - Join in group: Enter the room
  - Create group: Enter the number of room
  - Send message in group: Enter the number of room and the message 
7. **Send images**: Enter the user, and file path to imagen send
8. **Delete Account**: delete the account you are currently on 	
9. **Log Out**: Close the session on the server and terminate the program

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

