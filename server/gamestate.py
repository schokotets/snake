import threading

class GameState(threading.Thread):
    def __init__(self, websocket_send):
        super(GameState, self).__init__()
        self.websocket_send = websocket_send

    def handle(self, id, dir):
        print("gamestate: handling %d %s" % (id, dir))
        if dir == "r":
            self.websocket_send("%d turns right" % id)
        if dir == "l":
            self.websocket_send("%d turns left" % id)