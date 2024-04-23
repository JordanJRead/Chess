import chessengine as ce
from math import *

def rook_move(self, square, board):
    rank = ce.square_to_rank(square)
    file = ce.square_to_file(square)
    distance_to_top = 8 - ce.square_to_rank(square)
    distance_to_bottom = ce.square_to_rank(square) - 1
    distance_to_left = file - 1
    distance_to_right = 8 - file

    valid_pmoves = []
    colour = board[square][0]

    if colour == "w":
        not_colour = "b"
    else:
        not_colour = "w"

    # Rook move up
    if distance_to_top > 0:
        for i in range(1, distance_to_top + 1):

            if board[square + i * 8] == "--":
                valid_pmoves.append(square + i * 8)
                

            elif board[square + i * 8][0] == not_colour:
                valid_pmoves.append(square + i * 8)
                break
            else:
                break
    
    # Rook move down
    
    if distance_to_bottom > 0:
        for i in range(1, distance_to_bottom + 1):

            if board[square - i * 8] == "--":
                valid_pmoves.append(square - i * 8)
            
            elif board[square - i * 8][0] == not_colour:
                valid_pmoves.append(square - i * 8)
                break
            else:
                break
    
    # Rook move left
    if distance_to_left > 0:
        for i in range(1, distance_to_left + 1):
            if board[square - i] == "--": # Moving to empty square
                valid_pmoves.append(square - i)
            elif board[square - i][0] == not_colour: # Taking a piece stops you from going past the piece
                valid_pmoves.append(square - i)
                break
            else: # Does not let you take or go past your own colour piece
                break
    
    # Rook move right
    if distance_to_right > 0:
        for i in range(1, distance_to_right + 1):
            if board[square + i] == "--":
                valid_pmoves.append(square + i)
            elif board[square + i][0] == not_colour:
                valid_pmoves.append(square + i)
                break
            else:
                break
    return valid_pmoves


### KNIGHT MOVES
def knight_move(self, square, board):
    

    rank = ce.square_to_rank(square)
    file = ce.square_to_file(square)
    distance_to_top = 8 - ce.square_to_rank(square)
    distance_to_bottom = ce.square_to_rank(square) - 1
    distance_to_left = file - 1
    distance_to_right = 8 - file

    valid_pmoves = []
    colour = board[square][0]

    if colour == "w":
        not_colour = "b"
    else:
        not_colour = "w"
    ### Knight movement

    # Right right: file <= 6
    # Right: file <= 7
    # Left left: file >= 3
    # Left: file >= 2

    # Up up: rank <= 6
    # Up: rank <= 7
    # Down down: rank <= 3
    # Down: rank <= 2
    # Knight up up right
    if file <= 7 and rank <= 6:
        if board[square + 17][0] != colour or (self.anarchy and board[square + 17][1] == "R" and board[square][1] == "N"):
            valid_pmoves.append(square + 17)
    # Knight up right right
    if file <=6 and rank <= 7:
        if board[square + 10][0] != colour or (self.anarchy and board[square + 10][1] == "R"and board[square][1] == "N"):
            valid_pmoves.append(square + 10)
    # Knight down right right
    if file <= 6 and rank >= 2:
        if board[square - 6][0] != colour or (self.anarchy and board[square - 6][1] == "R"and board[square][1] == "N"):
            valid_pmoves.append(square - 6)
    # Knight down down right
    if file <= 7 and rank >= 3:
        if board[square - 15][0] != colour or (self.anarchy and board[square - 15][1] == "R"and board[square][1] == "N"):
            valid_pmoves.append(square - 15)
    # Knight up up left
    if file >= 2 and rank <= 6:
        if board[square + 15][0] != colour or (self.anarchy and board[square + 15][1] == "R" and board[square][1] == "N"):
            valid_pmoves.append(square + 15)
    # Knight up left left
    if file >= 3 and rank <= 7:
        if board[square + 6][0] != colour or (self.anarchy and board[square + 6][1] == "R"and board[square][1] == "N"):
            valid_pmoves.append(square + 6)
    # Knight down left left
    if file >= 3 and rank >= 2:
        if board[square - 10][0] != colour or (self.anarchy and board[square - 10][1] == "R"and board[square][1] == "N"):
            valid_pmoves.append(square - 10)
    # Knight down down left
    if file >= 2 and rank >= 3:
        if board[square - 17][0] != colour or (self.anarchy and board[square - 17][1] == "R"and board[square][1] == "N"):
            valid_pmoves.append(square - 17)
    return valid_pmoves


### BISHOP MOVES
def bishop_move(self, square, board):

    rank = ce.square_to_rank(square)
    file = ce.square_to_file(square)
    distance_to_top = 8 - ce.square_to_rank(square)
    distance_to_bottom = ce.square_to_rank(square) - 1
    distance_to_left = file - 1
    distance_to_right = 8 - file

    valid_pmoves = []
    colour = board[square][0]

    if colour == "w":
        not_colour = "b"
    else:
        not_colour = "w"

    ### BISHOP MOVEMENT
    for i in range(4): # Each i value corrosponds with the 4 bishop directions
        match i:
            case 0: # 0 = Up right
                diagonal_info = [distance_to_top, distance_to_right, 9]
            case 1: # 1 = Up left
                diagonal_info = [distance_to_top, distance_to_left, 7]
            case 2: # Down right
                diagonal_info = [distance_to_bottom, distance_to_right, -7]
            case 3: # Down left
                diagonal_info = [distance_to_bottom, distance_to_left, -9]
        distance_1 = diagonal_info[0]
        distance_2 = diagonal_info[1]
        square_add = diagonal_info[2]

        for y in range(min(distance_1, distance_2)): # "Formula" for finding bishop moves from the above variables
            iteration = y + 1
            if board[square + (square_add * iteration)][0] == colour:
                break
            elif board[square + (square_add * iteration)][0] == not_colour:
                valid_pmoves.append(square + (square_add * iteration))
                break
            else:
                valid_pmoves.append(square + (square_add * iteration))
    return valid_pmoves

