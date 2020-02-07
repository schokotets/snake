import threading
import http.server
import socketserver
import socket
import struct

HTTP_PORT=8080
UDP_PORT=9900

class HttpThread(threading.Thread):
    def run(self):
        Handler=http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", HTTP_PORT), Handler) as httpd:
                print("serving http at port", HTTP_PORT)
                httpd.serve_forever()


class UdpThread(threading.Thread):
    def run(self):
        # https://wiki.python.org/moin/UdpCommunication
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.bind(("", UDP_PORT))

        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            if(len(data) == 3):
                id,x,y = struct.unpack("Bbb", data[:3])
                print("received id:", id, "x:", x, "y:", y)
            else:
                print("received message of invalid length", len(data))

HttpThread().start()
UdpThread().start()
