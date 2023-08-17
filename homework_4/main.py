import urllib.parse
import mimetypes
import socket
import json
from datetime import datetime
from pathlib import Path
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler


HTTP_IP = ""
HTTP_PORT = 3000


UDP_IP = "127.0.0.1"
UDP_PORT = 5000


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message.html":
            self.send_html_file("message.html")
        else:
            if Path(f".{pr_url.path}").exists():
                self.send_static()
            else:
                self.send_html_file("error.html", 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(data, (UDP_IP, UDP_PORT))
        self.send_response(302)
        self.send_header("Location", "message.html")
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", "html")
        self.end_headers()
        with open(f".{self.path}", "rb") as file:
            self.wfile.write(file.read())


def start_http_server(ip: int, port: int) -> None:
    HTTPServer((ip, port), HttpHandler).serve_forever()


def start_udp_server(ip: int, port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as echo_server:
        echo_server.bind((ip, port))

        while True:
            data, address = echo_server.recvfrom(1024)
            data_path = "./storage/data.json"
            data_parse = urllib.parse.unquote_plus(data.decode())
            data = urllib.parse.parse_qs(data_parse)
            new_data_json = {
                str(datetime.now()): {key: value[0] for key, value in data.items()}
            }

            storage_path = Path("./storage/data.json")

            if not storage_path.exists():
                open(storage_path, "a").close()

            with open(data_path, "r") as file:
                data_json = json.load(file)

            data_json.update(new_data_json)

            with open(data_path, "w") as file:
                json.dump(data_json, file, indent=4)


if __name__ == "__main__":
    threads = []

    http_thread = Thread(target=start_http_server, args=(HTTP_IP, HTTP_PORT))
    http_thread.start()
    threads.append(http_thread)

    echo_server = Thread(target=start_udp_server, args=(UDP_IP, UDP_PORT))
    echo_server.start()
    threads.append(echo_server)

    [el.join() for el in threads]
