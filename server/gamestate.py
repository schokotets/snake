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
    food = -1

    def __init__(self, websocket_send):
        super(GameState, self).__init__()
        self.websocket_send = websocket_send

    def freepos(self):
        pos = random.randrange(WIDTH*HEIGHT)
        while self.grid[pos] != 0:
            pos = random.randrange(WIDTH*HEIGHT)
        return pos

    def join(self, id):
        pos = self.freepos()
        self.grid[pos] = id
        self.players[id] = [pos]
        self.facing[id] = "r"
        self.lengths[id] = 3

    def reset(self, id):
        for pos in self.players[id]:
            self.grid[pos] = 0
        pos = self.freepos()
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

    def bound(self, pos, dir):
        if pos % WIDTH == 0 and dir == "r": #left bound
            return pos - WIDTH
        if (pos+1) % WIDTH == 0 and dir == "l": #right bound
            return pos + WIDTH
        if pos < 0: #top bound
            return pos + WIDTH*HEIGHT
        if pos >= WIDTH*HEIGHT: #bottom bound
            return pos - WIDTH*HEIGHT
        return pos

    def update(self):
        for id in self.players:
            head = self.players[id][len(self.players[id])-1]
            if self.facing[id] == "u":
                self.players[id].append(self.bound(head-WIDTH, self.facing[id]))
            if self.facing[id] == "r":
                self.players[id].append(self.bound(head+1, self.facing[id]))
            if self.facing[id] == "l":
                self.players[id].append(self.bound(head-1, self.facing[id]))
            if self.facing[id] == "d":
                self.players[id].append(self.bound(head+WIDTH, self.facing[id]))
            head = self.players[id][len(self.players[id])-1]

            if self.grid[head] == -1:
                self.food = -1 #food eaten
                self.lengths[id] = self.lengths[id] +1
                print("gamestate: snake %d ate food, grew to length %d" % (id, self.lengths[id]))
            
            if self.grid[head] > 0: #collision
                self.reset(id)
                continue

            # keep snake to its length
            if len(self.players[id]) > self.lengths[id]:
                self.players[id] = self.players[id][1:]
    
        #grid redraw
        self.grid = [0] * (WIDTH*HEIGHT)
        for id in self.players:
            for pos in self.players[id]:
                self.grid[pos] = id
        
        #food generator
        if self.food == -1: #no food placed
            if random.random() < 0.1:
                self.food = self.freepos()
                print("gamestate: food spawned at pos %d" % self.food)
        if self.food != -1: #food exists
            self.grid[self.food] = -1

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
            time.sleep(0.3)
