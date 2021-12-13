# -*- coding: utf-8 -*-
"""
Funcionamento:
    - O cliente requisita um match ao servidor e espera.
    - A mensagem seguinte a primeira resposta do servidor são as 
      portas que o cliente deve usar para envio e recepção.
    - A recepção é feita com o uso de uma thread.
    - As mensagens enviadas contém um identificador (parecido com
      o número de sequência). 
    - Caso a mensagem recebida contenha a palavra "Recebido", a
      thread do receptor observa se a última mensagem enviada
      já recebeu o reconhecimento do peer. Caso ainda não tenha
      ocorrido confirmação, a mensagem de visto é printada e continuamos
      o loop.
    - Todas as transferências de dados ocorrem por fluxos UDP.
"""

import socket
import threading
import datetime


SELF_COUNTER = 0

class Receiver(threading.Thread):
    def __init__(self, sock, peer_address):
        super().__init__(daemon=True)
        self.sock = sock
        self.peer_address = peer_address
        self.counter = 0
        self.confirmed = False
        self.lastAcked = -1
        
    def run(self):
        global SELF_COUNTER
        while True:
            message = self.sock.recvfrom(1024)[0].decode()
            idx, message = message.split("#")
            if message == "Recebido" and ~self.confirmed:
                self.confirmed = True
                print(f"Mensagem {idx} recebida.")
                continue
            self.sock.sendto(f"{self.counter}#Recebido".encode(), self.peer_address)
            time = str(datetime.datetime.now())[:-7]
            print()
            print(f"{self.counter:<3} [{time}]: {message}")
            self.counter += 1

temp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
temp_socket.sendto("1".encode(), ("localhost", 30000))
_ = temp_socket.recvfrom(1024)
print("Procurando peer...\n")

peer_ip, send_to, listen_to = eval(temp_socket.recvfrom(2048)[0].decode())
peer_address = (peer_ip, send_to)
print(f"Peer: {peer_ip}\nEnviar para {send_to} e escutar em {listen_to}.")
temp_socket.close()

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind(("localhost", listen_to))
receiver = Receiver(receiver_socket, peer_address)
receiver.start()

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    message = input(f"Sua mensagem nº {SELF_COUNTER}: ")
    sender_socket.sendto(f"{SELF_COUNTER}#{message}".encode(), peer_address)
    receiver.confirmed = False
    SELF_COUNTER += 1
    
    
