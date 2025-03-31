import tkinter as tk
import random

# Colors for tiles
COLORS = {
    0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
    16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
    256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
}

class Game2048:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("2048 Game")
        self.board = [[0] * 4 for _ in range(4)]
        self.setup_ui()
        self.start_game()
        self.root.mainloop()

    def setup_ui(self):
        """Create the game grid UI."""
        self.cells = []
        self.frame = tk.Frame(self.root, bg="#bbada0", padx=10, pady=10)
        self.frame.grid()

        for r in range(4):
            row = []
            for c in range(4):
                label = tk.Label(self.frame, text="", font=("Arial", 24, "bold"), width=4, height=2, 
                                 bg=COLORS[0], fg="black", relief="solid", bd=2)
                label.grid(row=r, column=c, padx=5, pady=5)
                row.append(label)
            self.cells.append(row)

        self.root.bind("<KeyPress>", self.handle_key)

    def start_game(self):
        """Initialize the game with two random tiles."""
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()

    def add_new_tile(self):
        """Add a new tile (2 or 4) at a random empty position."""
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.board[r][c] = 2 if random.random() < 0.9 else 4

    def update_ui(self):
        """Update the UI to reflect the current board state."""
        for r in range(4):
            for c in range(4):
                value = self.board[r][c]
                self.cells[r][c].config(text=str(value) if value else "", bg=COLORS[value])
        self.root.update_idletasks()

    def compress(self, board):
        """Slide all tiles left."""
        new_board = [[0] * 4 for _ in range(4)]
        for r in range(4):
            pos = 0
            for c in range(4):
                if board[r][c] != 0:
                    new_board[r][pos] = board[r][c]
                    pos += 1
        return new_board

    def merge(self, board):
        """Merge adjacent equal tiles."""
        for r in range(4):
            for c in range(3):
                if board[r][c] == board[r][c+1] and board[r][c] != 0:
                    board[r][c] *= 2
                    board[r][c+1] = 0
        return board

    def reverse(self, board):
        """Reverse rows (used for right movement)."""
        return [row[::-1] for row in board]

    def transpose(self, board):
        """Transpose rows and columns (used for up/down movements)."""
        return [list(row) for row in zip(*board)]

    def move_left(self, board):
        return self.compress(self.merge(self.compress(board)))

    def move_right(self, board):
        return self.reverse(self.move_left(self.reverse(board)))

    def move_up(self, board):
        return self.transpose(self.move_left(self.transpose(board)))

    def move_down(self, board):
        return self.transpose(self.move_right(self.transpose(board)))

    def check_win(self):
        """Check if the player has reached 2048."""
        return any(2048 in row for row in self.board)

    def is_game_over(self):
        """Check if there are no more valid moves."""
        if any(0 in row for row in self.board):
            return False
        for r in range(4):
            for c in range(3):
                if self.board[r][c] == self.board[r][c+1]:
                    return False
        for r in range(3):
            for c in range(4):
                if self.board[r][c] == self.board[r+1][c]:
                    return False
        return True

    def handle_key(self, event):
        """Handle user key presses for movement."""
        key_map = {
            "Up": self.move_up,
            "Down": self.move_down,
            "Left": self.move_left,
            "Right": self.move_right
        }
        if event.keysym in key_map:
            new_board = key_map[event.keysym](self.board)
            if new_board != self.board:
                self.board = new_board
                self.add_new_tile()
                self.update_ui()
                if self.check_win():
                    self.show_message("🎉 You Win!")
                elif self.is_game_over():
                    self.show_message("💀 Game Over!")

    def show_message(self, message):
        """Display a win/loss message."""
        popup = tk.Toplevel(self.root)
        popup.title("Game Over")
        label = tk.Label(popup, text=message, font=("Arial", 16, "bold"), padx=20, pady=20)
        label.pack()
        button = tk.Button(popup, text="OK", command=popup.destroy)
        button.pack()

if __name__ == "__main__":
    Game2048()
