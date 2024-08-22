"""
Holds the code for the different bots(Easy, Medium and Difficult)
"""
import random
"""
These are a set of scores for different chess pieces and their positions on the chess board.
The piece_score dictionary gives the score for each type of piece.
The king is worth 0 points because it needs to survive throughtout game. If you lose the king, you lose the game.It needs to be protected rather than attack.
The knight_scores, bishop_scores, rook_scores, queen_scores, and pawn_scores lists give a score for each square on the chess board for each type of piece.


"""

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}

CHECKMATE = 1000
stale_mate = 0
DEPTH = 3

# Finds the best move for the AI. The function takes in the current game state, a list of valid moves, and a return queue. 
# The best move is put into the return queue.
def find_best_move(game_state, valid_moves, return_queue):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.white_to_move else -1)
    return_queue.put(next_move)


# It evaluates the game state by recursively searching the possible moves and scores them. 
# The function takes in the current game state, a list of valid moves, the depth of the search, alpha and beta values for alpha-beta pruning(concept adapted from Eddie Sharick), 
# and a turn multiplier to keep track of whose turn it is.
def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.get_valid_moves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score



#This function scores the board. A positive score is good for white, a negative score is good for black.
#It assigns a score to each piece on the board based on the piece type and its position on the board. The function returns the total score for the game state.
def scoreBoard(game_state):

    if game_state.check_mate:
        if game_state.white_to_move:
            return -CHECKMATE  # Black wins
        else:
            return CHECKMATE  # White wins
    elif game_state.stale_mate:
        return stale_mate
    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score

    return score



#Picks and returns a random valid move for the difficult bot which is embedded in the main code.
def findRandomMove(valid_moves):
    return random.choice(valid_moves)


#Class for the random bot
class RandomBot:
    #The function the random bot uses to find a move. It only choose a random legal move on the board. There is no strategy behind the moves
    def select_move(self, game_state):
        valid_moves = game_state.get_valid_moves()
        return random.choice(valid_moves)
    

#Class for the Medium bot        
class MinimaxBot:
    def __init__(self, depth):
        self.depth = depth
    
    #This function takes in a game_state object and returns the best move according to the minimax algorithm
    def select_move(self, game_state):
        valid_moves = game_state.get_valid_moves()
        best_move = None
        best_score = -CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            score = self.minimax(game_state, self.depth, False)
            game_state.undoMove()
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
    
    
    #This function The minimax function is the implementation of the minimax algorithm with alpha-beta pruning(Adapted from Eddie Sharick). 
    #It evaluates the game state by recursively searching the possible moves and scores them. 
    def minimax(self, game_state, depth, maximizing_player):
        if depth == 0 or game_state.check_mate or game_state.stale_mate:
            return scoreBoard(game_state)
        
        if maximizing_player:
            max_score = -CHECKMATE
            valid_moves = game_state.get_valid_moves()
            for move in valid_moves:
                game_state.makeMove(move)
                score = self.minimax(game_state, depth-1, False)
                game_state.undoMove()
                max_score = max(max_score, score)
            return max_score
        else:
            min_score = CHECKMATE
            valid_moves = game_state.get_valid_moves()
            for move in valid_moves:
                game_state.makeMove(move)
                score = self.minimax(game_state, depth-1, True)
                game_state.undoMove()
                min_score = min(min_score, score)
            return min_score
