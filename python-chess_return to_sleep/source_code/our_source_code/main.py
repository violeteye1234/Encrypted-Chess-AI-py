"""
Main driver file.
Handling user input.
Displaying current GameStatus object.
"""
import pygame 
import engine, bots, skeleton
import sys
from multiprocessing import Process, Queue

width = height = 512
WIDTH = 250
HEIGHT = height
dimension = 8
sq_size = height // dimension
fps = 15
IMAGES = {}

pygame.display.set_caption("Chess")

#Loads Images
def load_images():
    """
    Initialize a global directory of images.
    """

    #Loading Pictures
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(piece + ".png"), (sq_size, sq_size))



def main_difficultai(player_one, player_two, name_up, name_down):
    """
    Difficult Bot
    This will handle user input and update the graphics.
    """
    pygame.init()
    screen = pygame.display.set_mode((width + WIDTH, height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    game_state = engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    load_images()  # do this only once before while loop
    running = True
    sq_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = pygame.font.SysFont("Times New Roman", 14, False, False)
    bold_font = pygame.font.SysFont("Times New Roman", 14, True, False)
    """
    player_one = True  # if a human is playing white, then this will be True, else False
    player_two = False  # if a human is playing white, then this will be True, else False
    """
    white = True
    black = False    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    timer = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    whiteSecs = blackSecs = 0
    delta_time = 0


    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        if human_turn:
            white = True
            black = False
        else:
            white = False
            black = True
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    location = pygame.mouse.get_pos()  #  location of the mouse
                    col = location[0] // sq_size
                    row = location[1] // sq_size
                    if sq_selected == (row, col) or col >= 8:  # user clicked the same square twice
                        sq_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                sq_selected = ()  # reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]

            # key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:  # undo when 'z' is pressed
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == pygame.K_r:  # reset the game when 'r' is pressed
                    game_state = engine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == pygame.K_q: #Quit when 'q' is pressed
                    pygame.quit()
                    sys.exit()
        
        #add the time elapsed last frame to correct player 
        if white:
            whiteSecs += delta_time
        else:
            blackSecs += delta_time

        # Divide by 60 to get total minutes
        minsW = whiteSecs // 60
        # Use the remainders to get the secoonds
        secW = round(whiteSecs % 60)
        # Divide by 60 to get total minutes
        minB = blackSecs // 60
        # Use the remainders to get the secoonds
        secB = round(blackSecs % 60)

        #format the lead 0s
        whiteTime = "Time: {0:02}:{1:02}".format(minsW, secW)
        # Blit timer to the screen
        whiteTimer = font.render(whiteTime, True, BLACK)
        screen.blit(whiteTimer, [590, 425])
        #format the lead 0s
        blackTime = "Time: {0:02}:{1:02}".format(minB, secB)
        # Blit timer to the screen
        blackTimer = font.render(blackTime, True, BLACK)
        screen.blit(blackTimer, [590, 80])
        pygame.display.flip()
        #get the time elapsed since the last call in milliseconds, '/1000' to get seconds
        delta_time = timer.tick(60) / 1000

        # AI move finder
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()  # used to pass data between threads
                move_finder_process = Process(target= bots.find_best_move, args=(game_state, valid_moves, return_queue))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = return_queue.get()
                if ai_move is None:
                    ai_move = bots.findRandomMove(valid_moves)
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        #Animation
        if move_made:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, sq_selected)

        if not game_over:
            draw_name_top(name_up, screen, bold_font)
            draw_name_bottom(name_down,screen, bold_font)
            drawMoveLog(screen, game_state, move_log_font)


            

        if game_state.check_mate:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stale_mate:
            game_over = True
            drawEndGameText(screen, "stalemate")

        clock.tick(fps)
    
    #Updating Screen
    pygame.display.flip()
    pygame.display.update()



def drawGameState(screen, game_state, valid_moves, sq_selected):
    """
    Responsible for all the graphics within current game state.
    """
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, game_state, valid_moves, sq_selected)
    drawPieces(screen, game_state.board)  # draw pieces on top of those squares


