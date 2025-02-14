from socket import socket, AF_INET, SOCK_STREAM, gethostname


server = socket(AF_INET, SOCK_STREAM, -1)
server.bind((gethostname(), 8080))

print(f"Listening in {server.getsockname()[0]}:{server.getsockname()[1]}")

while 1:
    try:
        server.listen()

        (clientSocket, clientAddress) = server.accept()
        print(clientSocket)
        print(clientAddress)

        msg = clientSocket.recv(1024).decode()

        clientSocket.send("Hello from httpy :)".encode())
        clientSocket.close()
    except KeyboardInterrupt:
        server.close()

server.close()
