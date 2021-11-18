"""
O servidor funciona da seguinte forma (O estado inicial é o de espera):
                      
                          (Caso receba mensagem)
                      ---------<-----------<--------
                     /                              \
    esperando -> conectado -(timeout 20s)-> prestes a fechar -.
        ^                                                     /
        `----------<-------(timeout 10s)-------<-------------´
                                                               
Ao dar o primeiro timeout (20s) a variável about_to_close vira True
Originalmente, ela é setada para False toda vez que o cliente responde
Caso o cliente ainda não envie mensagem, a variável vai como True para
o try...except do timeout o que desconecta o cliente e reseta o loop.
"""


import socket
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 28877))
startedRunning = time.time()
server_socket.listen(1)
connected = False
about_to_close = False

try:
    while True:
        if not connected:
            # Entrando no estado inicial (Esperando)
            print("\nAguardando conexão...\n")
            connection, (IP, port) = server_socket.accept()
            
            # Entrando no estado Conectado
            t0 = time.time()
            print(f"Conectado a {IP}:{port}", f"{'*' * 27}\n", sep="\n")
            connection.settimeout(20)
            connected = True
        try:
            data = connection.recv(1024).decode()
            
            if data == "Encerrar" or not data:
                print(f"\nFechando conexão com {IP}:{port} por solicitação")
                print(f"Tempo de conexão: {time.time() - t0:.1f}s")
                print(f"Tempo online: {time.time() - startedRunning:.1f}s")
                print("Desligando...")
                break
            print(f"\nRequisitado > {data}")
            
            # Para gerenciar o estado do servidor:
            about_to_close = False
            connection.settimeout(20)
            
            connection.send(input("Responder > ").encode())
        except socket.timeout:
            if not about_to_close:
                # Entrando no estado Prestes a fechar
                about_to_close = True
                connection.settimeout(10)
                print(f"\nPrestes a me desconectar de {IP}:{port}")
                
                # Quando tento enviar, o cliente não consegue printar pois
                # está ocupado esperando input()
                # E se o cliente envia mensagem durante os dez segundos após
                # o timeout, recebe a alerta como resposta, o que mexe com a 
                # ordem das mensagens enviadas pelo servidor
                # connection.send("Alerta! Esta conexão será encerrada em breve!".encode())
            else:
                # Fechando conexão e voltando ao estado inicial
                print(f"\nFechando conexão com {IP}:{port} por inatividade")
                print(f"Tempo de conexão: {time.time() - t0:.1f}s\n")
                connection.close()
                connected = False
except:
    pass

connection.close()
server_socket.close()