import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(("localhost", 50000))

while True:
    message = input()
    if message == "Encerrar":
        break
    client_socket.sendto(message.encode(), ("localhost", 50000))
    answer = client_socket.recvfrom(1024)[0].decode()
    print(f"O servidor respondeu '{answer}'")
    
print("Encerrando conexão")
client_socket.sendall("Encerrar".encode())
client_socket.close()