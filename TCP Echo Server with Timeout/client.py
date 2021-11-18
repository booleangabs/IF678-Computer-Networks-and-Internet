import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect(("localhost", 28886))
    
    while True:
        message = input("Requisitar > ")
        client_socket.send(message.encode())
        
        if message == "Encerrar":
            print("Desligamento solicitado!")
            break
        
        try:
            answer = client_socket.recv(1024).decode()
            print(f"Resposta > {answer}")
        except ConnectionAbortedError:
            print("Conexão encerrada pelo servidor")
            client_socket.close()
            break
    
    client_socket.close()
except ConnectionRefusedError:
    print("Não foi possível se conectar ao servidor.")
