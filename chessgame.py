# TODO End condition images on the king (#, 1/2) - Checkmate square isnt showing the black, maybe make it a png? or figure out why
import chessengine
from math import *

# Pygame
import pygame
dimensions = 800
square_size = dimensions / 8
image_scale_size = square_size + 1
pygame.init()
screen = pygame.display.set_mode((dimensions, dimensions))
game = chessengine.GameState()

def draw_valid_square(square):
    coords = square_to_xy(square)
    screen.blit(valid_move_image, coords)
    pygame.display.update()

def draw_board():
    screen.blit(board_image, (0, 0))
    for i in game.board:
        if game.board[i][0] == "w":
            if game.board[i][1] == "P":
                screen.blit(wP_image, (square_to_xy(i)))
            if game.board[i][1] == "R":
                screen.blit(wR_image, (square_to_xy(i)))
            if game.board[i][1] == "N":
                screen.blit(wN_image, (square_to_xy(i)))
            if game.board[i][1] == "B":
                screen.blit(wB_image, (square_to_xy(i)))
            if game.board[i][1] == "Q":
                screen.blit(wQ_image, (square_to_xy(i)))
            if game.board[i][1] == "K":
                screen.blit(wK_image, (square_to_xy(i)))
            if game.board[i][1] == "Ñ":
                screen.blit(wÑ_image, (square_to_xy(i)))

        elif game.board[i][0] == "b":
            if game.board[i][1] == "P":
                screen.blit(bP_image, (square_to_xy(i)))
            if game.board[i][1] == "R":
                screen.blit(bR_image, (square_to_xy(i)))
            if game.board[i][1] == "N":
                screen.blit(bN_image, (square_to_xy(i)))
            if game.board[i][1] == "B":
                screen.blit(bB_image, (square_to_xy(i)))
            if game.board[i][1] == "Q":
                screen.blit(bQ_image, (square_to_xy(i)))
            if game.board[i][1] == "K":
                screen.blit(bK_image, (square_to_xy(i)))
    pygame.display.update()

# These convert between a square's number and its top left coordinates
def xy_to_square(x, y):
    x_axis = ceil((x+1)/square_size)
    rank = 9-ceil((y+1)/square_size)
    return (rank-1) * 8 + x_axis

def square_to_xy(square):
    x_axis = (((square-1)%8)+1)
    rank = ceil(square / 8)
    x = (x_axis - 1) * square_size
    y = (8 - rank) * square_size
    return [x,y]

