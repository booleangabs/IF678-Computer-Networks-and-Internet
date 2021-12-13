# -*- coding: utf-8 -*-
"""
Funcionamento:
    - O servidor assume que os peers estão no mesmo host
    - O servidor envia a cada par, as portas onde os peers deve,
      dar bind no receptor e para onde os peers deve direcionar as 
      mensagens.
    - As portas do tipo 4XXXX são para onde o peer 1 deve enviar e 
      onde o peer 2 deve escutar.
    - As portas do tipo 5XXXX são para onde o peer 2 deve enviar e 
      onde o peer 1 deve escutar.
    - Ele gerencia as portas sendo utilizadas com as variáveis
      PORTS e OFFSET. O primeiro par recebe como portas para uso
      40000 e 50000. O offset aumenta em 1 e o segundo par recebe
      40001 e 50001.
"""


import socket

PORTS = [40000, 50000]
OFFSET = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('localhost', 30000))
print("Servidor livre em localhost:30000", f"\n{'*' * 34}\n")
while True:
    peers = []
    next_peer_id = 1
    
    # Armazenando o próximo par
    while next_peer_id < 3:
        _, address = server_socket.recvfrom(1024)
        print(address)
        peers.append(address)
        server_socket.sendto("1".encode(), address)
        next_peer_id += 1
    print("Enviando endereços e portas")
    
    for i in range(2):
        PORTS[i] += OFFSET
    OFFSET += 1
    print(f"Os clientes usarão as portas {PORTS}.")
    
    # Dizer ao cliente 1:
    # Mande mensagens para IP de 2 na porta 4000X e espere resposta em 5000X
    info1 = [peers[1][0]] + PORTS
    
    # Dizer ao cliente 2:
    # Mande mensagens para IP de 1 na porta 5000X e espere ressposta em 4000X
    info2 = [peers[1][0]] + PORTS[::-1]
    
    message1 = str(info1).encode()
    message2 = str(info2).encode()
    server_socket.sendto(message1, peers[0])
    server_socket.sendto(message2, peers[1])

    next_peer_id = 1
    print("Servidor Livre\n")