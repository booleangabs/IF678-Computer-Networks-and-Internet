import socket


def bytes2string(data) -> str:
    return str(data).split('b')[1].strip('\'')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 50000))
print('Server running on port 50000', f'\n{"*" * 28}\n')
while True:
    message, address = server_socket.recvfrom(1024)
    if bytes2string(message) == 'quit':
        break
    print(f'Received "{bytes2string(message)}" from {address[0]}, port {address[1]}')
    print(f'Echoing back to {address[0]}, port {address[1]}')
    server_socket.sendto(message, address)
    
print('Shut down by client!')
server_socket.close()