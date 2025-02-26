from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import sys
import signal
import mimetypes
import os
from name import http_name
import argparse

"""
-------------------- Command Line Arguments Parser ---------------------
"""

parser = argparse.ArgumentParser(prog="Httpy", usage="%(prog)s [OPTIONS]")
parser.add_argument("--host",default="localhost", help="determine the host of server. [default: localhost]")
parser.add_argument("--p", "--port", default=8001, type=int , help="determine the porst of the server. [default: 8001]")
parser.add_argument("-V", "--version", action="version", version="%(prog)s 0.1.0")
parser.add_argument("--path", help="the path of directory for server to run. [default: current directory]")
args = parser.parse_args()


"""
----------- Command Line Arguments -----------
"""

host = args.host
port = args.p
path = args.path


server = socket(AF_INET, SOCK_STREAM, -1)

server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

server.bind((host, port))

print(http_name)
print(f"Listening in {server.getsockname()[0]}:{server.getsockname()[1]}")


def close_and_cleanup(sig, frame):
    print("\nShuting down the server.......")
    server.close()
    sys.exit(0)


def get_status_text(status):
    if status == 200:
        return 'OK'
    if status == 201:
        return 'CREATED'
    if status == 203:
        return 'NO CONTENT'
    if status == 400:
        return 'BAD REQUEST'
    if status == 404:
        return 'NOT FOUND'
    else:
        return 'Internal Pointer Variable Error'


def response(content, content_type, status):
    if isinstance(content, str):
        content = content.encode()
    status_text = get_status_text(status)
    content_length = len(content)
    http_status = f"HTTP/1.1 {status} {status_text}"

    headers = {
        "Content-Type": content_type,
        "Content-Length": content_length
    }

    res = [http_status]
    for key, item in headers.items():
        res.append(f"{key}: {item}")
    res.append("")

    header_str = "\n".join(res).encode() + b"\n"
    return header_str + content


def resolve_content_type(data_path):
    return mimetypes.guess_type(data_path)[0] or "application/octet-stream"


def resolve_path(data):
    path = data[1:]
    if os.path.isfile(path):
        return path
    return None


def request(socket: socket):
    try:
        req = socket.recv(1024).decode().splitlines()
        data = req[0].split()
        data_path = resolve_path(data[1])
        if data_path is None:
            return response("404 Not Found", "text/plain", 404)

        with open(data_path, 'rb') as file:
            content = file.read()

        return response(content, resolve_content_type(data_path), 200)
    except Exception as e:
        print(e)
        return response('500 Internal Pointer Variable!', 'text/plain', 500)


signal.signal(signal.SIGINT, close_and_cleanup)
server.listen()
while 1:
    try:
        (clientSocket, clientAddress) = server.accept()
        res = request(clientSocket)
        clientSocket.send(res)
        clientSocket.close()
    except OSError as e:
        print(e)
        break


server.close()