def drawBoard(screen):
    """
    Draw the squares on the board.
    The top left square is always light.
    """
    global colors
    colors = [pygame.Color((125,56,24)), pygame.Color((234, 221, 202))]
    for row in range(dimension):
        for column in range(dimension):
            color = colors[((row + column) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(column * sq_size, row * sq_size, sq_size, sq_size))


def highlightSquares(screen, game_state, valid_moves, sq_selected):
    """
    Highlight square selected and moves for piece selected.
    """
    if (len(game_state.move_log)) > 0:
        last_move = game_state.move_log[-1]
        s = pygame.Surface((sq_size, sq_size))
        s.set_alpha(100)
        s.fill(pygame.Color('red'))
        screen.blit(s, (last_move.end_col * sq_size, last_move.end_row * sq_size))
    if sq_selected != ():
        row, col = sq_selected
        if game_state.board[row][col][0] == (
                'w' if game_state.white_to_move else 'b'):  # sq_selected is a piece that can be moved
            # highlight selected square
            s = pygame.Surface((sq_size, sq_size))
            s.set_alpha(100)  # transparency value 0 -> transparent, 255 -> opaque
            s.fill(pygame.Color((15, 148, 4)))
            screen.blit(s, (col * sq_size, row * sq_size))
            # highlight moves from that square
            s.fill(pygame.Color('yellow'))
            for move in valid_moves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (move.end_col * sq_size, move.end_row * sq_size))


def drawPieces(screen, board):
    """
    Draw the pieces on the board using the current game_state.board
    """
    for row in range(dimension):
        for column in range(dimension):
            piece = board[row][column]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(column * sq_size, row * sq_size, sq_size, sq_size))


def drawMoveLog(screen, game_state, font):
    """
    Draws the move log.

    """
    move_log_rect = pygame.Rect(width, 100, WIDTH, HEIGHT-200)
    pygame.draw.rect(screen, pygame.Color((234, 221, 202)), move_log_rect)
    pygame.draw.line(screen, 'black', (512,0), (512, 512))   
    move_log = game_state.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        move_string = str(i // 2 + 1) + '. ' + str(move_log[i]) + " "
        if i + 1 < len(move_log):
            move_string += str(move_log[i + 1]) + "  "
        move_texts.append(move_string)


    #rendering text onto the page
    moves_per_row = 3
    padding = 5
    line_spacing = 2
    text_y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ""
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j]

        text_object = font.render(text, True, pygame.Color('black'))
        text_location = move_log_rect.move(padding, text_y)
        screen.blit(text_object, text_location)
        text_y += text_object.get_height() + line_spacing

#End Game Text
def drawEndGameText(screen, text):
    font = pygame.font.SysFont("Times New Roman", 32, True, False)
    text_object = font.render(text, False, pygame.Color("gray"))
    text_location = pygame.Rect(0, 0, width, height).move(width / 2 - text_object.get_width() / 2,
                                                                 height / 2 - text_object.get_height() / 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, False, pygame.Color('black'))
    screen.blit(text_object, text_location.move(2, 2))

#End Game Text
def draw_name_top(name, screen, font):
    name_top_rect = pygame.Rect(width, 0, WIDTH, 200)
    pygame.draw.rect(screen, pygame.Color((234, 221, 202)), name_top_rect)
    p1_name = name
    text_object = font.render(p1_name, True, pygame.Color('black'))
    screen.blit(text_object, (518, 10))

    legend = "Press Z: Undo"
    leg = font.render(legend, True, pygame.Color('black'))
    screen.blit(leg, (670, 10))
    
    legend2 = "Press R: Reset"
    leg2 = font.render(legend2, True, pygame.Color('black'))
    screen.blit(leg2, (670, 25))

    legend3 = "Press Q: Exit"
    leg3 = font.render(legend3, True, pygame.Color('black'))
    screen.blit(leg3, (670, 40))

