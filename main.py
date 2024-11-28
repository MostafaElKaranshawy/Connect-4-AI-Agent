import customtkinter as ctk
from tkinter import messagebox
import math

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
    def __init__(self, master, exit_game, game_mode, k, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.k = k
        self.exit_game = exit_game
        self.game_mode = game_mode  # Store the game mode
        self.current_player = 1  # Player 1 starts

        self.game_frame = ctk.CTkFrame(self,width=700, height=700)
        self.game_frame.pack(pady=50, padx=50)
        self.board = [[0] * COLS for _ in range(ROWS)]  # Initialize empty board
        self.configure(fg_color=BG_COLOR)

        # Header for column selection
        self.header_tiles = []
        self.create_header()

        # Create the main board
        self.tiles = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.create_board()

        # Exit button
        exit_button = ctk.CTkButton(
            self,
            text="Exit Game",
            command=self.show_exit_confirmation,
            fg_color="#FF6347",
            text_color="white",
            font=("Times New Roman", 20),
        )
        exit_button.pack(pady=10)

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
            tile.bind("<Leave>", lambda event, c=col: self.on_hover_leave(c))
            tile.bind("<Button-1>", lambda event, c=col: self.drop_token(c))

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

    def on_hover_enter(self, col):
        """Change header tile color on hover based on current player."""
        color = PLAYER_1_COLOR_HEADER if self.current_player == 1 else PLAYER_2_COLOR_HEADER
        self.header_tiles[col].configure(fg_color=color)

    def on_hover_leave(self, col):
        """Reset header tile color when hover leaves."""
        self.header_tiles[col].configure(fg_color="transparent")

    def drop_token(self, col):
        """Drop the token into the specified column."""
        for row in reversed(range(ROWS)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                color = PLAYER_1_COLOR if self.current_player == 1 else PLAYER_2_COLOR
                self.tiles[row][col].configure(fg_color=color)
                if self.check_winner(row, col):
                    self.show_winner()
                else:
                    self.current_player = 3 - self.current_player  # Switch player

                if self.game_mode == "player_vs_computer" and self.current_player == 2:
                    self.computer_turn()

                return

        messagebox.showwarning("Column Full", "This column is full. Try a different one.")

    def check_winner(self, row, col):
        """Check for a winner after a token is placed."""

        def count_in_direction(delta_row, delta_col):
            count = 0
            r, c = row, col
            while 0 <= r < ROWS and 0 <= c < COLS and self.board[r][c] == self.current_player:
                count += 1
                r += delta_row
                c += delta_col
            return count

        # Check all directions: horizontal, vertical, diagonal (both ways)
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            if count_in_direction(dr, dc) + count_in_direction(-dr, -dc) - 1 >= 4:
                return True
        return False

    def show_winner(self):
        """Display the winner and reset the game."""
        winner = f"Player {self.current_player} ({PLAYER_1_COLOR if self.current_player == 1 else PLAYER_2_COLOR}) wins!"
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

    def computer_turn(self):
        """Simulate the computer's turn using the Minimax algorithm."""
        print("Computer is thinking...")
        best_move, _ = self.minimax(self.board, self.k, -math.inf, math.inf, True)
        print(f"Best move for computer: Column {best_move}")
        self.drop_token(best_move)

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        """The Minimax algorithm with alpha-beta pruning to simulate a computer's move."""
        if depth == 0 or self.is_game_over(board):
            return -1, self.evaluate_board(board)

        available_moves = [col for col in range(COLS) if board[0][col] == 0]
        best_move = available_moves[0]

        if is_maximizing:
            max_eval = -math.inf
            for move in available_moves:
                new_board = self.simulate_move(board, move, 2)  # Computer's move
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move, max_eval
        else:
            min_eval = math.inf
            for move in available_moves:
                new_board = self.simulate_move(board, move, 1)  # Player's move
                eval, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, min_eval

    def evaluate_board(self, board):
        """Evaluate the current board to score it for the Minimax algorithm."""
        # You can implement your evaluation function here
        return 0  # Placeholder for evaluation function

    def simulate_move(self, board, col, player):
        """Simulate a move without changing the actual game board."""
        new_board = [row[:] for row in board]  # Copy of the board
        for row in reversed(range(ROWS)):
            if new_board[row][col] == 0:
                new_board[row][col] = player
                break
        return new_board

    def is_game_over(self, board):
        """Check if the game is over (win or full board)."""
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
        self.grid_rowconfigure(0, weight=1, pad=20, minsize=500)
        self.grid_columnconfigure(0, weight=1, pad=20, minsize=500)

        # Title label
        title_label = ctk.CTkLabel(self, text="Connect 4 Game", font=("Times New Roman", 30, "bold"), text_color='white')
        title_label.grid(row=0, column=0, pady=10)

        # Input field for K value
        self.k_entry = ctk.CTkEntry(self, placeholder_text="Enter K value" ,font=("Times New Roman", 20))
        self.k_entry.grid(row=1, column=0, pady=10)  # Ensure it takes available width
        self.k_entry._set_dimensions(200, 50)
        # Buttons for game modes
        player_vs_computer_button = ctk.CTkButton(
            self,
            text="Player 1 vs Computer",
            command=self.on_player_vs_computer,
            fg_color=PLAYER_1_BACKGROUND_COLOR,
            text_color="white",
            font=("Times New Roman", 20),
        )
        player_vs_computer_button.grid(row=2, column=0, pady=10)
        player_vs_computer_button._set_dimensions(200, 50)
        computer_vs_player_button = ctk.CTkButton(
            self,
            text="Computer vs Player 1",
            command=self.on_computer_vs_player,
            fg_color=PLAYER_2_BACKGROUND_COLOR,
            text_color="white",
            font=("Times New Roman", 20),
        )
        computer_vs_player_button.grid(row=3, column=0, pady=10)
        computer_vs_player_button._set_dimensions(200, 50)

        # Exit Button
        exit_button = ctk.CTkButton(
            self,
            text="Exit",
            command=self.show_exit_confirmation,
            fg_color="#FF6347",
            text_color="white",
            font=("Times New Roman", 20),
        )
        exit_button.grid(row=4, column=0, pady=10)
        exit_button._set_dimensions(200, 50)
    def on_player_vs_computer(self):
        """Start the game with Player 1 vs Computer."""
        k_value = self.get_k_value()
        if k_value:
            self.start_game("player_vs_computer", k_value)

    def on_computer_vs_player(self):
        """Start the game with Computer vs Player 1."""
        k_value = self.get_k_value()
        if k_value:
            self.start_game("computer_vs_player", k_value)

    def get_k_value(self):
        """Get the K value from the input field."""
        try:
            k_value = int(self.k_entry.get())
            if k_value < 4:  # Assuming a minimum winning length of 4
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

    def start_game(self, game_mode, k):
        """Switch to the game board screen with the selected mode."""
        self.options_screen.grid_forget()  # Hide the options screen
        self.game_screen = GameBoard(self, self.show_options, game_mode, k)
        self.game_screen.grid(row=0, column=0, sticky="nsew")  # Use grid() instead of pack()

    def show_options(self):
        """Go back to the options screen."""
        self.game_screen.grid_forget()  # Hide the game screen
        self.options_screen.grid(row=0, column=0, sticky="nsew")  # Show the options screen using grid()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
