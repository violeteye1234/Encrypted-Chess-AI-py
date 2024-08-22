from terminal_chesspieces import *
from terminal_special_moves import * 
import re
import chess

class ChessGame:
    def __init__(self):
        # Initialize the chess board, player White pieces is in uppercase, Black is in lowercase
        self.board = [
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "n", "b", "q", "k", "b", "n", "r"]
        ]

        # Initialize the game state
        self.current_player = "Black"
        self.win = False

        # Initialize the move history stack
        self.move_history_raw = []
        self.move_history = []
        self.captured_pieces = []
        self.raw_captured_pieces = []

        # Initialize the boolean objects
        self.opponent_pawn_double_move = False

        self.last_move_is_castling = False

        self.last_move_is_en_passant = False

        #Print board with guidance
    def print_board(self):
        for i, row in enumerate(self.board):
            print(f"{1+i} {row}")
        print("    a ,  b ,  c ,  d ,  e ,  f ,  g ,  h  ")

        #Check the board state with stalemate or checkmate 
    def checkwins(self):
        #new board object for chess library
        new_board = chess.Board()
        #Convert the 2d aray board to chess library board object
        for row in range(8):
            for col in range(8):
                piece = new_board.piece_type_at(chess.square(col, row))
                if piece is not None:
                    new_board.remove_piece_at(chess.square(col, row))
                if self.board[row][col] == " ":
                    continue
                if self.board[row][col].islower():
                    color = chess.WHITE
                else:
                    color = chess.BLACK
                piece = None
                if self.board[row][col].lower() == "p":
                    piece = chess.PAWN
                elif self.board[row][col].lower() == "r":
                    piece = chess.ROOK
                elif self.board[row][col].lower() == "n":
                    piece = chess.KNIGHT
                elif self.board[row][col].lower() == "b":
                    piece = chess.BISHOP
                elif self.board[row][col].lower() == "q":
                    piece = chess.QUEEN
                elif self.board[row][col].lower() == "k":
                    piece = chess.KING
                new_board.set_piece_at(chess.square(col, row), chess.Piece(piece, color))
        new_board=new_board.mirror()

        checkmate=new_board.is_checkmate()
        stalemate=new_board.is_stalemate()

        if checkmate:
            result = new_board.result()
            if result == "1-0":
                print("White wins by checkmate!")
                self.win=True
            elif result == "0-1":
                print("Black wins by checkmate!")
                self.win=True

        if stalemate:
            result = new_board.result()
            if result == "1-0":
                print("White wins by stalemate!")
                self.win=True
            elif result == "0-1":
                print("Black wins by stalemate!")
                self.win=True
        return checkmate,stalemate

        #Check moves is valid or not
    def move_piece(self, piece, from_row, from_col, to_row, to_col,move_input):
        # Determine the color of the piece
        color = 1 if piece.isupper() else -1

        
        # Check if the pawn move is valid
        if piece == "P" or piece == "p":
            #Check is it a pawn killing moves
            pawn_killing = Pawn.pawn_killing(self.board,color,from_row,from_col,to_row,to_col)
            if pawn_killing :
                self.board[from_row][from_col]=" "
                captured=self.board[to_row][to_col]
                self.board[to_row][to_col]="P" if color ==1 else "p"
                self.move_history.append((piece, move_input))
                self.move_history_raw.append((piece, from_row, from_col, to_row, to_col))
                self.captured_pieces.append(captured)
                self.raw_captured_pieces.append((captured,to_row,to_col))
                #Check if the pawn is entitled for pawn promotion after killing
                pawn_promotion = Pawn.promote_pawn(to_row,  color)
                if pawn_promotion is not None:
                    self.board[from_row][from_col] = " "
                    self.board[to_row][to_col] = pawn_promotion
                    return True
                return True

             # Check if the pawn move is valid
            move_check,self.opponent_pawn_double_move = Pawn.is_valid_move(self.board,from_row, from_col, to_row, to_col, color,self.opponent_pawn_double_move)
            #If the pawn move is valid, check if it is entitled for en_passant
            if move_check:
                if self.opponent_pawn_double_move==True:
                    if len(self.move_history_raw) > 0:                       
                        do_en_passant,board,en_passant_move,en_passant_pawn,captured_pawn_row,captured_pawn_col,en_passant_to_row,en_passant_to_col= Pawn.en_passant(self.board,color,from_row,from_col,to_row,to_col)
                        if do_en_passant :
                            self.board=board
                            self.current_player = "Black" if self.current_player == "White" else "White"
                            #Add killed pawn move
                            self.move_history.append((piece, move_input))
                            self.move_history_raw.append((piece, from_row, from_col, to_row, to_col))
                            #Add en passant move
                            self.move_history.append((en_passant_pawn,en_passant_move))
                            self.move_history_raw.append((en_passant_pawn,captured_pawn_row,captured_pawn_col,en_passant_to_row,en_passant_to_col))
                            self.last_move_is_en_passant=True 
                            self.captured_pieces.append(piece)
                            self.raw_captured_pieces.append((piece,to_row,to_col))
                            self.captured_pieces.append(None)
                            self.raw_captured_pieces.append(None)
                            return True
                          
                pawn_promotion = Pawn.promote_pawn(to_row,  color)
                #If the pawn is entitled for pawn promotion, promote_pawn will return user's selected pieces for promotion
                if pawn_promotion is not None:
                    self.board[from_row][from_col] = " "
                    self.board[to_row][to_col] = pawn_promotion
                    self.move_history.append((piece, move_input))
                    self.move_history_raw.append((piece, from_row, from_col, to_row, to_col))
                    self.captured_pieces.append(None)
                    self.raw_captured_pieces.append(None)
                    return True
                                            
        elif piece == "R" or piece == "r":
            # Check if the Rook move is valid
            move_check = Rook.is_valid_move(self.board,from_row, from_col, to_row, to_col)
        elif piece == "N" or piece == "n":
            # Check if the Knight move is valid
            move_check = Knight.is_valid_move(from_row, from_col, to_row, to_col)
        elif piece == "B" or piece == "b":
            # Check if the Bishop move is valid
            move_check = Bishop.is_valid_move(self.board,from_row, from_col, to_row, to_col)
        elif piece == "Q" or piece == "q":
            # Check if the Queen move is valid
            move_check = Queen.is_valid_move(self.board,from_row, from_col, to_row, to_col)
        elif piece == "K" or piece == "k":
            # Check if the king move is castling
            is_castling_boolean,board,castling_rook_move,castling_rook_move_raw=King.is_castling(self.board,self.move_history_raw,color,to_row, to_col)
            if is_castling_boolean == True:
                self.board=board
                self.move_history.append((castling_rook_move))
                self.move_history_raw.append((castling_rook_move_raw))
                self.board[to_row][to_col] = piece
                self.board[from_row][from_col] = " "
                self.move_history.append((piece, move_input))
                self.move_history_raw.append((piece, from_row, from_col, to_row, to_col))
                self.last_move_is_castling== True 
                self.captured_pieces.append(None)
                self.raw_captured_pieces.append(None)
                self.captured_pieces.append(None)
                self.raw_captured_pieces.append(None)
                return True,self.last_move_is_castling
            
            else:
                # Check if the King move is valid
                move_check = King.is_valid_move(from_row, from_col, to_row, to_col)
        else:
            return False
    
        if move_check:
            #Check if capture avaiable for Black 
            if self.board[to_row][to_col]!= " " :
                if self.board[from_row][from_col].isupper() and color == -1 :
                    captured_pieces=self.board[to_row][to_col]
                    self.captured_pieces.append(captured_pieces)
                    self.raw_captured_pieces.append(captured_pieces,[to_row],[to_col])
                    self.board[to_row][to_col] = piece
                    self.board[from_row][from_col] = " "
                    self.move_history.append((piece, move_input))
                    self.move_history_raw.append((piece, from_row, from_col, to_row, to_col))

                #Check if capture avaiable for White
                    return True,self.move_history,self.move_history_raw
                elif self.board[from_row][from_col].islower() and color == 1 :
                    captured_pieces=self.board[to_row][to_col]
                    self.captured_pieces.append(captured_pieces)
                    self.raw_captured_pieces.append(captured_pieces)
                    self.board[to_row][to_col] = piece
                    self.board[from_row][from_col] = " "
                    self.move_history.append((piece, move_input))
                    self.move_history_raw.append((piece, from_row, from_col, to_row, to_col))


                    return True
                else:
                    return False

            # Move the piece if move validation returns True
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = " "
            self.move_history.append((piece, move_input))
            self.move_history_raw.append((piece, from_row, from_col, to_row, to_col))
            self.captured_pieces.append(None)
            self.raw_captured_pieces.append(None)

            return True
        else:
            return False

    def undo_last_move(self):
        # Check if there are any moves in the move history stack
        if len(self.move_history) == 0:
            print("No moves to undo.")
            return False
        #Check if the last move is castling and do a double undo
        elif self.last_move_is_castling == True:
            last_move = self.move_history_raw.pop()
            self.move_history.pop()
            piece, from_row, from_col, to_row, to_col = last_move
            self.board[from_row][from_col] = piece
            self.board[to_row][to_col] = " "
            last_move = self.move_history_raw.pop()
            self.move_history.pop()
            piece, from_row, from_col, to_row, to_col = last_move
            self.board[from_row][from_col] = piece
            self.board[to_row][to_col] = " "
            self.current_player = "Black" if self.current_player == "White" else "White"
            self.captured_pieces.pop()
            self.raw_captured_pieces.pop()
            self.captured_pieces.pop()
            self.raw_captured_pieces.pop()
            return True
        #Check if the last move is en passant and do a double undo
        elif self.last_move_is_en_passant == True:
            last_move = self.move_history_raw.pop()
            self.move_history.pop()
            piece, from_row, from_col, to_row, to_col = last_move
            self.board[from_row][from_col] = piece
            self.board[to_row][to_col] = " "
            last_move = self.move_history_raw.pop()
            self.move_history.pop()
            piece, from_row, from_col, to_row, to_col = last_move
            self.board[from_row][from_col] = piece
            self.board[to_row][to_col] = " "
            self.captured_pieces.pop()
            self.raw_captured_pieces.pop()
            self.captured_pieces.pop()
            self.raw_captured_pieces.pop()
            return True
        
        else:


            # Get the last move if it is not castling and en passent ,and get the last capture from the move history stack and pop the last moves out of the stack
            last_move = self.move_history_raw.pop()
            self.move_history.pop()
            last_capture=self.raw_captured_pieces.pop()
            self.captured_pieces.pop()
            # Get the piece and position information from the last move
            piece, from_row, from_col, to_row, to_col = last_move
        
            # Move the piece back to its original position
            self.board[from_row][from_col] = piece
            self.board[to_row][to_col] = " "
           #Check is last move contains a capture,if captured data is not None, then proceed to undo the capture
            if last_capture is not None:

                captured_piece,captured_row,captured_col = last_capture
                self.board[captured_row][captured_col]=captured_piece
            # Switch the current player
            self.current_player = "Black" if self.current_player == "White" else "White"

            return True


    def play_game(self):

        while not self.win:
            # Get the user input for the move
            # Print the initial state of the board
            self.print_board()
            checkmate,stalemate=self.checkwins()
            print("Checkmate? "+str(checkmate))
            print("Stalemate? "+str(stalemate))
            # Print the move history and captured pieces for each round
            print("Moves history:"+str(self.move_history))
            print('Captured pieces:'+str(self.captured_pieces))
            move_input = input("Player "+ self.current_player +", Please Enter your move (e.g. 'e7 e5') or type \"undo\" if your opponents want to undo their last moves: ")

            # Check if the users input is in correct range and format
            if re.match('[a-h][1-8] [a-h][1-8]',move_input) or move_input=="undo":
                pass
            else :
                print("Invalid input. Try again.")
                continue
            # Check if users input is undo and call the undo function
            if move_input == "undo":
                # Undo the last move
                self.undo_last_move()
            else:
                #Formatting the users input into correct attributes.
                from_pos, to_pos = move_input.split()
                from_col, from_row = ord(from_pos[0]) - ord('a'), int(from_pos[1]) - 1
                to_col, to_row = ord(to_pos[0]) - ord('a'), int(to_pos[1]) - 1

                # Get the piece at the starting position
                piece = self.board[from_row][from_col]

                # Check if the piece belongs to the current player
                if (self.current_player == "White" and piece.isupper()) or \
                (self.current_player == "Black" and piece.islower()):

                    # Move the piece and switch the current player
                    if self.move_piece(piece, from_row, from_col, to_row, to_col,move_input):
                        self.current_player = "Black" if self.current_player == "White" else "White"
                        
                    else:
                        #Print error message when the moves is not valid.
                        print("Invalid move. Try again.")

                else:
                    #Print error message of palyers selected opponents pieces
                    print("Invalid piece. Try again.")


        print("Game over.")
        
if __name__ == "__main__":
    game=ChessGame()
    game.play_game()