#Users Name
def draw_name_bottom(name,screen, font):
    name_bottom_rect = pygame.Rect(width,HEIGHT-200 , WIDTH, HEIGHT)
    pygame.draw.rect(screen, pygame.Color((234, 221, 202)), name_bottom_rect)
    text_object = font.render(name, True, pygame.Color('black'))
    screen.blit(text_object, (522, 480))


def animateMove(move, screen, board, clock):
    """
    Animating a move
    """
    global colors
    d_row = move.end_row - move.start_row
    d_col = move.end_col - move.start_col
    frames_per_square = 10  # frames to move one square
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_square
    for frame in range(frame_count + 1):
        row, col = (move.start_row + d_row * frame / frame_count, move.start_col + d_col * frame / frame_count)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from its ending square
        color = colors[(move.end_row + move.end_col) % 2]
        end_square = pygame.Rect(move.end_col * sq_size, move.end_row * sq_size, sq_size, sq_size)
        pygame.draw.rect(screen, color, end_square)
        # draw captured piece onto rectangle
        if move.piece_captured != '--':
            if move.en_passant:
                enpassant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row - 1
                end_square = pygame.Rect(move.end_col * sq_size, enpassant_row * sq_size, sq_size, sq_size)
            screen.blit(IMAGES[move.piece_captured], end_square)
        # draw moving piece
        screen.blit(IMAGES[move.piece_shifted], pygame.Rect(col * sq_size, row * sq_size, sq_size, sq_size))
        pygame.display.flip()
        clock.tick(60)


