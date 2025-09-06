import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic-Tac-Toe")

        # Create buttons with some styling
        for i in range(9):
            btn = tk.Button(self.root, text="", font=("Helvetica", 24), height=2, width=5,
                            command=lambda i=i: self.make_move(i))
            btn.grid(row=i // 3, column=i % 3)

        self.current_player = "X"
        self.board = [""] * 9

    def make_move(self, index):
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.update_button_text(index)
            if self.check_winner():
                messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                self.root.quit()
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a tie!")
                self.root.quit()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def update_button_text(self, index):
        btn = self.root.grid_slaves(row=index // 3, column=index % 3)[0]
        btn.config(text=self.board[index])  # type: ignore

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]

        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != "":
                return True
        return False

if __name__ == "__main__":
    game = TicTacToe()
    game.root.mainloop()
