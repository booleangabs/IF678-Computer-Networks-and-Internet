# -*- coding: utf-8 -*-
"""
O servidor funciona da seguinte forma (O estado inicial é o de espera):
                      
         ---->------------>----
        /                      \
    esperando              conectado
        ^                      |
        `--<-(timeout 20s)-<--Â´
                                                               
"""

import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 28886))
server_socket.listen(1)
connected = False
startedRunning = time.time()

while True:
    if not connected:
        # Entrando no estado de espera
        print("\nAguardando conexão...\n")
        connection, (IP, port) = server_socket.accept()
        
        # Entrando no estado conectado
        print(f"Conectado a {IP}:{port}", f"\n{'*' * 27}\n")
        connection.settimeout(20) # em segundos
        connected = True
    try:
        t0 = time.time()
        data = connection.recv(1024).decode()
        
        if data == "Encerrar" or not data:
            print(f"Fechando conexão com {IP}:{port} por solicitação")
            print(f"Tempo de conexão: {time.time() - t0:.1f}s")
            print(f"Tempo online: {time.time() - startedRunning:.1f}s")
            print("Desligando...")
            break
        
        print(f"Recebi um '{data}'!")
        print("Respondendo...\n")
        connection.send(data.encode())
    except socket.timeout:
        # Voltando para o estado inicial
        print(f"Fechando conexão com {IP}:{port} por inatividade")
        print(f"Tempo de conexão: {time.time() - t0:.1f}s\n")
        connection.close()
        connected = False
        continue
        
connection.close()
server_socket.close()
