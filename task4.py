import tkinter as tk
from tkinter import ttk
W0 = 400
TILE_COLORS = {
        0: ("ivory", "#ivory"),
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
        self.board = tk.Frame(master= self.root,width =W0,height= W0+100)
        self.board.pack()
        self.main_canvas = tk.Canvas(master = self.board,width =W0,height= W0,bg ="ivory")
        self.main_canvas.pack()
        self.setup_init_tiles()

    def setup_init_tiles(self):
        self.tiles = []
        
        

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()
