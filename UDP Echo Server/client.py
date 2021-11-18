import socket

def bytes2string(data) -> str:
    return str(data).split('b')[1].strip('\'')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(('localhost', 50000))

while (message := input()) != 'quit':
    client_socket.sendto(bytes(message, 'utf-8'), ('localhost', 50000))
    answer = bytes2string(client_socket.recvfrom(1024)).split(',')[0].strip('\'')
    print(f'The server echoed back "{answer}"')

print('Connection ended!')
client_socket.sendall(bytes('quit', 'utf-8'))
client_socket.close()