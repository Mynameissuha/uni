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
        self.root = root
        
        # 1. Setup the main frame for the board
        self.board = tk.Frame(
            master=self.root, 
            width=W0, 
            height=W0, 
            bg='#bbada0',
            padx=5, 
            pady=5
        )
        
        self.mirror_grid = np.zeros((ITEM_IN_ROW, ITEM_IN_ROW), dtype=int)
        print("Initial Mirror Grid:\n", self.mirror_grid)

        # Binding events with keys
        self.root.bind('<Left>', self.handle_event)
        self.root.bind('<Right>', self.handle_event)
        self.root.bind('<Up>', self.handle_event)
        self.root.bind('<Down>', self.handle_event)
        self.root.bind('<Escape>', lambda event: root.quit())

        # Place the board frame in the root window
        self.board.grid(row=0, column=0)
        
        # --- FIX: CALL THE SETUP FUNCTION HERE ---
        # This function creates and grids the actual tiles, making them visible.
        self.setup_init_tiles() 
        
        # Start the game by adding two initial tiles
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
                    merged.append(non_zero[j] * 2)
                    #skip next if merged
                    j += 2 
                else:
                    merged.append(non_zero[j])
                    j += 1
            
            merged.extend([0] * (4 - len(merged)))
            board_copy[i] = merged
        
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
        self.tiles = [] # This will hold the Canvas widgets
        self.tile_labels = [] # This will hold the Label widgets used for numbers
        tile_size = W0 / ITEM_IN_ROW - 10 # Adjusted size for padding/spacing

        for i in range(ITEM_IN_ROW):
            row_tiles = []
            row_labels = []
            for j in range(ITEM_IN_ROW):
                # Frame to hold the tile background and padding
                tile_frame = tk.Frame(
                    master=self.board,
                    width=tile_size,
                    height=tile_size,
                    bg=TILE_COLORS[0][0] # Background color for 0 tile (ivory)
                )
                
                # Label to display the number, centered inside the frame
                tile_label = tk.Label(
                    master=tile_frame,
                    text='',
                    font=('Helvetica', 24, 'bold'),
                    width=4,
                    height=2,
                    bg=TILE_COLORS[0][0] # Match the frame background
                )

                # Use grid to place the tile frame in the main board
                # padx/pady adds spacing between tiles
                tile_frame.grid(row=i, column=j, padx=5, pady=5)
                # Pack the label into its frame to center it
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


    def add_new_tile(self):
        free_tiles = self.get_free_tiles()
        if not free_tiles:
            print("Game over")
            return

        # Choose a random free position
        r, c = random.choice(free_tiles)
        
        # 90% chance of '2', 10% chance of '4'
        new_value = 2 if random.random() < 0.9 else 4
        
        # Update the mirror grid
        self.mirror_grid[r, c] = new_value
        print(f"Added new tile {new_value} at ({r}, {c})")
        
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
                label.config(
                    bg=color_bg,
                    fg=color_fg,
                    text=str(value) if value != 0 else ''
                )

    def game(self):
        # --- FIX: REMOVED THE WHILE LOOP ---
        # The game is now event-driven. Logic runs in __init__ and handle_event.
        print("Game loop placeholder. Tkinter mainloop handles events now.")
        pass

# --- Tkinter execution block ---
if __name__ == "__main__":
    # Initialize numpy array to zeros for easier handling
    np.set_printoptions(formatter={'int': '{:4}'.format}) 
    
    root = tk.Tk()
    # Make window non-resizable
    root.resizable(False, False) 
    
    app = Game(root)
    # This line starts the main event loop, which listens for clicks, key presses, etc.
    root.mainloop()