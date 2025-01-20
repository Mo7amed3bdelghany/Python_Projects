import pygame
import sys
import pyttsx3

# Initialize pygame
pygame.init()

# Screen dimensions and constants
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS # SQUARE_SIZE = 75

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)
DARK_BROWN = (181, 136, 99) 
HIGHLIGHT_COLOR = (186, 202, 68)  # Color for highlighting available moves
SELECTED_COLOR = (255, 0, 0)  # color for capture piece

# Load Chess pieces
PIECES = {
    "w_king": pygame.image.load("Media/white_king.png"),
    "b_king": pygame.image.load("Media/black_king.png"),
    "b_queen": pygame.image.load("Media/black_queen.png"),
    "w_queen": pygame.image.load("Media/white_queen.png"),
    "b_rook": pygame.image.load("Media/black_rook.png"),
    "w_rook": pygame.image.load("Media/white_rook.png"),
    "b_knight": pygame.image.load("Media/black_knight.png"),
    "w_knight": pygame.image.load("Media/white_knight.png"),
    "w_bishop": pygame.image.load("Media/white_bishop.png"),
    "b_bishop": pygame.image.load("Media/black_bishop.png"),
    "w_pawn": pygame.image.load("Media/white_pawn.png"),
    "b_pawn": pygame.image.load("Media/black_pawn.png")
}

# Resize images to fit squares 
for key in PIECES:
    PIECES[key] = pygame.transform.scale(PIECES[key], (SQUARE_SIZE, SQUARE_SIZE))

# Load move sound
MOVE_SOUND = pygame.mixer.Sound("Media/move.wav")

# Load Background music
sound = pygame.mixer.Sound("Media/music-for-game.mp3")

def GameOver(who):
    engine = pyttsx3.init()
    engine.say("Game  Over " + who)
    engine.runAndWait() 

# Chessboard starting position
STARTING_POSITION = [
    ["b_rook", "b_knight", "b_bishop", "b_queen", "b_king", "b_bishop", "b_knight", "b_rook"],
    ["b_pawn"] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    ["w_pawn"] * 8,
    ["w_rook", "w_knight", "w_bishop", "w_queen", "w_king", "w_bishop", "w_knight", "w_rook"],
]

# Function to show splash screen
def show_splash_screen(screen):
    splash_image = pygame.image.load("Media/Splash_Screen.jpg")  # Load your splash image
    splash_image = pygame.transform.scale(splash_image, (WIDTH, HEIGHT))  # Scale it to fit the screen
    screen.blit(splash_image, (0, 0))
    pygame.display.flip() 
    pygame.time.delay(2000)  # Show for 5 seconds
    
