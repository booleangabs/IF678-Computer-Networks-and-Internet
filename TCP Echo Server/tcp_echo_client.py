import socket


def bytes2string(data) -> str:
    return str(data).split('b')[1].strip('\'')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 28887))

while (message := input()) != 'quit':
    client_socket.sendall(bytes(message, 'utf-8'))
    answer = bytes2string(client_socket.recv(1024))
    print(f'The server echoed back "{answer}"')

print('Connection ended!')
client_socket.sendall(bytes('quit', 'utf-8'))
client_socket.close()