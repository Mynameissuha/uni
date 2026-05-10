import tkinter as tk
from tkinter import ttk
import numpy as np
import random
import copy

W0 = 400
ITEM_IN_ROW = 4
TILE_COLORS = { 
    0: ("ivory", "ivory"),
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
    2048: ("#edc22e", "#f9f6f2")
}


class Game():
    def __init__(self, root):
        self.score = 0
        self.root = root
        
        self.board = tk.Frame(master=self.root, width=W0, height=W0, bg='#bbada0',padx=5,  pady=5)
        self.score_display = tk.Frame(master = self.root,width = W0,height = 30)
        
        self.mirror_grid = np.zeros((ITEM_IN_ROW, ITEM_IN_ROW), dtype=int)
        print("Initial Mirror Grid:\n", self.mirror_grid)

        # Binding events with keys
        self.root.bind('<Left>', self.handle_event)
        self.root.bind('<Right>', self.handle_event)
        self.root.bind('<Up>', self.handle_event)
        self.root.bind('<Down>', self.handle_event)
        self.root.bind('<Escape>', lambda event: root.quit())

        self.board.grid(row=0, column=0)
        self.score_display.grid(row =1,column = 0)
        self.label = tk.Label(master=self.score_display,text=self.score,font=('Helvetica', 24, 'bold'), width=4,height=2 )
        self.label.grid(row =0,column =0)
        self.setup_init_tiles()
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()
    

    def left_move(self,board):
        if not isinstance(board, np.ndarray):
            board = np.array(board)
        board_copy = board.copy()
        # print("MOVING LEFT\n")
        
        for i in range(4):
            row = board_copy[i]
            non_zero = [x for x in row if x != 0]
            merged = []
            j = 0
            while j < len(non_zero):
                if j + 1 < len(non_zero) and non_zero[j] == non_zero[j + 1]:
                    self.score += non_zero[j] * 2
                    merged.append(non_zero[j] * 2)
                    #skip next if merged
                    j += 2 
                else:
                    merged.append(non_zero[j])
                    j += 1
            
            merged.extend([0] * (4 - len(merged)))
            board_copy[i] = merged
        self.label.config(text = self.score)
        # print("\nFinal board:")
        # print(board_copy)
        return board_copy

    def handle_event(self, event):
        
        key_symbol = event.keysym
        
        
        if key_symbol in ['Left', 'Right', 'Up', 'Down']:
            
            print(f"{key_symbol} pressed. Move logic goes here.")

            if key_symbol == 'Left':
                board = self.left_move(self.mirror_grid)
                self.mirror_grid = board

            elif key_symbol == 'Right':
                print("MOVING RIGHT")
                reversed_board = self.mirror_grid.copy()
                reversed_board = reversed_board[:,::-1]
                board = self.left_move(reversed_board)
                print(f"MOVED RIGHT!:\n{board[:,::-1]}")
                self.mirror_grid = board[:,::-1]

            elif key_symbol == 'Up':
                print("MOVING UP")
                transposed_board = self.mirror_grid.copy()
                transposed_board = transposed_board.T
                board = self.left_move(transposed_board)
                print(f"MOVED UP!:\n{board.T}")
                self.mirror_grid = board.T

            elif key_symbol == 'Down':
                print("MOVING DOWN")
                deformed_board = self.mirror_grid.copy()
                deformed_board = deformed_board.T[:,::-1]
                board = self.left_move(deformed_board)
                print(f"MOVED DOWN!:\n{board.T[::-1,:]}")
                self.mirror_grid = board.T[::-1,:]
            self.add_new_tile()

        elif key_symbol == 'Escape':
            self.root.quit()
        else:
            print(f"Unknown key pressed: {key_symbol}")


    def setup_init_tiles(self):
        print("Setting up initial tiles (Canvases and Labels)")
        self.tiles = [] #
        self.tile_labels = [] 
        tile_size = W0 / ITEM_IN_ROW - 10 

        for i in range(ITEM_IN_ROW):
            row_tiles = []
            row_labels = []
            for j in range(ITEM_IN_ROW):
                
                tile_frame = tk.Frame(master=self.board,width=tile_size,height=tile_size,bg=TILE_COLORS[0][0] )
                tile_label = tk.Label(master=tile_frame,text='',font=('Helvetica', 24, 'bold'), width=4,height=2,bg=TILE_COLORS[0][0] )
                tile_frame.grid(row=i, column=j, padx=5, pady=5)
                
                tile_label.pack(expand=True, fill='both')

                row_tiles.append(tile_frame)
                row_labels.append(tile_label)
                
            self.tiles.append(row_tiles)
            self.tile_labels.append(row_labels)


    def get_free_tiles(self):
        # Returns a list in format (row, column) tuples where the mirror_grid value is 0
        free_tiles = []
        for r in range(ITEM_IN_ROW):
            for c in range(ITEM_IN_ROW):
                if self.mirror_grid[r, c] == 0:
                    free_tiles.append((r, c))
        return free_tiles

    def check_for_the_end(self):
        print('Checking for the end')
        init_board = self.mirror_grid.copy()
        #left
        left_board = self.left_move(init_board)
        print(f"IF MOVED LEFT")
                
        #right
        reversed_board = init_board.copy()
        reversed_board = reversed_board[:,::-1]
        board = self.left_move(reversed_board)
        print(f"IF MOVED RIGHT!:\n{board[:,::-1]}")
        right_board = board[:,::-1]

        #up
                
        transposed_board = init_board.copy()
        transposed_board = transposed_board.T
        board = self.left_move(transposed_board)
        print(f"IF MOVED UP!:\n{board.T}")
        up_board = board.T
        #down
        deformed_board = init_board.copy()
        deformed_board = deformed_board.T[:,::-1]
        board = self.left_move(deformed_board)
        print(f"IF MOVED DOWN!:\n{board.T[::-1,:]}")
        down_board = board.T[::-1,:]

        boards_unchanged_check = (np.array_equal(init_board, left_board) and np.array_equal(init_board, right_board) and np.array_equal(init_board, up_board) and np.array_equal(init_board, down_board))
        if boards_unchanged_check:
            print("=============================\n=============================\n\n\n\n\n\n\n\n\n         GAME OVER!         \n\n\n\n\n\n\n\n\n=============================\n=============================")
            

        

    def add_new_tile(self):
        free_tiles = self.get_free_tiles()
        if not free_tiles:
            self.check_for_the_end()
            return
        r,c = random.choice(free_tiles)
        
        # 90% chance for '2', 10% chance for '4'
        new_value = 2 if random.random() < 0.9 else 4
        self.mirror_grid[r, c] = new_value
        print(f"new grid:\n{self.mirror_grid}")
        self.update_ui()


    def update_ui(self):
        """Updates the colors and text of all UI labels based on the mirror grid."""
        for r in range(ITEM_IN_ROW):
            for c in range(ITEM_IN_ROW):
                value = self.mirror_grid[r, c]
                color_bg, color_fg = TILE_COLORS.get(value, ("black", "white"))

                # Update the tile background (Frame)
                self.tiles[r][c].config(bg=color_bg)

                # Update the tile label text and colors
                label = self.tile_labels[r][c]
                label.config(bg=color_bg,fg=color_fg,text=str(value) if value != 0 else '')
        free_tiles = self.get_free_tiles()
        if not free_tiles:
            self.check_for_the_end()
            
            return


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False) 
    
    app = Game(root)
    root.mainloop()