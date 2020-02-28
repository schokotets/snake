import threading
import http.server
import websocket_server
import socketserver
import socket
import struct
from gamestate import GameState

HTTP_PORT=8080
WEBSOCKET_PORT=8090
UDP_PORT=9900

class HttpThread(threading.Thread):
    def run(self):
        Handler=http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", HTTP_PORT), Handler) as httpd:
                print("webserver: serving http at port", HTTP_PORT)
                httpd.serve_forever()

class WebSocketThread(threading.Thread):
    websocks = websocket_server.WebsocketServer(WEBSOCKET_PORT)
    def send(self, msg):
        print("websocket: sending message \"%s\"" % msg)
        self.websocks.send_message_to_all(msg)
    def client_connected(self, client, server):
        print("websocket: client connected, given id %d" % client['id'])
    def run(self):
        self.websocks.set_fn_new_client(self.client_connected)
        print("websocket: serving websocket at port", WEBSOCKET_PORT)
        self.websocks.serve_forever()

class UdpThread(threading.Thread):
    def run(self):
        # https://wiki.python.org/moin/UdpCommunication
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.bind(("", UDP_PORT))
        print("udpserver: serving udp server at port", UDP_PORT)

        while True:
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            if(len(data) == 2):
                id,c = struct.unpack("Bc", data[:3])
                print("udpserver: received id:", id, "l/r:", c)
                gamestate.handle(id, c)
            else:
                print("udpserver: received message of invalid length", len(data))

try:
    print("system: staring threads...")
    websockt = WebSocketThread()
    websockt.start()
    gamestate = GameState(websockt.send)

    HttpThread().start()
    UdpThread().start()
except (KeyboardInterrupt, SystemExit):
    print("system: received keyboard interrupt, quitting threads")
    sys.exit()