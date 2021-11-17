import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(("localhost", 28886))
    message = ""
    while message != "quit":
        message = input()
        client_socket.sendall(message.encode())
        try:
            answer = client_socket.recv(1024).decode()
            print(f"O servidor respondeu '{answer}'")
        except ConnectionAbortedError:
            print("Conexão encerrada pelo servidor")
            client_socket.close()
            break
    else:
        print("Desligamento solicitado!")
    client_socket.close()
    
except ConnectionRefusedError:
    print("Não foi possível se conectar ao servidor.")

    
    
