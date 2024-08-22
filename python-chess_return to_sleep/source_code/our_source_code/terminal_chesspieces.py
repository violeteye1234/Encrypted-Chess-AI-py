class Pawn:

    def is_valid_move(board,from_row, from_col, to_row, to_col, color,opponent_pawn_double_move):
        # Check if pawn can move two spaces on their forst moves
        if (color == 1 and from_row == 1) or (color == -1 and from_row == 6):
            if 2 * abs(color) >= abs(to_row - from_row) > 1 and to_col == from_col and board[to_row][to_col] == " ":
                return True, True
            elif 2 * abs(color) >= abs(to_row - from_row) > 0 and to_col == from_col and board[to_row][to_col] == " ":
                return True,False
            else:
                return False,False
        # Check if pawn can move one space
        elif color==-1 and 1 * color <= (to_row - from_row) <  0 and to_col == from_col and board[to_row][to_col] == " ":
            return True,False
        elif color==1 and 1 * color >= (to_row - from_row) >  0 and to_col == from_col and board[to_row][to_col] == " ":
            return True,False
        else:
            return False,False
        
    def promote_pawn(to_row, color):
        # Check if pawn is in promote postion and proceed pawn promoation.
        while True:
            if (color == 1 and to_row == 7):
                promotion_selection=input("Please select your promotion pieces:(Q,R,B,N)")
                if promotion_selection == "Q":
                    return promotion_selection
                elif promotion_selection == "R":
                    return promotion_selection
                elif promotion_selection == "B":
                    return promotion_selection
                elif promotion_selection == "N":
                    return promotion_selection
                else:
                    print("Invalid input, Try again!")
            elif (color == -1 and to_row == 0):
                promotion_selection=input("Please select your promotion pieces:(q,r,b,n)")
                if promotion_selection == "q":
                    return promotion_selection
                elif promotion_selection == "r":
                    return promotion_selection
                elif promotion_selection == "b":
                    return promotion_selection
                elif promotion_selection == "n":
                    return promotion_selection
                else:
                    print("Invalid input, Try again!")
            else:
                return

    def en_passant(board,color,from_row,from_col,to_row,to_col):
        #Check if the moves is entitled for en passent moves and return values accordingly

        #Check if both pawn is in correct postions for en passant
        if color==1:
            if board[3][to_col+1] =="p":
                en_passant_to_row=2
                en_passant_to_col=to_col
                captured_pawn_row=3
                captured_pawn_col=to_col+1
                
            elif board[3][to_col-1] == "p":
                en_passant_to_row=2
                en_passant_to_col=to_col
                captured_pawn_row=3
                captured_pawn_col=to_col-1
                
            else:
                return False,None,None,None,None,None,None,None

        elif color==-1:
            if board[4][to_col+1] =="P":
                en_passant_to_row=5
                en_passant_to_col=to_col
                captured_pawn_row=4
                captured_pawn_col=to_col+1
                
            elif board[4][to_col-1] == "P":
                en_passant_to_row=5
                en_passant_to_col=to_col
                captured_pawn_row=4
                captured_pawn_col=to_col-1
                
            else:
                return False,None,None,None,None,None,None,None
        while True:
            #If the en passant is avaiable , ask players to proceeds en passant or not.
            if en_passant_to_row is not None:
                proceed_en_passant=input("Your opponent is entitled for En passant, do your opponent want to proceed?(Y/N)")
                if proceed_en_passant == "Y" or proceed_en_passant == "y":
                    if en_passant_to_row==2 :
                        #Create En passant pisces
                        en_passant_pawn="p"
                        #Update chess board with en passant move
                        board[captured_pawn_row][captured_pawn_col]=" "
                        board[en_passant_to_row][en_passant_to_col]=en_passant_pawn
                        board[from_row][from_col]=" "
                        board[to_row][to_col]=" "


                    else : 
                        #Create En passant pisces
                        en_passant_pawn="P"
                        #Update chess board with en passant move
                        board[captured_pawn_row][captured_pawn_col]=" "
                        board[en_passant_to_row][en_passant_to_col]=en_passant_pawn
                        board[from_row][from_col]=" "
                        board[to_row][to_col]=" "
                    #Create en passan move history
                    #Move History
                    en_passant_move=chr(captured_pawn_col + 97), int(captured_pawn_row) + 1," ",chr(en_passant_to_col + 97), int(en_passant_to_row) + 1
                    en_passant_move=''.join(str(element) for element in en_passant_move)

                    #Return board and en passant move history to chess engine

                    return True,board,en_passant_move,en_passant_pawn,captured_pawn_row,captured_pawn_col,en_passant_to_row,en_passant_to_col

                # Return None if the players choose not to procees en passant
                elif proceed_en_passant == "N" or proceed_en_passant == "n":
                    return False,None,None,None,None,None,None,None
                
                else :
                    print("Invalid input, Try again!")

    #Check if the pawn moves is a killing moves.
    def pawn_killing(board,color,from_row,from_col,to_row,to_col):
        if color == 1:
            if to_row-from_row==1 and abs(to_col-from_col) == 1 and board[to_row][to_col].islower() == True:
                return True
        else:
            if to_row-from_row==-1 and abs(to_col-from_col) == 1 and board[to_row][to_col].isupper() == True:
                return True
            return False
        

