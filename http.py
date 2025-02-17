from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, gethostname
import sys
import signal


server = socket(AF_INET, SOCK_STREAM, -1)

server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

server.bind((gethostname(), 8001))

print(f"Listening in {server.getsockname()[0]}:{server.getsockname()[1]}")


def close_and_cleanup(sig, frame):
    print("\nShuting down the server.......")
    server.close()
    sys.exit(0)


signal.signal(signal.SIGINT, close_and_cleanup)

server.listen()
while 1:
    try:
        (clientSocket, clientAddress) = server.accept()
        print(clientAddress)
        msg = clientSocket.recv(2024).decode()
        clientSocket.send("""HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 30

<html><body>Hello World</body></html>
""".encode())
        clientSocket.close()
    except OSError:
        break

server.close()
