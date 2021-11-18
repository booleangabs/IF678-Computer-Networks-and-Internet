import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.connect(("localhost", 28886))

while True:
    try:
        message = input("Requisitar > ")
        client_socket.sendto(message.encode(), ("localhost", 50000))
        if message == "Encerrar":
            break
        answer = client_socket.recvfrom(1024)[0].decode()
        print(f"Resposta > {answer}")
    except:
        print("Não foi possível se comunicar com o servidor")
    
client_socket.sendall("Encerrar".encode())
client_socket.close()