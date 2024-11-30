from tkinter.constants import (DISABLED, NORMAL)
import customtkinter as ctk
from tkinter import messagebox, Canvas, Scrollbar
from methods import Methods

COLS = 7
ROWS = 6
PLAYER_1_COLOR = "red"
PLAYER_2_COLOR = "yellow"  # Steel Blue
PLAYER_1_COLOR_HEADER = "#FF0000"
PLAYER_2_COLOR_HEADER = "#FFFF00"
PLAYER_1_BACKGROUND_COLOR = "#1E90FF"  # Dodger Blue
PLAYER_2_BACKGROUND_COLOR = "#4682B4"
EMPTY_COLOR = "#B0C4DE"  # Light Steel Blue
BG_COLOR = "lightblue"  # Sky Blue


class GameBoard(ctk.CTkFrame):
    def __init__(self, master, exit_game, game_mode, k, method, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.k = k
        self.exit_game = exit_game
        self.game_mode = game_mode  # Store the game mode
        self.current_player = 1  # Player 1 starts
        self.method = method
        self.algorithm = Methods(method, game_mode, k)
        self.game_started = False
        self.player1_score = 0
        self.player2_score = 0
        self.player1 = "Player 1" if game_mode == 2 else "Computer"
        self.player2 = "Player 2" if game_mode == 1 else "Computer"

        self.canvas = Canvas(self)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas
        self.content_frame = ctk.CTkFrame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Bind the configuration to update the scrollable region
        self.content_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Center the content_frame within the window
        self.place(relx=0.5, rely=0.5, anchor="center")

        # Set the window size to fit the content
        self.master.geometry("800x1200")  # Adjust this based on your layout

        # Add widgets inside content_frame (this frame will be scrollable)
        self.score_board = ctk.CTkFrame(self.content_frame, width=500, height=500, bg_color="transparent")
        self.score_board_player1 = ctk.CTkLabel(self.score_board, text=f"{self.player1}: {self.player1_score}",
                                                font=("Times New Roman", 30, "bold", "italic"),
                                                text_color='blue', fg_color="transparent")
        self.score_board_player2 = ctk.CTkLabel(self.score_board, text=f"{self.player2}: {self.player2_score}",
                                                font=("Times New Roman", 30, "bold", "italic"),
                                                text_color='blue', fg_color="transparent")
        self.score_board.pack(pady=10)
        self.score_board_player1.pack(pady=10)
        self.score_board_player2.pack(pady=10)

        self.game_frame = ctk.CTkFrame(self.content_frame, width=700, height=700)
        self.game_frame.pack(pady=50, padx=50)
        self.board = [[0] * COLS for _ in range(ROWS)]  # Initialize empty board
        self.configure(fg_color=BG_COLOR)


        # Header for column selection
        self.header_tiles = []
        self.create_header()

        # Create the main board
        self.tiles = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.create_board()

        self.buttons = ctk.CTkFrame(self.content_frame, width=500, height=300, bg_color="transparent")
        self.buttons.pack(pady=10)

        self.start_game_button = ctk.CTkButton(
            self.buttons,
            text="Start Game",
            fg_color='green',
            command=self.start_game,
            text_color='white',
            font=("Times New Roman", 20),
        )
        self.start_game_button.pack(side="left", padx=10, pady=10)

        exit_button = ctk.CTkButton(
            self.buttons,
            text="Exit Game",
            command=self.show_exit_confirmation,
            fg_color="#FF6347",
            text_color="white",
            font=("Times New Roman", 20),
        )
        exit_button.pack(side="left", padx=10, pady=10)

    def create_header(self):
        """Create interactive header tiles above the board."""
        header_frame = ctk.CTkFrame(self.game_frame, fg_color="transparent")
        header_frame.pack(pady=10)

        # Configure columns to make them equal width
        for col in range(COLS):
            header_frame.grid_columnconfigure(col, weight=1, minsize=80)  # Set minimum size of 80px

        for col in range(COLS):
            tile = ctk.CTkLabel(
                header_frame,
                text="",
                fg_color="transparent",
                width=80,
                height=80,
                corner_radius=40,
            )
            tile.grid(row=0, column=col, padx=10, pady=5)
            self.header_tiles.append(tile)
            tile.bind("<Enter>", lambda event, c=col: self.on_hover_enter(c))
            tile.bind("<Motion>", lambda event, c=col: self.on_hover_enter(c))
            tile.bind("<Leave>", lambda event, c=col: self.on_hover_leave(c))
            tile.bind("<Button-1>", lambda event, c=col: self.human_turn(c))

    def create_board(self):
        """Create the Connect 4 board."""
        board_frame = ctk.CTkFrame(self.game_frame, fg_color="blue", corner_radius=10)
        board_frame.pack(pady=30)

        # Configure the rows and columns of the board
        for col in range(COLS):
            board_frame.grid_columnconfigure(col, weight=1, minsize=80)  # Set minimum size of 80px
        for row in range(ROWS):
            board_frame.grid_rowconfigure(row, weight=1, minsize=80)  # Set minimum size of 80px

        for row in range(ROWS):
            for col in range(COLS):
                tile = ctk.CTkLabel(
                    board_frame,
                    text="",
                    fg_color=EMPTY_COLOR,
                    width=80,
                    height=80,
                    corner_radius=40,
                )
                tile.grid(row=row, column=col, padx=10, pady=5)
                self.tiles[row][col] = tile

    def start_game(self):
        """Start a new game."""
        self.start_game_button.configure(state=DISABLED)
        self.reset_board()
        self.game_started = True
        self.update_idletasks()  # Force the UI to update immediately
        if self.current_player == self.game_mode:
            self.computer_turn()

    def on_hover_enter(self, col):
        """Change header tile color on hover based on current player."""
        if self.current_player == self.game_mode or (not self.game_started):
            self.header_tiles[col].configure(fg_color="transparent")
            return
        color = PLAYER_1_COLOR_HEADER if self.current_player == 1 else PLAYER_2_COLOR_HEADER
        self.header_tiles[col].configure(fg_color=color)

        self.update_idletasks()  # Force the UI to update immediately

    def on_hover_leave(self, col):
        """Reset header tile color when hover leaves."""
        self.header_tiles[col].configure(fg_color="transparent")
        self.update_idletasks()  # Force the UI to update immediately

    def drop_token(self, col):
        """Drop the token into the specified column."""
        for row in reversed(range(ROWS)):
            if self.board[row][col] == 0:
                color = PLAYER_1_COLOR if self.current_player == 1 else PLAYER_2_COLOR
                self.tiles[row][col].configure(fg_color=color)  # Update the visual tile
                self.board[row][col] = self.current_player  # Update the logical board state

                self.header_tiles[col].configure(fg_color="transparent")
                self.update_idletasks()  # Force the UI to update immediately
                self.compute_scores(row, col, self.current_player)  # Compute scores after updates
                self.current_player = 2 if self.current_player == 1 else 1  # Switch the current player

                # Check if the game is over
                if self.is_game_over(self.board):
                    self.show_winner()
                    return

                # Handle computer's turn if applicable
                if self.game_mode == self.current_player:
                    self.computer_turn()

                return
        messagebox.showwarning("Column Full", "This column is full. Try a different one.")

    def compute_scores(self, row, col, player_turn):

        # check for the row up
        count = 0
        for i in range(0,4):
            if row + i < ROWS:
                if self.board[row + i][col] == player_turn:
                    count += 1
                else:
                    break
        if count == 4:
            if player_turn == 1:
                self.player1_score += 1
            else:
                self.player2_score += 1

        count = 0
        for i in range(0,4):
            if row - i >= 0:
                if self.board[row - i][col] == player_turn:
                    count += 1
                else:
                    break
        if count == 4:
            if player_turn == 1:
                self.player1_score += 1
            else:
                self.player2_score += 1

        count = 0
        for i in range(0,4):
            if col + i < COLS:
                if self.board[row][col + i] == player_turn:
                    count += 1
                else:
                    break
        if count == 4:
            if player_turn == 1:
                self.player1_score += 1
            else:
                self.player2_score += 1

        count = 0
        for i in range(0,4):
            if col - i >= 0:
                if self.board[row][col - i] == player_turn:
                    count += 1
                else:
                    break
        if count == 4:
            if player_turn == 1:
                self.player1_score += 1
            else:
                self.player2_score += 1

        self.update_score_board(self.player1_score, self.player2_score)
        return

    def update_score_board(self, player1_score, player2_score):
        self.score_board_player1.configure(text=f"{self.player1}: {player1_score}")
        self.score_board_player2.configure(text=f"{self.player2}: {player2_score}")


    def show_winner(self):
        """Display the winner and reset the game."""
        winner = ""
        if self.player1_score > self.player2_score:
            winner = f"{self.player1} ({PLAYER_1_COLOR}) wins!"
        else:
            winner = f"{self.player2} ({PLAYER_2_COLOR}) wins!"
        if messagebox.askyesno("Game Over", f"{winner}\n\nDo you want to play again?"):
            self.reset_board()
        else:
            self.exit_game()

    def reset_board(self):
        """Reset the board for a new game."""
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.current_player = 1
        for row in range(ROWS):
            for col in range(COLS):
                self.tiles[row][col].configure(fg_color=EMPTY_COLOR)

    def show_exit_confirmation(self):
        """Show a confirmation dialog when the user tries to exit the game."""
        response = messagebox.askyesno("Exit Game", "Are you sure you want to exit the current game?")
        if response:
            self.exit_game()
    def human_turn(self, col):
        if self.current_player == self.game_mode or not self.game_started:
            return
        self.drop_token(col)
    def computer_turn(self):
        if self.player1 == "Computer":
            self.score_board_player1.configure(text=f"{self.player1}: {self.player1_score}\tComputer is thinking....")
        else:
            self.score_board_player2.configure(text=f"{self.player2}: {self.player2_score}\tComputer is thinking....")
        self.update_idletasks()  # Force the UI to update immediately
        best_move = self.algorithm.computer_choice(board=self.board)
        if self.player1 == "Computer":
            self.score_board_player1.configure(text=f"{self.player1}: {self.player1_score}")
        else:
            self.score_board_player2.configure(text=f"{self.player2}: {self.player2_score}")
        print(f"Best move for computer: Column {best_move}")
        self.drop_token(best_move)

    def is_game_over(self, board):
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == 0:
                    return False
        return True

class OptionsMenu(ctk.CTkFrame):
    def __init__(self, master, start_game, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.start_game = start_game
        self.configure(fg_color=BG_COLOR)

        # Set the frame to expand and fill the entire screen
        self.grid_rowconfigure(0, weight=1, pad=20, minsize=200)
        self.grid_columnconfigure(0, weight=1, pad=20, minsize=500)

        # Title label
        title_label = ctk.CTkLabel(self, text="Connect 4 Game", font=("Times New Roman", 30, "bold"),
                                   text_color='white')
        title_label.grid(row=0, column=0, pady=10)

        # Input field for K value
        self.k_entry = ctk.CTkEntry(self, placeholder_text="Enter K value", font=("Times New Roman", 20))
        self.k_entry.grid(row=1, column=0, pady=10)
        self.k_entry._set_dimensions(300, 30)

        # Game mode options
        method_options = ["Minmax without pruning", "Alpha-beta Minmax", "Expectiminmax"]

        # Create a CTkComboBox for overall game mode
        self.method_combo_box = ctk.CTkComboBox(self, values=method_options, width=200, font=("Times New Roman", 20))
        self.method_combo_box.set("Select an option")
        self.method_combo_box.grid(row=2, column=0, pady=10)
        self.method_combo_box._set_dimensions(300, 30)

        # Drop-down menu for selecting player vs computer settings
        self.mode_options = ["Computer as player1", "Computer as player2"]
        self.mode_combo_box = ctk.CTkComboBox(self, values=self.mode_options, width=200, font=("Times New Roman", 20))
        self.mode_combo_box.set("Choose computer player turn")
        self.mode_combo_box.grid(row=3, column=0, pady=10)
        self.mode_combo_box._set_dimensions(300, 30)

        # Button to confirm selection and start the game
        start_button = ctk.CTkButton(
            self,
            text="Start Game",
            command=self.start_game_with_settings,
            fg_color="green",
            text_color="white",
            font=("Times New Roman", 20),
        )
        start_button.grid(row=4, column=0, pady=10)
        start_button._set_dimensions(300, 30)

        # Exit Button
        exit_button = ctk.CTkButton(
            self,
            text="Exit",
            command=self.show_exit_confirmation,
            fg_color="red",
            text_color="white",
            font=("Times New Roman", 20),
        )
        exit_button.grid(row=5, column=0, pady=10)
        exit_button._set_dimensions(300, 30)


    def start_game_with_settings(self):
        k_value = self.get_k_value()
        if not k_value:
            return
        mode = self.mode_combo_box.get()
        method = self.method_combo_box.get()
        if mode == "Computer as player1":
            self.start_game(1, k_value, method)
        elif mode == "Computer as player2":
            self.start_game(2, k_value, method)

    def get_k_value(self):
        """Get the K value from the input field."""
        try:
            k_value = int(self.k_entry.get())
            if k_value < 0:  # Assuming a minimum winning length of 4
                raise ValueError("K value must be at least 4.")
            return k_value
        except ValueError as e:
            # Show error if the input is invalid
            messagebox.showwarning(
                title="Invalid Input",
                message="Please Enter a valid k value"
            )
            return None
    def show_exit_confirmation(self):
        """Show a confirmation dialog when the user tries to exit the game."""
        response = messagebox.askyesno("Exit Game", "Are you sure you want to exit the game?")
        if response:
            self.quit()


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.game_screen = None
        self.title("Connect 4")
        # self.geometry("700x800")

        # Use blue color scheme for the app
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Configure rows and columns for grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create and show the options screen initially
        self.options_screen = OptionsMenu(self, self.start_game)
        self.options_screen.grid(row=0, column=0, sticky="nsew")  # Use grid() instead of pack()

    def start_game(self, computer_turn, k, method):
        """Switch to the game board screen with the selected mode."""
        self.options_screen.grid_forget()  # Hide the options screen
        self.game_screen = GameBoard(self, self.show_options, computer_turn, k, method)
        self.game_screen.grid(row=0, column=0, sticky="nsew")  # Use grid() instead of pack()

    def show_options(self):
        """Go back to the options screen."""
        self.game_screen.grid_forget()  # Hide the game screen
        self.options_screen.grid(row=0, column=0, sticky="nsew")  # Show the options screen using grid()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