# Function to show the main menu
def show_main_menu(screen):
    font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 50)
    start_button = button_font.render(' START PLAYER VS PLAYER ', True, WHITE)
    exit_button = button_font.render(' EXIT GAME. ', True, WHITE)

    # Frame properties
    start_color = (0, 128, 0)  # Green for Start button
    exit_color = (128, 0, 0)   # Red for Exit button
    frame_padding = 10

    # Calculate button positions
    start_button_x = (WIDTH // 2 - start_button.get_width() // 2)
    start_button_y = HEIGHT // 2
    exit_button_x = WIDTH // 2 - exit_button.get_width() // 2
    exit_button_y = HEIGHT // 2 + start_button.get_height() + 40  # Add space between buttons

    # Load background image
    background_image = pygame.image.load('Media/Chess_Board.jpg') 
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))  # Scale to fit the screen

    while True:
        # Start music
        sound.play()

        # Blit the background image
        screen.blit(background_image, (0, 0))
        
        text = font.render("Chess Game", True, BLACK)
        textrect = text.get_rect()
        textrect.center = (WIDTH // 2, HEIGHT // 3)
        screen.blit(text, textrect)

        # Draw frames around the buttons
        pygame.draw.rect(screen, start_color, (start_button_x - frame_padding, start_button_y - frame_padding, start_button.get_width() + frame_padding * 2, start_button.get_height() + frame_padding * 2))
        pygame.draw.rect(screen, exit_color, (exit_button_x - frame_padding, exit_button_y - frame_padding, exit_button.get_width() + frame_padding * 2, exit_button.get_height() + frame_padding * 2))

        # Blit buttons onto the screen
        screen.blit(start_button, (start_button_x, start_button_y))
        screen.blit(exit_button, (exit_button_x, exit_button_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Stop music
                sound.stop()

                x, y = event.pos
                # Check if Start button was clicked
                if start_button_x <= x <= start_button_x + start_button.get_width() and \
                start_button_y <= y <= start_button_y + start_button.get_height():
                    return  # Start the game
                # Check if Exit button was clicked
                if exit_button_x <= x <= exit_button_x + exit_button.get_width() and \
                exit_button_y <= y <= exit_button_y + exit_button.get_height():
                    pygame.quit()
                    sys.exit()

# Draw the chessboard
def draw_board(screen, valid_moves, capture_moves):
    for row in range(ROWS):
        for col in range(COLS):
            if (row, col) in valid_moves:
                pygame.draw.circle(screen, (0, 200, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 6)
            else:
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            # Draw a rectangle around capturable pieces
            if (row, col) in capture_moves:
                pygame.draw.rect(screen, SELECTED_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces on the board
def draw_pieces(screen, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece: 
                screen.blit(PIECES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Validate moves for all pieces
def is_valid_move(piece, start, end, board):
    piece_type = piece[2:]  # "pawn",  "rook"
    piece_color = piece[0]  # "w" or "b"
    start_row, start_col = start
    end_row, end_col = end
    
    # Prevent capturing own pieces
    if board[end_row][end_col] and board[end_row][end_col][0] == piece_color:
        return False

    if piece_type == "pawn":
        direction = -1 if piece_color == "w" else 1
        if start_col == end_col:  # Forward move
            if board[end_row][end_col] is None:
                if end_row == start_row + direction:
                    return True
                # Check for two-square move
                if end_row == start_row + 2 * direction and (start_row == 6 if piece_color == "w" else start_row == 1):
                    # Check both squares in front of the pawn
                    if board[start_row + direction][start_col] is None and board[end_row][end_col] is None:
                        return True
        elif abs(start_col - end_col) == 1 and end_row == start_row + direction:  # Capture move
            if board[end_row][end_col]:
                return True
            
    elif piece_type == "rook":
        if start_row == end_row or start_col == end_col:  # Horizontal or vertical
            step_row = (end_row - start_row) // max(1, abs(end_row - start_row)) if start_row != end_row else 0
            step_col = (end_col - start_col) // max(1, abs(end_col - start_col)) if start_col != end_col else 0

            current_row, current_col = start_row + step_row, start_col + step_col
            while (current_row, current_col) != (end_row, end_col):
                if board[current_row][current_col]:
                    return False
                current_row += step_row
                current_col += step_col
            return True
    elif piece_type == "knight":
        if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
            return True
    elif piece_type == "bishop":
        if abs(start_row - end_row) == abs(start_col - end_col):  # Diagonal
            step_row = (end_row - start_row) // abs(end_row - start_row)
            step_col = (end_col - start_col) // abs(end_col - start_col)

            current_row, current_col = start_row + step_row, start_col + step_col
            while (current_row, current_col) != (end_row, end_col):
                if board[current_row][current_col]:
                    return False
                current_row += step_row
                current_col += step_col
            return True
    elif piece_type == "queen":
        # Combines rook and bishop movement
        return is_valid_move(piece_color + "_rook", start, end, board) or is_valid_move(piece_color + "_bishop", start, end, board)
    elif piece_type == "king":
        if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
            return True

    return False

# Get all valid moves for a selected piece
def get_valid_moves(piece, start, board):
    valid_moves = []
    capture_moves = [] 
    for row in range(ROWS):
        for col in range(COLS):
            if is_valid_move(piece, start, (row, col), board):
                valid_moves.append((row, col))
                if board[row][col] and board[row][col][0] != piece[0]:  # Check if it's a capturable piece
                    capture_moves.append((row, col))
    return valid_moves, capture_moves


# End the game when the king is captured
def check_for_king_capture(board):
    white_king_present = any("w_king" in row for row in board)
    black_king_present = any("b_king" in row for row in board)

    if not white_king_present:
        print("Black wins! White's king has been captured.\n")
        GameOver("White")
        pygame.quit()
        sys.exit()
    if not black_king_present:
        print("White wins! Black's king has been captured.\n")
        GameOver("Black")
        pygame.quit()
        sys.exit()
        


def main():
    # Window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    # The name of window
    pygame.display.set_caption("Chess Game")

    # Show splash screen
    show_splash_screen(screen)
    
    # Show main menu
    show_main_menu(screen)

    # Game setup
    board = [row[:] for row in STARTING_POSITION]
    """
    board=[]
    for row in STARTING_POEITION:
        board.append(row[:])
    """
    
    selected_piece = None
    valid_moves = []
    capture_moves = []
    
    running = True
    turn = "w"  # "w" for white, "b" for black

    while running:
        draw_board(screen, valid_moves, capture_moves)
        draw_pieces(screen, board)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                
                if selected_piece:
                    if is_valid_move(selected_piece[0], (selected_piece[1], selected_piece[2]), (row, col), board):
                        board[selected_piece[1]][selected_piece[2]] = None
                        board[row][col] = selected_piece[0]
                        MOVE_SOUND.play()  # Play the sound effect
                        turn = "b" if turn == "w" else "w"  # Switch turn
                        check_for_king_capture(board)  # Check after every move
                    selected_piece = None
                    valid_moves = []
                    capture_moves = []
                else:
                    if board[row][col] and board[row][col][0] == turn:
                        selected_piece = (board[row][col], row, col)
                        valid_moves, capture_moves = get_valid_moves(selected_piece[0], (row, col), board)

# Run the game
if __name__ == "__main__":
    main()