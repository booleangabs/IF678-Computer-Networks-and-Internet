import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 28886))
server_socket.listen(1)
connected = False

while True:
    if not connected:
        print("Aguardando conexão...\n")
        connection, (IP, port) = server_socket.accept()
        print(f"Conectado a {IP}:{port}", f"\n{'*' * 27}\n")
        connection.settimeout(20) # em segundos
        connected = True
        
    try:
        t0 = time.time()
        data = connection.recv(1024).decode()
        if data == "quit" or not data:
            print("Desligando...")
            print(f"Tempo de conexão: {time.time() - t0:.1f}s")
            break
        print(f"Recebi um '{data}'!")
        print("Respondendo...\n")
        connection.sendall(data.encode())
    except socket.timeout:
        print(f"Fechando conexão com {IP}:{port}...\n")
        print(f"Tempo de conexão: {time.time() - t0:.1f}s")
        connection.close()
        connected = False
        continue
        
connection.close()
server_socket.close()