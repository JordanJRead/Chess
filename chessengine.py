# TODO make sure that the king does not pass through check to castle. Maybe use the checking_for_check argument in pmoves
# to do different stuff?? although that checks the other colour's moves, not yours
# new idea, make a second temp board to check checks for that the king in the inbetween position
from math import *
from copy import deepcopy
import pieces

def square_to_rank(square):
    return ceil(square / 8)

def square_to_file(square):
    return (square - 1) % 8 + 1

def find_closest(list, num):
    # Find the closest value in a list to a number
    small_distance = abs(num - list[0])
    close_number = list[0]
    for i in range(len(list)):
        if i > 0: # Not first iteration
            distance = abs(list[i] - num)
            if distance < small_distance:
                small_distance = distance
                close_number = list[i]
    return close_number

class GameState:
    def __init__(self, anarchy = False):
        self.anarchy = anarchy
        self.turn = "w"
        self.not_turn = "b"
        self.white_en = 100
        self.black_en = 100
        self.fiftyrule = 0
        self.white_can_castle_short = True
        self.white_can_castle_long = True
        self.black_can_castle_short = True
        self.black_can_castle_long = True
        self.board = {
            57: "bR", 58: "bN", 59: "bB", 60: "bQ", 61: "bK", 62: "bB", 63: "bN", 64: "bR",
            49: "bP", 50: "bP", 51: "bP", 52: "bP", 53: "bP", 54: "bP", 55: "bP", 56: "bP",
            41: "--", 42: "--", 43: "--", 44: "--", 45: "--", 46: "--", 47: "--", 48: "--",
            33: "--", 34: "--", 35: "--", 36: "--", 37: "--", 38: "--", 39: "--", 40: "--",
            25: "--", 26: "--", 27: "--", 28: "--", 29: "--", 30: "--", 31: "--", 32: "--",
            17: "--", 18: "--", 19: "--", 20: "--", 21: "--", 22: "--", 23: "--", 24: "--",
             9: "wP", 10: "wP", 11: "wP", 12: "wP", 13: "wP", 14: "wP", 15: "wP", 16: "wP",
             1: "wR",  2: "wN",  3: "wB",  4: "wQ",  5: "wK",  6: "wB",  7: "wN",  8: "wR",
        }

        b = self.board
        self.clean_board = ""
        for i in range(len(self.board)): # Makes a board that can be printed and read easily
            rank_top = ceil((i+1)/8)
            square = 64 - rank_top*8 + i%8 + 1
            self.clean_board += b[square]
            if (i+1) % 8 == 0:
                self.clean_board += "\n"
            else:
                self.clean_board += ","

    def make_clean_board(self):
        b = self.board
        self.clean_board = ""
        for i in range(len(self.board)):
            rank_top = ceil((i+1)/8)
            square = 64 - rank_top*8 + i%8 + 1
            self.clean_board += b[square]
            if (i+1) % 8 == 0:
                self.clean_board += "\n"
            else:
                self.clean_board += ","

    # Returns a list of valid moves given a square. The p in pmoves signifies that the moves did not check if they put the player in check, which will be dealt with later
    def find_pmoves(self, square, board = None, checking_for_check = False):
        if board == None: # Sets the default board to be the gamestate board (you can't reference self in arguments)
            board = self.board
        
        # Variables for future use
        rank = square_to_rank(square)
        file = square_to_file(square)
        distance_to_top = 8 - square_to_rank(square)
        distance_to_bottom = square_to_rank(square) - 1
        distance_to_left = file - 1
        distance_to_right = 8 - file

        valid_pmoves = []
        colour = board[square][0]

        if colour == "w":
            not_colour = "b"
        else:
            not_colour = "w"
        
        match board[square][1]: # Match case for piece type
            case "P": # Untested
                for i in pieces.pawn_move(self, square, board):
                    valid_pmoves.append(i)
            case "R":
                for i in pieces.rook_move(self, square, board):
                    valid_pmoves.append(i)
            case "N":
                for i in pieces.knight_move(self, square, board):
                    valid_pmoves.append(i)
            case "K": # Untested
                for i in pieces.king_move(self, square, board, checking_for_check):
                    valid_pmoves.append(i)
            case "B":
                for i in pieces.bishop_move(self, square, board):
                    valid_pmoves.append(i)
            case "Q": # FIXME there is a problem with the queen around the top right?
                for i in pieces.bishop_move(self, square, board):
                    valid_pmoves.append(i)
                for i in pieces.rook_move(self, square, board):
                    valid_pmoves.append(i)
            case "Ñ": # Untested
                for i in pieces.knight_move(self, square, board):
                    valid_pmoves.append(i)
                for i in pieces.rook_move(self, square, board):
                    valid_pmoves.append(i)             
        return valid_pmoves

    def make_temp_board(self, square, destination):
        # Make a copy of the game board with one piece having moved
        temp_board = deepcopy(self.board)
        temp_board[destination] = temp_board[square]
        temp_board[square] = "--"
        if temp_board[square][1] == "K":
            if abs(square - destination) == 2: # If castling
                # Move the rook
                rook_to_move = find_closest([1, 8, 57, 64], square)
                temp_board[rook_to_move] = "--"
                if rook_to_move in [1, 57]: # a file rook
                    temp_board[rook_to_move + 3]
                else:
                    temp_board[rook_to_move - 2]
                
        return temp_board
        # I will iterate through a list of pmoves, and put all those boards into a check finder that uses find_pmoves
    
    def is_in_check(self, colour, board = None):
        if board == None:
            board = self.board
        valid_pmoves = []
        match colour:
            case "w":
                not_colour = "b"
            case "b":
                not_colour = "w"
        keys = list(board.keys())
        vals = list(board.values())
        pos = vals.index(colour + "K")
        king_square = keys[pos]
        
        # Loop through the board and put all the enemy's pieces through find_pmoves and check against colour's king's position
        for i in board:
            if board[i][0] == not_colour: # Enemy piece found
                for y in self.find_pmoves(i, board, True):
                    valid_pmoves.append(y)
        return king_square in valid_pmoves
            # return king in valid_pmoves
    
    def find_moves(self, square):
        colour = self.board[square][0]
        valid_moves = []
        valid_pmoves = self.find_pmoves(square)

        # Go through the valid moves that the piece can make, then see if it puts you in check
        if valid_pmoves is not None: # If you have moves
            for i in valid_pmoves: # Check to see if they put you in check
                temp_board = self.make_temp_board(square, i) # Make a temporary board where you made that move
                if not self.is_in_check(colour, temp_board):
                    if self.board[square][1] == "K" and abs(i - square) == 2: # If the move being checking is a castle

                        if i < square: # Figure out the king's inbetween square
                            value = -1
                        else:
                            value = 1

                        temp_board = self.make_temp_board(square, square + (value)) # Makes a temp board where the king
                                                                                    # is in the middle of castling
                        if not self.is_in_check(colour, temp_board): # If you are not in check while moving to castle
                            valid_moves.append(i)
                    else:
                        valid_moves.append(i)
            return valid_moves
    
    def move(self, square, destination):
        colour = self.board[square][0]
        # If pawn is moving 2 (en passant)
        if self.board[square][1] == "P" and (destination == square + 16 or destination == square - 16):
            if self.board[square][0] == "w":
                self.white_en = square + 8
            else:
                self.black_en = square - 8
        # Take out the piece that got en passanted
        if self.board[square] == "wP" and destination == self.black_en:
            self.board[self.black_en - 8] = "--"
        elif self.board[square] == "bP" and destination == self.white_en:
            self.board[self.white_en + 8] = "--"

        # Castling rights
        match self.board[square][0]:
                case "w":
                    if self.board[square][1] == "K":
                        self.white_can_castle_long = False
                        self.white_can_castle_short = False
                    if square == 1: # White's a rook
                        self.white_can_castle_long = False
                    elif square == 8: # White's h rook
                        self.white_can_castle_short = False
                case "b":
                    if self.board[square][1] == "K":
                        self.black_can_castle_long = False
                        self.black_can_castle_short = False
                    if square == 57: # Black's a rook
                        self.black_can_castle_long = False
                    elif square == 64: # Black's h rook
                        self.black_can_castle_short = False

        # Move the castling rook
        if self.board[square][1] == "K":
            if abs(square - destination) == 2: # If castling
                # Move the rook
                rook_to_move = find_closest([1, 8, 57, 64], destination)
                self.board[rook_to_move] = "--"
                rook_code = colour + "R"
                if rook_to_move in [1, 57]:
                    self.board[rook_to_move + 3] = rook_code
                else:
                    self.board[rook_to_move - 2] = rook_code
        if self.board[square][1] == "P" or self.board[destination] != "--":
            self.fiftyrule = 0
        else:
            self.fiftyrule += 1

        # Anarchy
        if self.anarchy:
            if self.board[destination] == colour + "R":
                self.board[square] = colour + "Ñ" # Turns the piece you are moving into a knook so that it can take your rook
                
        # Move the piece
        self.board[destination] = self.board[square]
        self.board[square] = "--"
        self.make_clean_board()

    def promote(self, square, piece):
        self.board[square] = self.board[square][0] + piece

    def end_turn(self):
        if self.turn == "w":
            
            self.turn = "b"
            self.not_turn = "w"
            self.black_en = 100
        else:
            self.turn = "w"
            self.not_turn = "b"
            self.white_en = 100
    
    def check_end_condition(self, colour): # Checks if colour lost / stalemated
        in_check = self.is_in_check(colour)

        # Checks if colour has moves
        valid_moves = []
        for i in self.board:
            if self.board[i][0] == colour: # For each of colour's pieces
                for y in self.find_moves(i):
                    valid_moves.append(y) # Add each valid move to this list
        has_moves = bool(valid_moves)
                
        ### Checkmate
        if in_check and not has_moves:
            return "checkmate"
        ### Stalemate
        if not in_check and not has_moves:
            return "stalemate"
        
        ### Insufficient material
        pieces = []
        for i in self.board:
            if self.board[i] != "--":
                pieces.append(self.board[i]) # Puts all the piece codes (wK) from the board into a list
        # King v King
        if len(pieces) == 2:
            return "insufficient material"
        
        w_pieces = []
        b_pieces = []

        ### King / King + B or N
        if len(pieces) <= 4:
            for i in pieces: # Sort pieces by colour
                if i[0] == "w":
                    w_pieces.append(pieces[i])
                else:
                    b_pieces.append(pieces[i])
            if len(w_pieces) == 1 and len(b_pieces) == 2: # 1 vs 2 w/b
                for i in b_pieces:
                    if i == "bN" or i == "bB": # W king vs black king + B xor N
                        return "insufficient material"
            if len(b_pieces) == 1 and len(w_pieces) == 2: # 2 vs 1 w/b
                for i in w_pieces:
                    if i == "wN" or i == "wB": # B king vs white king + B xor N
                        return "insufficient material"
            # King + minor vs same
            if len(w_pieces) == 2 and len(w_pieces) == b_pieces: # If each colour has 2 pieces
                for i in w_pieces:
                    if i == "wN" or i == "wB":
                        for y in b_pieces:
                            if y == "bN" or y == "bB":
                                return "insufficient material"
            # King + 2 knights vs king
            if len(w_pieces) == 3: # 3w vs 1b
                w_knights = 0
                for i in w_pieces:
                    if i == "wN":
                        w_knights += 1
                if w_knights == 2:
                    return "insufficient material"

                    
                    # Allow either player to claim a draw if no capture has been made or no pawn has been moved in the last 50 moves. 
        if self.fiftyrule >= 100:
            return "50 move rule"

        return "not over"