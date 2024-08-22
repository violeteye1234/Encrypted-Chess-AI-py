""" 
The provided code consists of several functions that check for different types of moves in a game of chess:

1. castle: checks if the move is a castle and executes it if it is.
2. en_passant: checks if the move is an en passant capture and removes the captured pawn if it is.
3. kill_piece: checks if the move is a capture and removes the captured piece if it is.
4. promote_pawn: checks if the move is a pawn promotion and promotes the pawn if it is.
5. is_stalemate: checks if the game is in stalemate.
6. Checkmate: check if the king is in checkmate.
7. Special moves script: makes sure all the following above connects and flows on conditions.

The code has been compiled into a single script called special moves. 
The make_move function takes in the board, from_square, to_square, and an optional promotion_piece argument. 
It then checks if the move is a castle, en passant capture, capture, pawn promotion, or a regular move, and 
returns a string indicating the type of move that was made.

However, there may be room for improvement depending on the specific 
needs of the project it is being used for. 
For example, additional error handling could be added to handle unexpected input values. 
Additionally, the make_move function could be expanded to handle other types of special moves, 
such as pawn double moves or checking for checkmate.
"""

def castle(board, from_square, to_square):
    # Check if the move is a castle
    if board.is_castling(chess.Move(from_square, to_square)):
        # Move the king
        board.set_piece_at(to_square, board.piece_at(from_square))
        board.remove_piece_at(from_square)

        # Move the rook
        if to_square == chess.G1:
            board.set_piece_at(chess.F1, board.piece_at(chess.H1))
            board.remove_piece_at(chess.H1)
        else:
            board.set_piece_at(chess.F8, board.piece_at(chess.H8))
            board.remove_piece_at(chess.H8)

        return True
    else:
        return False

def en_passant(board, from_square, to_square):
    # Check if the move is an en passant capture
    if board.is_en_passant(chess.Move(from_square, to_square)):
        # Remove the captured pawn
        if board.turn == chess.WHITE:
            captured_pawn_square = chess.square(to_square % 8, to_square // 8 - 1)
        else:
            captured_pawn_square = chess.square(to_square % 8, to_square // 8 + 1)

        captured_pawn = board.remove_piece_at(captured_pawn_square)
        return captured_pawn
    else:
        return None
        
def kill_piece(board, from_square, to_square):
    # Check if the move is a capture
    if board.is_capture(chess.Move(from_square, to_square)):
        # Remove the captured piece from the board
        captured_piece = board.remove_piece_at(to_square)
        return captured_piece
    else:
        return None

def promote_pawn(board, from_square, to_square, promotion_piece):
    # Check if the move is a pawn promotion
    if board.piece_at(from_square).piece_type == chess.PAWN and \
            (chess.rank(to_square) == chess.RANK_1 or chess.rank(to_square) == chess.RANK_8):
        # Remove the pawn from the from_square
        board.remove_piece_at(from_square)
        # Add the promoted piece to the to_square
        board.set_piece_at(to_square, promotion_piece)
        return True
    else:
        return False

def is_stalemate(board):
    # Check if the king is not in check
    if not board.is_check():
        # Generate all possible moves for the player
        moves = list(board.legal_moves)
        # Check if there are any legal moves
        if len(moves) == 0:
            # If there are no legal moves, it's stalemate
            return True
    # If the king is in check, it's not stalemate
    return False

def is_checkmate(board):
    # Check if the king is in checkmate
    if board.is_checkmate():
        return True
    else:
        return False

# Special moves script
def make_move(board, from_square, to_square, promotion_piece=None):
    # Check if the move is a castle
    if castle(board, from_square, to_square):
        return "castle"

    # Check if the move is an en passant capture
    captured_pawn = en_passant(board, from_square, to_square)
    if captured_pawn is not None:
        return "en passant"
        
    # Check if the move is a capture
    captured_piece = kill_piece(board, from_square, to_square)
    if captured_piece is not None:
        return "capture"

    # Check if the move is a pawn promotion
    if promotion_piece is not None and promote_pawn(board, from_square, to_square, promotion_piece):
        return "promotion"

    # Check if the move is a double pawn move
    if double_pawn:
        if board.piece_at(from_square).piece_type == chess.PAWN and \
                (chess.rank(to_square) == chess.RANK_3 or chess.rank(to_square) == chess.RANK_6):
            # Move the pawn two squares forward
            board.set_piece_at(to_square, board,piece_at(from_square))
            board.remove_piece_at(from_square)
            return "double pawn"
        else:
            return "invalid move"

    # Check for checkmate
    if is_checkmate(board):
        return "checkmate"
    
    # If none of the above conditions are met, it's a regular move
    # Check if the move is legal
    if chess.Move(from_square, to_square) in board.legal_moves:
        board.push(chess.Move(from_square, to_square))
        return "regular"
    else:
        return

# Personal notes and back-up concept below
"""
To connect the chesspieces code with the special_moves script, you can modify the is_valid_move function in 
each of the Pawn, Rook, Bishop, Knight, Queen, and King classes to take in the board argument in addition to the from_row, 
from_col, to_row, to_col, and color arguments. 
The board argument should be a 2D array representing the current state of the chess board.
"""

# Here is an example modification of the Pawn class to take in the board argument:
"""
class Pawn:
    def is_valid_move(from_row, from_col, to_row, to_col, color, board):
        # set direction based on color
        if (color == 1 and from_row == 1) or (color == -1 and from_row == 6):
            if 2 * abs(color) >= abs(to_row - from_row) > 0 and to_col == from_col and board[to_row][to_col] is None:
                return True
            else:
                return False
        # Check if pawn can move one space
        elif 1 * abs(color) >= abs(to_row - from_row) > 0 and to_col == from_col and board[to_row][to_col] is None:
            return True
        else:
            return False
# you would need to similarly modify the is_valid_move function in the other classes to take in the board argument.

# Once you have modified the is_valid_move functions, you can use them in the make_move function of the special_moves 
# script to check if a move is legal before executing it. For example, you could modify the promote_pawn function to use the 
# is_valid_move function of the Pawn class to check if a pawn promotion move is legal:

def promote_pawn(board, from_square, to_square, promotion_piece):
    from_row, from_col = square_to_row_col(from_square)
    to_row, to_col = square_to_row_col(to_square)

    # Check if move is legal
    if Pawn.is_valid_move(from_row, from_col, to_row, to_col, board[from_row][from_col].color, board):
        # Execute move
        board[from_row][from_col] = None
        board[to_row][to_col] = promotion_piece
        return "promotion"
    else:
        return "invalid move"
# You would need to similarly modify the other functions in the special_moves script to use the appropriate is_valid_move function for each piece type. 
"""