# Brings up a menu to choose what to promote a piece to - queen, rook, bishop, knight, knook in the future
def promote_select():
    colour = game.turn
    screen.blit(valid_move_image, (square_to_xy(36)))
    screen.blit(valid_move_image, (square_to_xy(37)))
    screen.blit(valid_move_image, (square_to_xy(28)))
    screen.blit(valid_move_image, (square_to_xy(29)))
    if colour == "w":
        screen.blit(wQ_image, (square_to_xy(36)))
        screen.blit(wR_image, (square_to_xy(37)))
        screen.blit(wB_image, (square_to_xy(28)))
        screen.blit(wN_image, (square_to_xy(29)))
    else:
        screen.blit(bQ_image, (square_to_xy(36)))
        screen.blit(bR_image, (square_to_xy(37)))
        screen.blit(bB_image, (square_to_xy(28)))
        screen.blit(bN_image, (square_to_xy(29)))
   
    pygame.display.update()
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
                pygame.quit()
            # Selecting a square
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get what square the mouse clicked on
                selected_square = xy_to_square(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
               
                if selected_square == 36:
                    return "Q"
                elif selected_square == 37:
                    return "R"
                elif selected_square == 28:
                    return "B"
                elif selected_square == 29:
                    return "N"

valid_move_image = pygame.transform.scale(pygame.image.load("data/valid_move.png"), (image_scale_size, image_scale_size))
valid_move_image.set_alpha(100)
board_image = pygame.transform.scale(pygame.image.load("data/chess_board.png"), (dimensions, dimensions))
checkmate_image = pygame.transform.scale(pygame.image.load("data/checkmate_square.svg"), (image_scale_size, image_scale_size))
#checkmate_image.set_alpha(255)

wP_image = pygame.transform.scale(pygame.image.load("data/white_pawn.svg"), (image_scale_size, image_scale_size))
wR_image = pygame.transform.scale(pygame.image.load("data/white_rook.svg"), (image_scale_size, image_scale_size))
wN_image = pygame.transform.scale(pygame.image.load("data/white_knight.svg"), (image_scale_size, image_scale_size))
wB_image = pygame.transform.scale(pygame.image.load("data/white_bishop.svg"), (image_scale_size, image_scale_size))
wQ_image = pygame.transform.scale(pygame.image.load("data/white_queen.svg"), (image_scale_size, image_scale_size))
wÑ_image = pygame.transform.scale(pygame.image.load("pieces_vector/white_knook_better.xcf"), (image_scale_size, image_scale_size))
wRight_image = pygame.transform.scale(pygame.image.load("pieces_vector/white_right.xcf"), (image_scale_size, image_scale_size))

wK_image = pygame.transform.scale(pygame.image.load("data/white_king.svg"), (image_scale_size, image_scale_size))
bP_image = pygame.transform.scale(pygame.image.load("data/black_pawn.svg"), (image_scale_size, image_scale_size))
bR_image = pygame.transform.scale(pygame.image.load("data/black_rook.svg"), (image_scale_size, image_scale_size))
bN_image = pygame.transform.scale(pygame.image.load("data/black_knight.svg"), (image_scale_size, image_scale_size))
bB_image = pygame.transform.scale(pygame.image.load("data/black_bishop.svg"), (image_scale_size, image_scale_size))
bQ_image = pygame.transform.scale(pygame.image.load("data/black_queen.svg"), (image_scale_size, image_scale_size))

wR_image_alpha = pygame.transform.scale(pygame.image.load("data/white_rook.svg"), (image_scale_size, image_scale_size))
wR_image_alpha.set_alpha(100)
wN_image_alpha = pygame.transform.scale(pygame.image.load("data/white_knight.svg"), (image_scale_size, image_scale_size))
wN_image_alpha.set_alpha(100)
wB_image_alpha = pygame.transform.scale(pygame.image.load("data/white_bishop.svg"), (image_scale_size, image_scale_size))
wB_image_alpha.set_alpha(100)
wQ_image_alpha = pygame.transform.scale(pygame.image.load("data/white_queen.svg"), (image_scale_size, image_scale_size))
wQ_image_alpha.set_alpha(100)

bR_image_alpha = pygame.transform.scale(pygame.image.load("data/black_rook.svg"), (image_scale_size, image_scale_size))
bR_image_alpha.set_alpha(100)
bN_image_alpha = pygame.transform.scale(pygame.image.load("data/black_knight.svg"), (image_scale_size, image_scale_size))
bN_image_alpha.set_alpha(100)
bB_image_alpha = pygame.transform.scale(pygame.image.load("data/black_bishop.svg"), (image_scale_size, image_scale_size))
bB_image_alpha.set_alpha(100)
bQ_image_alpha = pygame.transform.scale(pygame.image.load("data/black_queen.svg"), (image_scale_size, image_scale_size))

bQ_image_alpha.set_alpha(100)
bK_image = pygame.transform.scale(pygame.image.load("data/black_king.svg"), (image_scale_size, image_scale_size))

game_on = True
selected_a_piece = False
draw_board()
valid_moves = []
while game_on: # Game loop
   
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
        # Selecting a square
        if event.type == pygame.MOUSEBUTTONDOWN:
           
            # Get what square the mouse clicked on
            selected_square = xy_to_square(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            if game.board[selected_square][0] == game.turn and selected_square not in valid_moves: # Clicking on a valid square would just move there
                selected_piece = selected_square
                selected_a_piece = True
                valid_moves = game.find_moves(selected_piece)
                draw_board()
                if bool(valid_moves):
                    for i in valid_moves:
                        draw_valid_square(i)

            elif selected_a_piece: # Move the piece
                if selected_square in valid_moves:
                    destination = selected_square
                    game.move(selected_piece, destination)

                    # Promoting
                    if game.board[destination][1] == "P" and ((game.board[destination][0] == "w" and destination > 56) or (game.board[destination][0] == "b" and destination < 9)): # Promote a pawn
                        promote_to = promote_select()
                        game.promote(destination, promote_to)

                    game.end_turn()
                    valid_moves = []
                    selected_a_piece = False
                    draw_board()
                    print(game.check_end_condition(game.turn))

                    # Mate
                    if game.check_end_condition(game.turn) == "checkmate":
                        keys = list(game.board.keys())
                        vals = list(game.board.values())
                        pos = vals.index(game.turn + "K")
                        king_square = keys[pos]
                        game.board[king_square] = "--"
                        screen.blit(checkmate_image, square_to_xy(king_square))
                        valid_moves = []
                        pygame.display.update()
                   
                    # Stalemate
                   
pygame.quit()