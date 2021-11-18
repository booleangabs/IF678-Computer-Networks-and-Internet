import socket

def bytes2string(data) -> str:
    return str(data).split('b')[1].strip('\'')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 28887))
server_socket.listen(1)
connection, address = server_socket.accept()
print(f'Connected to {address[0]}, port {address[1]}', f'\n{"*" * 34}\n')
while True:
    data = bytes2string(connection.recv(1024))
    if data == 'quit':
        print('Client told me to shut down!')
        break
    print(f'Received a "{data}" from {address[0]}, {address[1]}')
    print('Echoing back...\n')
    connection.sendall(bytes(data, 'utf8'))
    
connection.close()
server_socket.close()