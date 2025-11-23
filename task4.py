import tkinter as tk
from tkinter import ttk
import numpy as np
import random
W0 = 400
ITEM_IN_ROW = 4
TILE_COLORS = { 0: ("ivory", "#ivory"),
        2: ("#eee4da", "#776e65"),
        4: ("#ede0c8", "#776e65"),
        8: ("#f2b179", "#f9f6f2"),
        16: ("#f59563", "#f9f6f2"),
        32: ("#f67c5f", "#f9f6f2"),
        64: ("#f65e3b", "#f9f6f2"),
        128: ("#edcf72", "#f9f6f2"),
        256: ("#edcc61", "#f9f6f2"),
        512: ("#edc850", "#f9f6f2"),
        1024: ("#edc53f", "#f9f6f2"),
        2048: ("#edc22e", "#f9f6f2")}


class Game():
    def __init__(self,root):
        self.root = root
        self.board = tk.Frame(master= self.root,width =W0,height= W0,bg = 'ivory')
        
        
        self.mirror_grid = [[0 for _ in range(ITEM_IN_ROW)] for _ in range(ITEM_IN_ROW)]
        print(self.mirror_grid)

        #binding events with keys
        self.root.bind('<Left>',self.handle_event)
        self.root.bind('<Right>',self.handle_event)
        self.root.bind('<Up>',self.handle_event)
        self.root.bind('<Down>',self.handle_event)
        self.root.bind('<Escape>', lambda event: root.quit())

        self.board.grid(row = 0,column = 0)
        self.game()




    def handle_event(self,event):

        key_symbol = event.keysym
        
        if key_symbol == 'Left':
            print("LEFT\n")
            
        elif key_symbol == 'Right':
           print("RIGHT\n")

        elif key_symbol == 'Up':
           print("UP\n")

        elif key_symbol == 'Down':
           print("DOWN\n")


        else:
            print(f"Unknown key pressed: {key_symbol}")


    def setup_init_tiles(self):
        print("setting up init tiles")
        self.tiles = []
        for i in range(ITEM_IN_ROW):
            row = []
            for j in range(ITEM_IN_ROW):
                row.append(tk.Canvas(master= self.board,width = W0/4-6,height = W0/4-6,bg = TILE_COLORS[0][0]))
                print('grid')
                row[j].grid(row = i,column = j)
            self.tiles.append(row)


    def get_free_tiles(self):
        pass


    def add_new_tile(self):
        # new_tile = random.choice(["2","4"])
        # print(new_tile)
        # free_tiles = self.get_free_tiles()
        pass

    def game(self):
        self.setup_init_tiles()
        flag = True
        while flag:
            self.add_new_tile()
            
            

        # randomly generate on a free tile 2 or 4 
        # check how many tiles are taken
        # if 
        
        

if __name__ == "__main__":
    root = tk.Tk()
    root.focus_set()
    game = Game(root)
    root.mainloop()
