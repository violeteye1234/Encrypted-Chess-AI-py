import pygame 
import sys
import main, skeleton
import encryption as ap

#Sign up page Function
def sign_page():

    # Setting up the screen
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Signup Page")

    # Setting up fonts
    title_font = pygame.font.SysFont("Times New Roman", 40)
    label_font = pygame.font.SysFont("Times New Roman", 30)
    signup_font = pygame.font.SysFont("Times New Roman",25)
    input_font = pygame.font.SysFont("Times New Roman", 20)

    # Setting up colors
    background_color = (233, 241, 250)
    title_color = (0, 0, 0)
    label_color = (0, 0, 0)
    input_color = (0, 0, 0)
    button_color = (173, 216, 230)
    button_text_color = (0, 0, 0)

    # Setting up text
    signup_text = title_font.render("Sign Up", True, title_color)
    username_label_text = label_font.render("Username", True, label_color)
    password_label_text = label_font.render("Password", True, label_color)
    repassword_label_text = label_font.render("Confirm Password", True, label_color)
    continue_text = signup_font.render("Continue", True, label_color)
    quit_text = signup_font.render("Quit", True, button_text_color)

    # Setting up input boxes
    username_input_box = pygame.Rect(155, 150, 200, 30)
    password_input_box = pygame.Rect(155, 250, 200, 30)
    repassword_input_box = pygame.Rect(155, 350, 200, 30)

    username_text = ""
    password_text = ""
    repassword_text = ""

    # Setting up buttons
    continue_button = pygame.Rect(170, 410, 175, 30)
    quit_button = pygame.Rect(380, 450, 100, 30)

    # Setting up while loop
    running = True
    while running:
    
        #Event handling
        for event in pygame.event.get():

            #Quiting or pressing the X button on the top right of the pop up screen                
            if event.type == pygame.QUIT:
                running = False
                
            #Getting mouse information
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                #Clicking the continue button
                if continue_button.collidepoint(mouse_pos):
                    print("Continue")
                    running = False 

                #Clicking the quit button   
                elif quit_button.collidepoint(mouse_pos):
                    running = False

            #Event handling for typing
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    username_text = ""
                    password_text = ""  
                    repassword_text = ""
                
                #If the user presses backspace in the username and password boxes
                elif event.key == pygame.K_BACKSPACE:
                    if username_input_box.collidepoint(pygame.mouse.get_pos()):
                        username_text = username_text[:-1]
                    elif password_input_box.collidepoint(pygame.mouse.get_pos()):
                        password_text = password_text[:-1]
                    elif repassword_input_box.collidepoint(pygame.mouse.get_pos()):
                        repassword_text = repassword_text[:-1]

                #If the user types in the username and password boxes
                else:

                    #Gets the username 
                    if username_input_box.collidepoint(pygame.mouse.get_pos()):
                        username_text += event.unicode

                    #Gets the password   
                    elif password_input_box.collidepoint(pygame.mouse.get_pos()):
                        password_text += event.unicode

                    #Gets the re-entered password and checks if they match 
                    elif repassword_input_box.collidepoint(pygame.mouse.get_pos()):
                        repassword_text += event.unicode
                        if repassword_text == password_text:

                            #Creates an account and saves them into the server
                            secret_str = ap.un_encrypted_account.encrypt(key = '@$4ZOcL@BGettSfGo^#@^1w3sT*AwX$M', password =  password_text)
                            ap.un_encrypted_account.create_account(username_text, secret_str, points = 1000)
                            print('Successfully created')

        # # Drawing the screen, text, boxes and rendering user input onto the screen created
        screen.fill(background_color)
        pygame.draw.rect(screen, button_color, continue_button)
        pygame.draw.rect(screen, button_color, quit_button)
        screen.blit(signup_text, (195, 25))
        screen.blit(username_label_text, (195, 110))
        screen.blit(password_label_text, (200, 210))
        screen.blit(repassword_label_text, (145, 310))
        screen.blit(continue_text, (210, 410))
        screen.blit(quit_text, (407, 450))
        pygame.draw.rect(screen, input_color, username_input_box, 2)
        pygame.draw.rect(screen, input_color, password_input_box, 2)
        pygame.draw.rect(screen, input_color, repassword_input_box, 2)
        screen.blit(input_font.render(username_text, True, input_color), (username_input_box.x+5, username_input_box.y+5))
        screen.blit(input_font.render(password_text, True, input_color), (password_input_box.x+5, password_input_box.y+5))
        screen.blit(input_font.render(repassword_text, True, input_color), (repassword_input_box.x+5, repassword_input_box.y+5))


        #Updating Screen
        pygame.display.update()

