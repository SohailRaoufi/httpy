from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import sys
import signal
import mimetypes
import os
from name import http_name
import argparse
from another import generate_directory_listing


class Httpy:
    def __init__(self, host="localhost", port=8001, path=None):
        self.host = host
        self.port = port
        self.path = path or os.getcwd()
        self.server = socket(AF_INET, SOCK_STREAM, -1)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))

    def serve(self):
        print(http_name)
        print(f"Listening on {self.host}:{self.port}")

        signal.signal(signal.SIGINT, self.shutdown)
        self.server.listen()

        while 1:
            try:
                (clientSocket, clientAddress) = self.server.accept()
                self.handle_request(clientSocket)
            except OSError as e:
                print(e)
                break

        self.server.close()

    def shutdown(self, sig, frame):
        print("\nShuting down the server.......")
        self.server.close()
        sys.exit(0)

    def handle_request(self, client_socket: socket):
        try:
            req = client_socket.recv(1024).decode().splitlines()
            if not req:
                return
            request_line = req[0].split()

            if len(request_line) < 2:
                client_socket.send(self.response("400 Bad Request", "text/plain", 400))
                client_socket.close()
                return

            content = self.resolve_path(request_line)
            if content is None:
                client_socket.send(
                    self.response("500 Internal File Variable!", "text/plain", 500)
                )
                client_socket.close()
                return

            client_socket.send(content)

        except Exception as e:
            print(e)
            client_socket.send(
                self.response("500 Internal Pointer Variable!", "text/plain", 500)
            )
        finally:
            client_socket.close()

    def response(self, content, content_type, status):
        if isinstance(content, str):
            content = content.encode()
        status_text = self.get_status_text(status)
        content_length = len(content)
        http_status = f"HTTP/1.1 {status} {status_text}"

        headers = {"Content-Type": content_type, "Content-Length": content_length}

        res = [http_status]
        for key, item in headers.items():
            res.append(f"{key}: {item}")
        res.append("")

        header_str = "\n".join(res).encode() + b"\n"
        return header_str + content

    def resolve_path(self, data):
        path = data[1]
        final_path = os.path.join(self.path, path.lstrip("/"))

        if os.path.isdir(final_path):
            list_dir = generate_directory_listing(final_path, path)
            return self.response(list_dir, "text/html", 200)

        if os.path.isfile(final_path):
            with open(final_path, "rb") as file:
                content = file.read()
            return self.response(content, self.resolve_content_type(final_path), 200)

    @staticmethod
    def get_status_text(status):
        return {
            200: "OK",
            201: "CREATED",
            204: "NO CONTENT",
            400: "BAD REQUEST",
            404: "NOT FOUND",
            500: "INTERNAL SERVER ERROR",
        }.get(status, "UNKNOWN STATUS")

    @staticmethod
    def resolve_content_type(data_path):
        return mimetypes.guess_type(data_path)[0] or "application/octet-stream"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Httpy", description="Simple HTTP Server")
    parser.add_argument(
        "--host", default="localhost", help="Server host [default: localhost]"
    )
    parser.add_argument(
        "--p", "--port", default=8001, type=int, help="Server port [default: 8001]"
    )
    parser.add_argument(
        "--path", help="Directory to serve files from [default: current directory]"
    )

    args = parser.parse_args()
    server = Httpy(host=args.host, port=args.p, path=args.path)
    server.serve()
