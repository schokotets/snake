class GameState:
    def __init__(self, websocket_send):
        self.websocket_send = websocket_send

    def handle(self, id, c):
        print("gamestate: handling %d %s" % (id, c))
        if c == b"r":
            self.websocket_send("%d turns right" % id)
        if c == b"l":
            self.websocket_send("%d turns left" % id)