import tkinter as tk
from tkinter import font

class TikTacToeBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tik Tac Toe Board")
        self._cells = {}
        self._create_board_display()
        self._create_board_grid()

    
    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display= tk.Label(
            master = display_frame,
            text = "Make the first move!",
            font = font.Font(size=28, weight="bold")
        )

        self.display.pack()

    
    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        number_of_rows = 3
        number_of_cols = 3

        for row in range(number_of_rows):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)

            for col in range(number_of_cols):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    height=2,
                    width=4,
                    highlightbackground="lightblue"
                )

                self._cells[button] = (row, col)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )


def main():
    board = TikTacToeBoard()
    board.mainloop()


if __name__ == "__main__":
    main()