#Medium Bot function
def main_mediumai(player_one, player_two, name_up, name_down):

    pygame.init()
    medium_bot = bots.MinimaxBot(depth = 3)
    screen = pygame.display.set_mode((width + WIDTH, height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    game_state = engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    load_images()  # do this only once before while loop
    running = True
    sq_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = pygame.font.SysFont("Times New Roman", 14, False, False)
    bold_font = pygame.font.SysFont("Times New Roman", 14, True, False)
    white = True
    black = False    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    timer = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    whiteSecs = blackSecs = 0
    delta_time = 0

    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        if human_turn:
            white = True
            black = False
        else:
            white = False
            black = True
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    location = pygame.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // sq_size
                    row = location[1] // sq_size
                    if sq_selected == (row, col) or col >= 8:  # user clicked the same square twice
                        sq_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                sq_selected = ()  # reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]

            # key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:  # undo when 'z' is pressed
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == pygame.K_r:  # reset the game when 'r' is pressed
                    game_state = engine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        #add the time elapsed last frame to correct player 
        if white:
            whiteSecs += delta_time
        else:
            blackSecs += delta_time

        # Divide by 60 to get total minutes
        minsW = whiteSecs // 60
        # Use the remainders to get the secoonds
        secW = round(whiteSecs % 60)
        # Divide by 60 to get total minutes
        minB = blackSecs // 60
        # Use the remainders to get the secoonds
        secB = round(blackSecs % 60)

        #format the lead 0s
        whiteTime = "Time: {0:02}:{1:02}".format(minsW, secW)
        # Blit timer to the screen
        whiteTimer = font.render(whiteTime, True, BLACK)
        screen.blit(whiteTimer, [590, 425])
        #format the lead 0s
        blackTime = "Time: {0:02}:{1:02}".format(minB, secB)
        # Blit timer to the screen
        blackTimer = font.render(blackTime, True, BLACK)
        screen.blit(blackTimer, [590, 80])
        pygame.display.flip()
        #get the time elapsed since the last call in milliseconds, '/1000' to get seconds
        delta_time = timer.tick(60) / 1000

        # AI move finder
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()  # used to pass data between threads
                move_finder_process = Process(target=bots.find_best_move, args=(game_state, valid_moves, return_queue))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = medium_bot.select_move(game_state)
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, sq_selected)

        if not game_over:
            draw_name_top(name_up,screen, bold_font)
            draw_name_bottom(name_down, screen, bold_font)
            drawMoveLog(screen, game_state, move_log_font)

            

        if game_state.check_mate:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stale_mate:
            game_over = True
            drawEndGameText(screen, "stalemate")

        clock.tick(fps)
    pygame.display.flip()
    pygame.display.update()

def main_easyai(player_one, player_two, name_up, name_down):

    pygame.init()
    random_bot = bots.RandomBot()
    screen = pygame.display.set_mode((width + WIDTH, height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    game_state = engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    load_images()  # do this only once before while loop
    running = True
    sq_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    ai_thinking = False
    move_undone = False
    move_finder_process = None
    move_log_font = pygame.font.SysFont("Times New Roman", 14, False, False)
    bold_font = pygame.font.SysFont("Times New Roman", 14, True, False)
    #player_one = True  # if a human is playing white, then this will be True, else False
    #player_two = False  # if a hyman is playing white, then this will be True, else False
    white = True
    black = False    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    timer = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    whiteSecs = blackSecs = 0
    delta_time = 0

    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        if human_turn:
            white = True
            black = False
        else:
            white = False
            black = True

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    location = pygame.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // sq_size
                    row = location[1] // sq_size
                    if sq_selected == (row, col) or col >= 8:  # user clicked the same square twice
                        sq_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                sq_selected = ()  # reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]

            # key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:  # undo when 'z' is pressed
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == pygame.K_r:  # reset the game when 'r' is pressed
                    game_state = engine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    if ai_thinking:
                        move_finder_process.terminate()
                        ai_thinking = False
                    move_undone = True
                if e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        #add the time elapsed last frame to correct player 
        if white:
            whiteSecs += delta_time
        else:
            blackSecs += delta_time

        # Divide by 60 to get total minutes
        minsW = whiteSecs // 60
        # Use the remainders to get the secoonds
        secW = round(whiteSecs % 60)
        # Divide by 60 to get total minutes
        minB = blackSecs // 60
        # Use the remainders to get the secoonds
        secB = round(blackSecs % 60)

        #format the lead 0s
        whiteTime = "Time: {0:02}:{1:02}".format(minsW, secW)
        # Blit timer to the screen
        whiteTimer = font.render(whiteTime, True, BLACK)
        screen.blit(whiteTimer, [590, 425])
        #format the lead 0s
        blackTime = "Time: {0:02}:{1:02}".format(minB, secB)
        # Blit timer to the screen
        blackTimer = font.render(blackTime, True, BLACK)
        screen.blit(blackTimer, [590, 80])
        pygame.display.flip()
        #get the time elapsed since the last call in milliseconds, '/1000' to get seconds
        delta_time = timer.tick(60) / 1000


        # AI move finder
        if not game_over and not human_turn and not move_undone:
            if not ai_thinking:
                ai_thinking = True
                return_queue = Queue()  # used to pass data between threads
                move_finder_process = Process(target=bots.find_best_move, args=(game_state, valid_moves, return_queue))
                move_finder_process.start()

            if not move_finder_process.is_alive():
                ai_move = random_bot.select_move(game_state)
                game_state.makeMove(ai_move)
                move_made = True
                animate = True
                ai_thinking = False

        if move_made:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, sq_selected)

        if not game_over:
            draw_name_top(name_up,screen, bold_font)
            draw_name_bottom(name_down, screen, bold_font)
            drawMoveLog(screen, game_state, move_log_font)

            

        if game_state.check_mate:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stale_mate:
            game_over = True
            drawEndGameText(screen, "stalemate")

        clock.tick(fps)
    pygame.display.flip()
    pygame.display.update()

#Chess Board for 2 players on the same device
def main_chessboard():

    pygame.init()
    random_bot = bots.RandomBot()
    screen = pygame.display.set_mode((width + WIDTH, height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    game_state = engine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False  # flag variable for when a move is made
    animate = False  # flag variable for when we should animate a move
    load_images()  # do this only once before while loop
    running = True
    sq_selected = ()  # no square is selected initially, this will keep track of the last click of the user (tuple(row,col))
    player_clicks = []  # this will keep track of player clicks (two tuples)
    game_over = False
    move_log_font = pygame.font.SysFont("Times New Roman", 14, False, False)
    bold_font = pygame.font.SysFont("Times New Roman", 14, True, False)
    player_one = True  # if a human is playing white, then this will be True, else False
    player_two = True # if a hyman is playing white, then this will be True, else False
    white = True
    black = False    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    timer = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    whiteSecs = blackSecs = 0
    delta_time = 0

    while running:
        human_turn = (game_state.white_to_move and player_one) or (not game_state.white_to_move and player_two)
        if game_state.white_to_move:
            white = True
            black = False
        else:
            white = False
            black = True
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    location = pygame.mouse.get_pos()  # (x, y) location of the mouse
                    col = location[0] // sq_size
                    row = location[1] // sq_size
                    if sq_selected == (row, col) or col >= 8:  # user clicked the same square twice
                        sq_selected = ()  # deselect
                        player_clicks = []  # clear clicks
                    else:
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected)  # append for both 1st and 2nd click
                    if len(player_clicks) == 2 and human_turn:  # after 2nd click
                        move = engine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.makeMove(valid_moves[i])
                                move_made = True
                                animate = True
                                sq_selected = ()  # reset user clicks
                                player_clicks = []
                        if not move_made:
                            player_clicks = [sq_selected]

            # key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:  # undo when 'z' is pressed
                    game_state.undoMove()
                    move_made = True
                    animate = False
                    game_over = False
                    move_undone = True
                if e.key == pygame.K_r:  # reset the game when 'r' is pressed
                    game_state = engine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    sq_selected = ()
                    player_clicks = []
                    move_made = False
                    animate = False
                    game_over = False
                    move_undone = True
                if e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


        #add the time elapsed last frame to correct player 
        if white:
            whiteSecs += delta_time
        else:
            blackSecs += delta_time

        # Divide by 60 to get total minutes
        minsW = whiteSecs // 60
        # Use the remainders to get the secoonds
        secW = round(whiteSecs % 60)
        # Divide by 60 to get total minutes
        minB = blackSecs // 60
        # Use the remainders to get the secoonds
        secB = round(blackSecs % 60)

        #format the lead 0s
        whiteTime = "Time: {0:02}:{1:02}".format(minsW, secW)
        # Blit timer to the screen
        whiteTimer = font.render(whiteTime, True, BLACK)
        screen.blit(whiteTimer, [590, 425])
        #format the lead 0s
        blackTime = "Time: {0:02}:{1:02}".format(minB, secB)
        # Blit timer to the screen
        blackTimer = font.render(blackTime, True, BLACK)
        screen.blit(blackTimer, [590, 80])
        pygame.display.flip()
        #get the time elapsed since the last call in milliseconds, '/1000' to get seconds
        delta_time = timer.tick(60) / 1000


        if move_made:
            if animate:
                animateMove(game_state.move_log[-1], screen, game_state.board, clock)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False
            move_undone = False

        drawGameState(screen, game_state, valid_moves, sq_selected)

        if not game_over:
            draw_name_top("Opponent",screen, bold_font)
            draw_name_bottom(screen, bold_font)
            drawMoveLog(screen, game_state, move_log_font)

            

        if game_state.check_mate:
            game_over = True
            if game_state.white_to_move:
                drawEndGameText(screen, "Black wins by checkmate")
            else:
                drawEndGameText(screen, "White wins by checkmate")

        elif game_state.stale_mate:
            game_over = True
            drawEndGameText(screen, "stalemate")

        clock.tick(fps)
    pygame.display.flip()
    pygame.display.update()


if __name__ == "__main__":

    main_chessboard()