class Rook:
    # Method to check if a rook move is valid
    def is_valid_move(board, from_row, from_col, to_row, to_col):
        # Check if the move is along a row or a column
        if from_row == to_row or from_col == to_col:
            # Check if there are any pieces in between the start and end squares
            if from_row == to_row:
                # Moving along a row
                for col in range(min(from_col, to_col) + 1, max(from_col, to_col)):
                    if board[from_row][col] != " ":
                        return False
            else:
                # Moving along a column
                for row in range(min(from_row, to_row) + 1, max(from_row, to_row)):
                    if board[row][from_col] != " ":
                        return False
            return True
        else:
            return False

        
class Bishop: 
    # Method to check if a bishop move is valid
    def is_valid_move(board, from_row, from_col, to_row, to_col):
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)

        if row_diff != col_diff:
            # The move is not diagonal
            return False
        
        if from_row == to_row or from_col == to_col:
            # The bishop is not actually moving
            return False

        # Check for obstructions between the starting and ending squares
        row_dir = 1 if to_row > from_row else -1
        col_dir = 1 if to_col > from_col else -1
        
        row, col = from_row + row_dir, from_col + col_dir
        while row != to_row and col != to_col:
            if board[row][col] != " ":
                # There is a piece blocking the bishop's path
                return False
            row += row_dir
            col += col_dir
        
        # The move is valid if there are no obstructions
        return True


class Knight: 
    # Method to check if a knight move is valid
    def is_valid_move(from_row, from_col, to_row, to_col):
        if (abs(from_row - to_row) == 2 and abs(from_col - to_col) == 1) or (abs(from_row - to_row) == 1 and abs(from_col - to_col) == 2):
            return True
        else:
            return False

class Queen: 
    # Method to check if a queen move is valid
    def is_valid_move(board, from_row, from_col, to_row, to_col):
        # Check if the move is a valid rook move or bishop move
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        if abs(from_row - to_row) != 0 and abs(from_col - to_col) == 0:
            # Vertical move 
            step = 1 if to_row > from_row else -1
            for r in range(from_row + step, to_row, step):
                if board[r][from_col] != " ":
                    return False
            return True
        elif abs(from_col - to_col) != 0 and abs(from_row - to_row) == 0:
            # Horizontal move 
            step = 1 if to_col > from_col else -1
            for c in range(from_col + step, to_col, step):
                if board[from_row][c] != " ":
                    return False
            return True
        elif row_diff == col_diff and from_row != to_row and from_col != to_col and row_diff != 0:
            # Diagonal move 
            step_row = 1 if to_row > from_row else -1
            step_col = 1 if to_col > from_col else -1
            r, c = from_row + step_row, from_col + step_col
            while r != to_row and c != to_col:
                if board[r][c] != " ":
                    return False
                r += step_row
                c += step_col
            return True
        else:
            return False


class King: 
    # Method to check if a king move is valid
    def is_valid_move(from_row, from_col, to_row, to_col):
        row_diff = abs(from_row - to_row)
        col_diff = abs(from_col - to_col)
        if row_diff <= 1 and col_diff <= 1 and (row_diff + col_diff) > 0:
            return True
        else:
            return False
    # Check if the King moves is castling    
    def is_castling(board,move_history_raw,color,to_row, to_col):
        found_k=False
        found_r=False
        if color==1:
            #Check if king or rook moved before, procees if move history returns False.
            for item in move_history_raw:
                if item[0] == "K":
                    found_k = True
                elif item[0] == "R":
                    found_r = True
          
            if found_r ==False or found_k ==False :
                if to_row == 0 and to_col == 6:
                    board[0][5]="R"
                    board[0][7]=" "
                    castling_rook_move="R","h1 f1"
                    castling_rook_move_raw="R",0,7,0,5
                    return True,board,castling_rook_move,castling_rook_move_raw
                elif to_row == 0 and to_col == 2:
                    board[0][3]="R"
                    board[0][0]=" "
                    castling_rook_move="R","a1 d1"
                    castling_rook_move_raw="R",0,0,0,3
                    return True,board,castling_rook_move,castling_rook_move_raw
                else:
                    return False,None,None,None
            

        else :
            for item in move_history_raw:
                if item[0] == "k":
                    found_k = True
                elif item[0] == "r":
                    found_r = True
            
            if found_r ==False or found_k ==False :
                if to_row == 0 and to_col == 6:
                    board[7][5]="r"
                    board[7][7]=" "
                    castling_rook_move="r","h8 f8"
                    castling_rook_move_raw="r",7,7,7,5
                    return True,board,castling_rook_move,castling_rook_move_raw
                elif to_row == 0 and to_col == 2:
                    board[7][3]="r"
                    board[7][7]=" "
                    castling_rook_move="r","a8 d8"
                    castling_rook_move_raw="r",7,0,7,3
                    return True,board,castling_rook_move,castling_rook_move_raw
                else:
                    return False,None,None,None
