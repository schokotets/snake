import threading
import http.server
import websocket_server
import socketserver
import socket
import sys
import os
import struct
from gamestate import GameState

HTTP_PORT=8080
WEBSOCKET_PORT=8090
UDP_PORT=9900

class HttpThread(threading.Thread):
    def run(self):
        web_dir = os.path.join(os.path.dirname(__file__), 'web')
        os.chdir(web_dir)
        Handler=http.server.SimpleHTTPRequestHandler

        with socketserver.TCPServer(("", HTTP_PORT), Handler) as httpd:
                print("webserver: serving http at port", HTTP_PORT)
                httpd.serve_forever()

class WebSocketThread(threading.Thread):
    websocks = websocket_server.WebsocketServer(WEBSOCKET_PORT, '0.0.0.0')
    def send(self, msg):
        #print("websocket: sending message \"%s\"" % msg)
        self.websocks.send_message_to_all(msg)
    def client_connected(self, client, server):
        print("websocket: client connected, given id %d" % client['id'])
        server.send_message(client, "%d" % client['id'])
    def client_left(self, client, server):
        if 'id' in client:
            print("websocket: client %d left" % client['id'])
            gamestate.kill(client['id'])
    def message_received(self, client, server, msg):
        print("websocket: received message \"%s\" from client %d" % (msg, client['id']))
        if msg == "join":
            gamestate.join(client['id'])
        else:
            id,dir = msg.split()
            gamestate.handle(int(id), dir)
    def run(self):
        self.websocks.set_fn_new_client(self.client_connected)
        self.websocks.set_fn_client_left(self.client_left)
        self.websocks.set_fn_message_received(self.message_received)
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
                gamestate.handle(id, c.decode("utf-8"))
            else:
                print("udpserver: received message of invalid length", len(data))

try:
    print("system: staring threads...")

    websockt = WebSocketThread()
    websockt.daemon = True
    websockt.start()

    gamestate = GameState(websockt.send)
    gamestate.daemon = True
    gamestate.start()

    httpt = HttpThread()
    httpt.daemon = True
    httpt.start()

    #udpt = UdpThread()
    #udpt.daemon = True
    #udpt.start()

    while websockt.is_alive():
        websockt.join(1)
    sys.exit()
except (KeyboardInterrupt, SystemExit):
    print("system: received keyboard interrupt, quitting threads")
    sys.exit()
