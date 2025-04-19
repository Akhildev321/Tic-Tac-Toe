import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.player = "X"
        self.buttons = [[None]*3 for _ in range(3)]
        self.score = {"X": 0, "O": 0}
        self.vs_ai = False
        self.create_widgets()

    def create_widgets(self):
        # Mode selector
        mode_frame = tk.Frame(self.root)
        mode_frame.pack()
        tk.Button(mode_frame, text="Player vs Player", command=self.start_pvp).pack(side="left", padx=5)
        tk.Button(mode_frame, text="Player vs AI", command=self.start_ai).pack(side="left", padx=5)

        # Scoreboard
        self.score_label = tk.Label(self.root, text="Score - X: 0 | O: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)

        # Board
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.board_frame, text=" ", font=("Arial", 24), width=5, height=2,
                                   command=lambda r=i, c=j: self.on_click(r, c))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def start_pvp(self):
        self.vs_ai = False
        self.reset_board()

    def start_ai(self):
        self.vs_ai = True
        self.reset_board()

    def reset_board(self):
        self.player = "X"
        for row in self.buttons:
            for button in row:
                button.config(text=" ", state=tk.NORMAL)

    def on_click(self, r, c):
        if self.buttons[r][c]['text'] == " ":
            self.buttons[r][c]['text'] = self.player
            self.buttons[r][c]['state'] = tk.DISABLED
            if self.check_winner():
                self.score[self.player] += 1
                self.score_label.config(text=f"Score - X: {self.score['X']} | O: {self.score['O']}")
                messagebox.showinfo("Game Over", f"Player {self.player} wins!")
                self.ask_restart()
                return
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.ask_restart()
                return

            # Switch player or play AI move
            if self.vs_ai:
                self.player = "O"
                self.root.after(500, self.ai_move)
            else:
                self.player = "O" if self.player == "X" else "X"

    def ai_move(self):
        # Basic AI: Random available move
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.buttons[i][j]['text'] == " "]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.buttons[r][c]['text'] = "O"
            self.buttons[r][c]['state'] = tk.DISABLED
            if self.check_winner():
                self.score["O"] += 1
                self.score_label.config(text=f"Score - X: {self.score['X']} | O: {self.score['O']}")
                messagebox.showinfo("Game Over", "AI wins!")
                self.ask_restart()
                return
            elif self.is_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.ask_restart()
                return
        self.player = "X"

    def check_winner(self):
        b = self.buttons
        for i in range(3):
            if b[i][0]['text'] == b[i][1]['text'] == b[i][2]['text'] != " ":
                return True
            if b[0][i]['text'] == b[1][i]['text'] == b[2][i]['text'] != " ":
                return True
        if b[0][0]['text'] == b[1][1]['text'] == b[2][2]['text'] != " ":
            return True
        if b[0][2]['text'] == b[1][1]['text'] == b[2][0]['text'] != " ":
            return True
        return False

    def is_draw(self):
        return all(button['text'] != " " for row in self.buttons for button in row)

    def ask_restart(self):
        if messagebox.askyesno("Play Again?", "Do you want to play again?"):
            self.reset_board()
        else:
            self.root.quit()