def king_move(self, square, board, checking_for_check):

    rank = ce.square_to_rank(square)
    file = ce.square_to_file(square)
    distance_to_top = 8 - ce.square_to_rank(square)
    distance_to_bottom = ce.square_to_rank(square) - 1
    distance_to_left = file - 1
    distance_to_right = 8 - file

    valid_pmoves = []
    colour = board[square][0]

    if colour == "w":
        not_colour = "b"
    else:
        not_colour = "w"

    ### KING MOVEMENT
    # Up
    if rank < 8:
        # Up left
        if file > 1:
            if board[square + 7][0] != colour:
                valid_pmoves.append(square + 7)
        # Up
        if board[square + 8][0] != colour:
            valid_pmoves.append(square + 8)
        # Up right
        if file < 8:
            if board[square + 9][0] != colour:
                valid_pmoves.append(square + 9)
    # Down
    if rank > 1:
        # Down left
        if file > 1:
            if board[square - 9][0] != colour:
                valid_pmoves.append(square - 9)
        # Down
        if board[square - 8][0] != colour:
            valid_pmoves.append(square - 8)
        # Down right
        if file < 8:
            if board[square - 7][0] != colour:
                valid_pmoves.append(square - 7)
    # Left
    if file > 1:
        if board[square - 1][0] != colour:
            valid_pmoves.append(square - 1)
    # Right
    if file < 8:
        if board[square + 1][0] != colour:
            valid_pmoves.append(square + 1)
    ### Castling
    if not checking_for_check:
        match colour:
            case "w":
                if not self.is_in_check("w"):
                    if self.white_can_castle_long and (board[2] + board[3] + board[4] == "------"):
                        valid_pmoves.append(3)
                    if self.white_can_castle_short and (board[6] + board[7] == "----"):
                        valid_pmoves.append(7)
            case "b":
                if not self.is_in_check("b"):
                    if self.black_can_castle_long and (board[58] + board[59] + board[60] == "------"):
                        valid_pmoves.append(59)
                    if self.black_can_castle_short and (board[62] + board[63] == "----"):
                        valid_pmoves.append(63)
    return valid_pmoves

def pawn_move(self, square, board):

    rank = ce.square_to_rank(square)
    file = ce.square_to_file(square)
    distance_to_top = 8 - ce.square_to_rank(square)
    distance_to_bottom = ce.square_to_rank(square) - 1
    distance_to_left = file - 1
    distance_to_right = 8 - file

    valid_pmoves = []
    colour = board[square][0]

    if colour == "w":
        not_colour = "b"
    else:
        not_colour = "w"

    ### PAWN MOVEMENT
    if board[square][0] == "w":
        # If pawn can go ahead
            if square + 8 <= 64:
                if board[square + 8] == "--":
                    valid_pmoves.append(square + 8)
                    # If pawn can go 2 ahead
                    if square + 16 <= 64:
                        if board[square + 16] == "--" and rank == 2:
                            valid_pmoves.append(square + 16)
            # If pawn can take on right
            if square + 9 <= 64:
                if (board[square + 9][0] == "b" or square + 9 == self.black_en) and ceil((square + 9) / 8) - 1 == rank:
                    valid_pmoves.append(square + 9)
            # If pawn can take on left
            if square + 7 <= 64:
                if (board[square + 7][0] == "b" or square + 7 == self.black_en) and ceil((square + 7) / 8) > rank:
                    valid_pmoves.append(square + 7)
    else: # Black pawn
        # If pawn can go ahead
            if square - 8 > 0:
                if board[square - 8] == "--":
                    valid_pmoves.append(square - 8)
                    # If pawn can go 2 ahead
                    if square - 16 > 0:
                        if board[square - 16] == "--" and rank == 7:
                            valid_pmoves.append(square - 16)
            # If pawn can take on right
            if square - 7 > 0:
                if (board[square - 7][0] == "w" or square - 7 == self.white_en) and ceil((square - 7) / 8) < rank:
                    valid_pmoves.append(square - 7)
            # If pawn can take on left
            if square - 9 > 0:
                if (board[square - 9][0] == "w" or square - 9 == self.white_en) and ceil((square - 9) / 8) + 1 == rank:
                    valid_pmoves.append(square - 9)
    return valid_pmoves

def right_move(self, square, board):

    rank = ce.square_to_rank(square)
    file = ce.square_to_file(square)
    distance_to_top = 8 - ce.square_to_rank(square)
    distance_to_bottom = ce.square_to_rank(square) - 1
    distance_to_left = file - 1
    distance_to_right = 8 - file

    valid_pmoves = []
    colour = board[square][0]

    if colour == "w":
        not_colour = "b"
    else:
        not_colour = "w"
    
    if distance_to_right > 0:
        for i in range(1, distance_to_right + 1):
            if board[square + i] == "--":
                valid_pmoves.append(square + i)
            elif board[square + i][0] == not_colour:
                valid_pmoves.append(square + i)
                break
            else:
                break
    return valid_pmoves