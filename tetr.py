import os
import tkinter as tk
import random
import pygame
import threading

# Initialize Pygame Mixer
pygame.mixer.init()

# Define constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
DELAY = 500

# Define Tetris shapes and their colors
SHAPES = [
    ([[1, 1, 1], [0, 1, 0]], "purple"),  # T-shape
    ([[1, 1, 1, 1]], "cyan"),            # I-shape
    ([[1, 1, 1], [1, 0, 0]], "blue"),    # L-shape
    ([[1, 1, 1], [0, 0, 1]], "orange"),  # J-shape
    ([[1, 1], [1, 1]], "yellow"),        # O-shape
    ([[0, 1, 1], [1, 1, 0]], "green"),   # S-shape
    ([[1, 1, 0], [0, 1, 1]], "red"),     # Z-shape
]

class Tetris:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tetris")
        
        # Make the window full screen
        self.window.attributes('-fullscreen', True)
        self.window.bind("<Escape>", self.exit_fullscreen)
        
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        # Calculate cell size based on screen size
        self.cell_size = min(self.screen_width // (GRID_WIDTH + 6), self.screen_height // GRID_HEIGHT)
        
        # Calculate dimensions for centering
        game_width = GRID_WIDTH * self.cell_size
        sidebar_width = 6 * self.cell_size
        total_width = game_width + sidebar_width
        offset_x = (self.screen_width - total_width) // 2

        # Create main frame
        self.main_frame = tk.Frame(self.window, bg="darkgray")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas for the game
        self.canvas = tk.Canvas(self.main_frame, width=GRID_WIDTH * self.cell_size, height=GRID_HEIGHT * self.cell_size, background="lightgray")
        self.canvas.place(x=offset_x, y=0)
        
        # Create frame for the scoreboard, hold feature, and next pieces
        self.frame = tk.Frame(self.main_frame, bg="darkgray")
        self.frame.place(x=offset_x + game_width, y=0, width=sidebar_width, height=self.screen_height)
        
        self.score_label = tk.Label(self.frame, text="Score: 0", font=("Arial", 16), bg="darkgray", fg="white")
        self.score_label.pack(pady=10)
        
        self.hold_label = tk.Label(self.frame, text="Hold", font=("Arial", 16), bg="darkgray", fg="white")
        self.hold_label.pack(pady=10)
        
        self.hold_canvas = tk.Canvas(self.frame, width=4 * self.cell_size, height=4 * self.cell_size, bg="darkgray")
        self.hold_canvas.pack(pady=10)
        
        self.next_label = tk.Label(self.frame, text="Next", font=("Arial", 16), bg="darkgray", fg="white")
        self.next_label.pack(pady=10)
        
        self.next_canvas = tk.Canvas(self.frame, width=4 * self.cell_size, height=12 * self.cell_size, bg="darkgray")
        self.next_canvas.pack(pady=10)
        
        self.pause_button = tk.Button(self.frame, text="Pause", font=("Arial", 16), command=self.toggle_pause)
        self.pause_button.pack(pady=20)

        self.quit_button = tk.Button(self.frame, text="Quit", font=("Arial", 16), command=self.quit_game)
        self.quit_button.pack(pady=10)

        self.score = 0
        self.combo = 0
        self.board = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece, self.current_color = self.new_piece()
        self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        self.hold_piece = None
        self.hold_used = False
        self.game_over = False
        self.hold_piece_old = None
        self.paused = False
        
        self.next_pieces = [self.new_piece() for _ in range(3)]
        
        self.window.bind("<KeyPress>", self.key_press)
        self.update()
        
        # Start background music
        self.play_background_music("song.wav")
        
        self.window.mainloop()

    def new_piece(self):
        return random.choice(SHAPES)

    def get_next_piece(self):
        piece = self.next_pieces.pop(0)
        self.next_pieces.append(self.new_piece())
        return piece

    def draw_board(self):
        self.canvas.delete("all")
        
        # Draw grid
        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                self.canvas.create_rectangle(c * self.cell_size, r * self.cell_size, (c + 1) * self.cell_size, (r + 1) * self.cell_size, outline="white")
        
        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                if self.board[r][c] != 0:
                    self.canvas.create_rectangle(c * self.cell_size, r * self.cell_size, (c + 1) * self.cell_size, (r + 1) * self.cell_size, fill=self.board[r][c])
        for r in range(len(self.current_piece)):
            for c in range(len(self.current_piece[r])):
                if self.current_piece[r][c] == 1:
                    self.canvas.create_rectangle((self.current_x + c) * self.cell_size, (self.current_y + r) * self.cell_size, (self.current_x + c + 1) * self.cell_size, (self.current_y + r + 1) * self.cell_size, fill=self.current_color)
        self.draw_hold()
        self.draw_next()

    def draw_hold(self):
        self.hold_canvas.delete("all")
        if self.hold_piece:
            piece, color = self.hold_piece
            for r in range(len(piece)):
                for c in range(len(piece[r])):
                    if piece[r][c] == 1:
                        self.hold_canvas.create_rectangle(c * self.cell_size, r * self.cell_size, (c + 1) * self.cell_size, (r + 1) * self.cell_size, fill=color)

    def draw_next(self):
        self.next_canvas.delete("all")
        for i, (piece, color) in enumerate(self.next_pieces):
            for r in range(len(piece)):
                for c in range(len(piece[r])):
                    if piece[r][c] == 1:
                        self.next_canvas.create_rectangle(c * self.cell_size, (i * 4 + r) * self.cell_size, (c + 1) * self.cell_size, ((i * 4 + r) + 1) * self.cell_size, fill=color)

    def move_piece(self, dx, dy):
        self.current_x += dx
        self.current_y += dy
        if self.collision():
            self.current_x -= dx
            self.current_y -= dy
            if dy != 0:
                self.lock_piece()
                lines_cleared = self.clear_lines()
                self.update_score(lines_cleared)
                self.current_piece, self.current_color = self.get_next_piece()
                self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
                self.current_y = 0
                self.hold_used = False
                if self.collision():
                    self.play_sound("game_over.wav")
                    self.game_over = True
                elif lines_cleared > 0:
                    if lines_cleared == 4:
                        self.play_sound("tetris.wav")
                    else:
                        self.play_sound("clear.wav")
                else:
                    self.play_sound("place.wav")

    def rotate_piece(self):
        new_piece = [list(row) for row in zip(*self.current_piece[::-1])]
        if not self.check_collision(new_piece):
            self.current_piece = new_piece

    def check_collision(self, piece):
        for r in range(len(piece)):
            for c in range(len(piece[r])):
                if piece[r][c] == 1:
                    if (r + self.current_y >= GRID_HEIGHT or
                        c + self.current_x < 0 or
                        c + self.current_x >= GRID_WIDTH or
                        self.board[r + self.current_y][c + self.current_x] != 0):
                        return True
        return False

    def collision(self):
        return self.check_collision(self.current_piece)

    def lock_piece(self):
        for r in range(len(self.current_piece)):
            for c in range(len(self.current_piece[r])):
                if self.current_piece[r][c] == 1:
                    self.board[self.current_y + r][self.current_x + c] = self.current_color

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = GRID_HEIGHT - len(new_board)
        if lines_cleared > 0:
            self.combo += 1
        else:
            self.combo = 0
        new_board = [[0 for _ in range(GRID_WIDTH)] for _ in range(lines_cleared)] + new_board
        self.board = new_board
        return lines_cleared

    def update_score(self, lines_cleared):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800
        self.score += self.combo * 50
        self.score_label.config(text=f"Score: {self.score}")

    def update(self):
        if not self.game_over and not self.paused:
            self.move_piece(0, 1)
            self.draw_board()
            self.window.after(DELAY, self.update)
        elif self.game_over:
            self.canvas.create_text(GRID_WIDTH * self.cell_size // 2, GRID_HEIGHT * self.cell_size // 2, text="Game Over", font=("Arial", 24), fill="red")

    def key_press(self, event):
        if event.keysym == "Left":
            self.move_piece(-1, 0)
        elif event.keysym == "Right":
            self.move_piece(1, 0)
        elif event.keysym == "Down":
            self.move_piece(0, 1)
        elif event.keysym == "Up":
            self.rotate_piece()
        elif event.keysym == "space":
            self.quick_drop()
        elif event.keysym == "c":
            self.hold()
        elif event.keysym == "p":
            self.toggle_pause()
        self.draw_board()

    def quick_drop(self):
        while not self.collision():
            self.current_y += 1
        self.current_y -= 1
        self.move_piece(0, 1)

    def hold(self):
        if not self.hold_used:
            self.play_sound("hold.wav")
            if self.hold_piece is not None:
                self.hold_piece_old = self.hold_piece
            else:
                self.hold_piece_old = self.new_piece()
            self.current_piece, self.hold_piece = self.hold_piece or (self.current_piece, self.current_color), (self.current_piece, self.current_color)
            self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
            self.current_y = 0
            if self.hold_piece is None:
                self.current_piece, self.current_color = self.new_piece()
                self.current_x = GRID_WIDTH // 2 - len(self.current_piece[0]) // 2
                self.current_y = 0
                self.hold_used = False
                if self.collision():
                    self.play_sound("game_over.wav")
                    self.game_over = True
            else:
                self.current_piece, self.current_color = self.hold_piece_old
            self.hold_used = True

    def play_sound(self, file):
        full_path = os.path.abspath(file)
        sound = pygame.mixer.Sound(full_path)
        sound.play()

    def play_background_music(self, file):
        def music_thread():
            full_path = os.path.abspath(file)
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play(-1)  # Play the music indefinitely
        threading.Thread(target=music_thread, daemon=True).start()

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")
            self.update()

    def quit_game(self):
        self.window.destroy()

    def exit_fullscreen(self, event):
        self.window.attributes('-fullscreen', False)

if __name__ == "__main__":
    Tetris()