def screen_two():
                    
    # Set up the display
    screen_size = (400, 300)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Difficulty Level")

    # Define some colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    CINNAMON = (224, 187, 130)
    UMBER = (110, 38, 14)
    BROWN_1 =(74, 44, 42)
    BROWN_2=(159, 104, 65)


    # Set up the buttons
    button_font = pygame.font.SysFont("Times New Roman", 30)
    quit_button_rect = pygame.Rect(10,10,50,50)
    quit_font = pygame.font.SysFont("Times New Roman", 15)
    quit_button = quit_font.render("Quit", True, BLACK)

    easy_button_rect = pygame.Rect(100, 50, 200, 50)
    easy_button = button_font.render("Easy", True, WHITE)

    medium_button_rect = pygame.Rect(100, 125, 200, 50)
    medium_button = button_font.render("Medium", True, WHITE)

    hard_button_rect = pygame.Rect(100, 200, 200, 50)
    hard_button = button_font.render("Difficult", True, WHITE)

    #while loop 
    loop = True
    while loop:
    #Event handling
        for event in pygame.event.get():

            #Quiting or pressing the X button on the top right of the pop up screen
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Getting mouse information
            elif event.type == pygame.MOUSEBUTTONDOWN:

                #choose which colour
                if easy_button_rect.collidepoint(event.pos):
                    print("Easy mode selected")
                    print(skeleton.username_text +"hi")
                    black_or_white_easy()

                #choose which colour
                elif medium_button_rect.collidepoint(event.pos):
                    print("Medium mode selected")
                    black_or_white_medium()

                #choose which colour 
                elif hard_button_rect.collidepoint(event.pos):
                    print("Difficult mode selected")
                    black_or_white_difficult()
                
                #Clicking the quit button
                elif quit_button_rect.collidepoint(event.pos):
                    loop = False

        # Draw the buttons
        screen.fill(CINNAMON)
        pygame.draw.rect(screen, UMBER, easy_button_rect)
        pygame.draw.rect(screen, BROWN_2, medium_button_rect)
        pygame.draw.rect(screen, BROWN_1, hard_button_rect)
        screen.blit(easy_button, (175, 60))
        screen.blit(medium_button, (150, 135))
        screen.blit(hard_button, (150, 210))
        screen.blit(quit_button, (10,10))

        # Update the display
        pygame.display.update()


def screen_three():
                    
    # Set up the display
    screen_size = (400, 300)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Multiplayer")

    # Define some colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    CINNAMON = (224, 187, 130)
    UMBER = (110, 38, 14)
    BROWN_1 =(74, 44, 42)
    BROWN_2=(159, 104, 65)


    # Set up the buttons
    button_font = pygame.font.SysFont("Times New Roman", 30)

    quit_button_rect = pygame.Rect(10,10,50,50)
    quit_font = pygame.font.SysFont("Times New Roman", 15)
    quit_button = quit_font.render("Quit", True, BLACK)


    pc_button_rect = pygame.Rect(100, 75, 200, 50)
    pc_button = button_font.render("Pass & Play", True, WHITE)

    LAN_button_rect = pygame.Rect(100, 175, 200, 50)
    LAN_button = button_font.render("LAN", True, WHITE)

    # Setting up while loop
    loop = True
    while loop:

        #Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Getting mouse information
            elif event.type == pygame.MOUSEBUTTONDOWN:

                #Clicking the Pass and Play Button button
                if pc_button_rect.collidepoint(event.pos):
                    print("Pass and Play selected")

                    #with or without GUI
                    gui_or_no()
                
                #Clicking the LAN button
                elif LAN_button_rect.collidepoint(event.pos):
                    print("LAN mode selected")
                    #LAN game needs to be added #######################################JOE#########################3
                    main.main_chessboard()

                #Clicking the quit button
                elif quit_button_rect.collidepoint(event.pos):
                    loop = False                

        # Draw the buttons
        screen.fill(CINNAMON)
        pygame.draw.rect(screen, BROWN_1, pc_button_rect)
        pygame.draw.rect(screen, BROWN_2, LAN_button_rect)
        screen.blit(pc_button, (130, 85))
        screen.blit(LAN_button, (170, 185))
        screen.blit(quit_button, (10,10))


        # Update the display
        pygame.display.update()
      

