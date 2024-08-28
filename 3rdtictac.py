import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.current_player = "X"
        self.board = [["" for _ in range(5)] for _ in range(5)]  # Updated for 5x5 grid
        self.buttons = [[None for _ in range(5)] for _ in range(5)]  # Updated for 5x5 grid
        self.history = []
        self.scores = {"X": 0, "O": 0, "Draw": 0}
        self.create_widgets(root)
        self.update_score_labels()
        self.update_turn_message()

    def create_widgets(self, root):
        self.player_x_name = tk.StringVar(value="Player X")
        self.player_o_name = tk.StringVar(value="Player O")
        
        tk.Label(root, text="Player X:").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.player_x_name).grid(row=0, column=1)
        tk.Label(root, text="Player O:").grid(row=0, column=2)
        tk.Entry(root, textvariable=self.player_o_name).grid(row=0, column=3)
        
        self.score_label_x = tk.Label(root, text=f"(´°̥̥̥̥̥̥̥̥ω°̥̥̥̥̥̥̥̥｀): {self.scores['X']}")
        self.score_label_x.grid(row=1, column=0)
        self.score_label_o = tk.Label(root, text=f"(⌐■_■): {self.scores['O']}")
        self.score_label_o.grid(row=1, column=1)
        self.score_label_draw = tk.Label(root, text=f"Draw: {self.scores['Draw']}")
        self.score_label_draw.grid(row=1, column=2)
        
        self.turn_label = tk.Label(root, text="")
        self.turn_label.grid(row=2, column=0, columnspan=5)  # Message Board

        for row in range(5):  # Updated for 5x5 grid
            for col in range(5):  # Updated for 5x5 grid
                button = tk.Button(root, text="", width=10, height=3, bg='black', fg='white', command=lambda r=row, c=col: self.button_click(r, c))
                button.grid(row=row+3, column=col)
                self.buttons[row][col] = button
                
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_game)
        self.reset_button.grid(row=8, column=0, columnspan=3, pady=10)
        
        self.undo_button = tk.Button(root, text="Undo", command=self.undo_move)
        self.undo_button.grid(row=8, column=3, pady=10)

    def button_click(self, row, col):
        if self.board[row][col] == "" and not self.check_winner():
            self.history.append((row, col, self.current_player))
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.get_symbol(self.current_player))
            winner = self.check_winner()
            if winner:
                messagebox.showinfo("Game Over", f"{self.get_current_player_name()} wins!")
                self.scores[winner] += 1
                self.update_score_labels()
            elif all(self.board[r][c] != "" for r in range(5) for c in range(5)):  # Updated for 5x5 grid
                messagebox.showinfo("Game Over", "It's a draw!")
                self.scores["Draw"] += 1
                self.update_score_labels()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.update_turn_message()

    def check_winner(self):
        winning_combinations = []

        # Horizontal, Vertical, and Diagonal combinations for 5x5 grid
        for i in range(5):
            # Horizontal
            winning_combinations.append([(i, j) for j in range(5)])
            # Vertical
            winning_combinations.append([(j, i) for j in range(5)])

        # Diagonals
        winning_combinations.append([(i, i) for i in range(5)])
        winning_combinations.append([(i, 4 - i) for i in range(5)])

        for combo in winning_combinations:
            if all(self.board[row][col] == self.current_player and self.board[row][col] != "" for row, col in combo):
                self.highlight_winning_line(combo)
                return self.current_player
        return None

    def highlight_winning_line(self, combo):
        for position in combo:
            row, col = position
            self.buttons[row][col].config(bg="green")

    def undo_move(self):
        if self.history:
            row, col, player = self.history.pop()
            self.board[row][col] = ""
            self.buttons[row][col].config(text="", bg='black')
            self.current_player = player
            self.update_turn_message()

    def reset_game(self):
        self.board = [["" for _ in range(5)] for _ in range(5)]  # Updated for 5x5 grid
        for row in range(5):  # Updated for 5x5 grid
            for col in range(5):  # Updated for 5x5 grid
                self.buttons[row][col].config(text="", bg='black')
        self.history.clear()
        self.current_player = "X"
        self.update_turn_message()

    def update_score_labels(self):
        self.score_label_x.config(text=f"(´°̥̥̥̥̥̥̥̥ω°̥̥̥̥̥̥̥̥｀): {self.scores['X']}")
        self.score_label_o.config(text=f"(⌐■_■): {self.scores['O']}")
        self.score_label_draw.config(text=f"Draw: {self.scores['Draw']}")

    def update_turn_message(self):
        player_name = self.get_current_player_name()
        self.turn_label.config(text=f"{player_name}'s turn")

    def get_current_player_name(self):
        return self.player_x_name.get() if self.current_player == "X" else self.player_o_name.get()

    def get_symbol(self, player):
        return "(´°̥̥̥̥̥̥̥̥ω°̥̥̥̥̥̥̥̥｀)" if player == "X" else "(⌐■_■)"

# Create the main window
root = tk.Tk()
root.title("Tic-Tac-Toe")
game = TicTacToe(root)
root.mainloop()
