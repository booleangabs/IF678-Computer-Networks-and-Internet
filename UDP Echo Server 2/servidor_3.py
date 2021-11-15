import socket
import datetime


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("localhost", 50000))
print("Servidor online em localhost:50000", f"\n{'*' * 34}\n")
while True:
    message, address = server_socket.recvfrom(1024)
    message = message.decode()
    if message == "Encerrar":
        print("Adeus")
        break
    elif message == "Que horas são?":
        answer = str(datetime.datetime.now()).split()[1]
    elif message == "Em que ano estamos?":
        answer = "Segundo o calendário chinês, estamos no Ano do Boi."
    else:
        answer = message
    print(f"Recebi '{message}' de {address[0]}:{address[1]}")
    print(f"Respondendo a {address[0]}:{address[1]}\n")
    server_socket.sendto(answer.encode(), address)
    
server_socket.close()