def gui_or_no():
    # Set up the display
    screen_size = (400, 300)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("GUI")

    # Define some colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    CINNAMON = (224, 187, 130)
    UMBER = (110, 38, 14)
    BROWN_1 =(74, 44, 42)
    BROWN_2=(159, 104, 65)


    # Set up the buttons
    button_font = pygame.font.SysFont("Times New Roman", 30, False, False)

    quit_button_rect = pygame.Rect(10,10,50,50)
    quit_font = pygame.font.SysFont("Times New Roman", 15, False, False)
    quit_button = quit_font.render("Quit", True, BLACK)


    yes = pygame.Rect(100, 75, 200, 50)
    yes_button= button_font.render("With GUI", True, WHITE)

    no = pygame.Rect(100, 175, 200, 50)
    no_button = button_font.render("Without GUI", True, WHITE)

    # Setting up while loop
    loop = True
    while loop:
        #Event handling
        for event in pygame.event.get():

            #Quiting or pressing the X button on the top right of the pop up screen
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Getting mouse information
            elif event.type == pygame.MOUSEBUTTONDOWN:

                #Pass and Play with GUI
                if yes.collidepoint(event.pos):
                    print("GUI selected")
                    main.main_chessboard()

                #Pass and Play without GUI
                elif no.collidepoint(event.pos):
                    print("No GUI selected")

                #Clicking the quit button
                elif quit_button_rect.collidepoint(event.pos):
                    loop = False                

        # Draw the buttons
        screen.fill(CINNAMON)
        pygame.draw.rect(screen, BROWN_1, yes)
        pygame.draw.rect(screen, BROWN_2, no)
        screen.blit(yes_button, (140, 85))
        screen.blit(no_button, (122, 185))
        screen.blit(quit_button, (10,10))


        # Update the display
        pygame.display.update()
        

def black_or_white_easy():
    # Set up the display
    screen_size = (400, 300)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Colour")

    # Define some colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    CINNAMON = (224, 187, 130)
    UMBER = (110, 38, 14)
    BROWN_1 =(74, 44, 42)
    BROWN_2=(159, 104, 65)


    # Set up the buttons
    button_font = pygame.font.SysFont("Times New Roman", 30, False, False)

    quit_button_rect = pygame.Rect(10,10,50,50)
    quit_font = pygame.font.SysFont("Times New Roman", 15, False, False)
    quit_button = quit_font.render("Quit", True, BLACK)


    white = pygame.Rect(100, 75, 200, 50)
    white_button= button_font.render("White", True, WHITE)

    black = pygame.Rect(100, 175, 200, 50)
    black_button = button_font.render("Black", True, WHITE)

    # Setting up while loop
    loop = True
    while loop:
        #Event handling
        for event in pygame.event.get():

            #Quiting or pressing the X button on the top right of the pop up screen
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Getting mouse information
            elif event.type == pygame.MOUSEBUTTONDOWN:

                #User plays white with Easy Bot
                if white.collidepoint(event.pos):
                    print("White selected")
                    main.main_easyai(True, False, "ChatGPT", "You")

                #User plays black with Easy Bot
                elif black.collidepoint(event.pos):
                    print("Black GUI selected")
                    main.main_easyai(False, True, "You", "ChatGPT")

                #Clicking the quit button
                elif quit_button_rect.collidepoint(event.pos):
                    loop = False                

        # Draw the buttons
        screen.fill(CINNAMON)
        pygame.draw.rect(screen, BROWN_1, white)
        pygame.draw.rect(screen, BROWN_2, black)
        screen.blit(white_button, (162, 85))
        screen.blit(black_button, (162, 185))
        screen.blit(quit_button, (10,10))


        # Update the display
        pygame.display.update()

