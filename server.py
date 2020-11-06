import socket
import threading

'''
Constant values that 'should' not change at all
    includes the server, port, format, and disconnect msg
'''
PORT = 5049
SERVER = '192.168.0.7' 
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(connection, addr):
    
    print(f'[NEW CONNECTION] {addr} connected')
    connected = True
    while connected:
        msg_len = connection.recv(64).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = connection.recv(msg_len).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f'[{addr}] {msg}')
            while True:
                msg = input('Type message to send\n')
                connection.send(msg.encode(FORMAT))

                if msg == DISCONNECT_MESSAGE:
                    break
            
def start():
    server.listen()
    print(f'Server is listening on {SERVER} PORT:{PORT}')
    while True:
        connection, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, addr))
        thread.start()
        #print(f'[ACTIVE CONNECTIONS] {thread.active_count() - 1}')

print('Server is starting...')
start()

