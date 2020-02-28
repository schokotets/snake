import threading
import random
import time

WIDTH = 20
HEIGHT = 12

class GameState(threading.Thread):
    grid = [0] * (WIDTH*HEIGHT)
    players = {} # positions of the players' blocks
    facing = {}
    lengths = {}

    def __init__(self, websocket_send):
        super(GameState, self).__init__()
        self.websocket_send = websocket_send

    def join(self, id):
        pos = random.randrange(WIDTH*HEIGHT)
        while self.grid[pos] != 0:
            pos = random.randrange(WIDTH*HEIGHT)
        self.grid[pos] = id
        self.players[id] = [pos]
        self.facing[id] = "r"
        self.lengths[id] = 3
    
    def kill(self, id):
        for pos in self.players[id]:
            self.grid[pos] = 0
        del self.players[id]
        del self.facing[id]
        del self.lengths[id]

    def bound(self, pos):
        if pos < 0:
            return pos + WIDTH*HEIGHT
        if pos >= WIDTH*HEIGHT:
            return pos - WIDTH*HEIGHT
        return pos

    def update(self):
        for id in self.players:
            head = self.players[id][len(self.players[id])-1]
            if self.facing[id] == "u":
                self.players[id].append(self.bound(head-WIDTH))
            if self.facing[id] == "r":
                self.players[id].append(self.bound(head+1))
                print("add tile for %d at %d" %(id, self.bound(head+1)))
            if self.facing[id] == "l":
                self.players[id].append(self.bound(head-1))
            if self.facing[id] == "d":
                self.players[id].append(self.bound(head+WIDTH))
            head = self.players[id][len(self.players[id])-1]
            self.grid[head] = id
            if len(self.players[id]) > self.lengths[id]:
                self.grid[self.players[id][0]] = 0
                self.players[id] = self.players[id][1:]

    def handle(self, id, dir):
        print("gamestate: handling %d %s" % (id, dir))
        if dir == "u" and self.facing[id] != "d":
            print("gamestate: snake %d turns up" % id)
            self.facing[id] = dir
        if dir == "r" and self.facing[id] != "l":
            print("gamestate: snake %d turns right" % id)
            self.facing[id] = dir
        if dir == "d" and self.facing[id] != "u":
            print("gamestate: snake %d turns down" % id)
            self.facing[id] = dir
        if dir == "l" and self.facing[id] != "r":
            print("gamestate: snake %d turns left" % id)
            self.facing[id] = dir

    def sendState(self):
        #print("gamestate: playing field \\")
        data = "%dx%d\n" % (WIDTH, HEIGHT)
        for y in range(HEIGHT):
            for x in range(WIDTH):
                data += "%d;" % self.grid[y*WIDTH+x]
            data += "\n"
        #print(data)
        self.websocket_send(data)

    def run(self):
        while True:
            self.update()
            self.sendState()
            time.sleep(1)