def black_or_white_medium():
    # Set up the display
    screen_size = (400, 300)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Colour")

    # Define some colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    CINNAMON = (224, 187, 130)
    UMBER = (110, 38, 14)
    BROWN_1 =(74, 44, 42)
    BROWN_2=(159, 104, 65)


    # Set up the buttons
    button_font = pygame.font.SysFont("Times New Roman", 30, False, False)

    quit_button_rect = pygame.Rect(10,10,50,50)
    quit_font = pygame.font.SysFont("Times New Roman", 15, False, False)
    quit_button = quit_font.render("Quit", True, BLACK)


    white = pygame.Rect(100, 75, 200, 50)
    white_button= button_font.render("White", True, WHITE)

    black = pygame.Rect(100, 175, 200, 50)
    black_button = button_font.render("Black", True, WHITE)

    # Setting up while loop
    loop = True
    while loop:
        #Event handling
        for event in pygame.event.get():

            #Quiting or pressing the X button on the top right of the pop up screen
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Getting mouse information
            elif event.type == pygame.MOUSEBUTTONDOWN:

                #User plays white with medium Bot
                if white.collidepoint(event.pos):
                    print("White selected")
                    main.main_mediumai(True, False, "Magnus Carlsen","You")

                #User plays black with medium Bot
                elif black.collidepoint(event.pos):
                    print("Black GUI selected")
                    main.main_mediumai(False, True, "You","Magnus Carlsen")

                #Clicking the quit button
                elif quit_button_rect.collidepoint(event.pos):
                    loop = False                

        # Draw the buttons
        screen.fill(CINNAMON)
        pygame.draw.rect(screen, BROWN_1, white)
        pygame.draw.rect(screen, BROWN_2, black)
        screen.blit(white_button, (162, 85))
        screen.blit(black_button, (162, 185))
        screen.blit(quit_button, (10,10))


        # Update the display
        pygame.display.update()

def black_or_white_difficult():
    # Set up the display
    screen_size = (400, 300)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Colour")

    # Define some colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    CINNAMON = (224, 187, 130)
    UMBER = (110, 38, 14)
    BROWN_1 =(74, 44, 42)
    BROWN_2=(159, 104, 65)


    # Set up the buttons
    button_font = pygame.font.SysFont("Times New Roman", 30, False, False)

    quit_button_rect = pygame.Rect(10,10,50,50)
    quit_font = pygame.font.SysFont("Times New Roman", 15, False, False)
    quit_button = quit_font.render("Quit", True, BLACK)


    white = pygame.Rect(100, 75, 200, 50)
    white_button= button_font.render("White", True, WHITE)

    black = pygame.Rect(100, 175, 200, 50)
    black_button = button_font.render("Black", True, WHITE)

    # Setting up while loop
    loop = True
    while loop:
        #Event handling
        for event in pygame.event.get():

            #Quiting or pressing the X button on the top right of the pop up screen
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Getting mouse information
            elif event.type == pygame.MOUSEBUTTONDOWN:

                #User plays white with difficult Bot
                if white.collidepoint(event.pos):
                    print("White selected")
                    main.main_difficultai(True, False, "Dr. Roy","You")

                #User plays black with difficult Bot
                elif black.collidepoint(event.pos):
                    print("Black GUI selected")
                    main.main_difficultai(False, True, "You","Dr. Roy")

                #Clicking the quit button
                elif quit_button_rect.collidepoint(event.pos):
                    loop = False                

        # Draw the buttons
        screen.fill(CINNAMON)
        pygame.draw.rect(screen, BROWN_1, white)
        pygame.draw.rect(screen, BROWN_2, black)
        screen.blit(white_button, (162, 85))
        screen.blit(black_button, (162, 185))
        screen.blit(quit_button, (10,10))


        # Update the display
        pygame.display.update()



