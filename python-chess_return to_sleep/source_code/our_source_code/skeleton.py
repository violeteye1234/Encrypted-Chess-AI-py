import pygame
import sys
import login
import base64
from Crypto.Cipher import AES
import numpy as np
import random, string
import string, secrets
import boto3
import json

#Please run this code to access all of the code
username_text = ""

password_text = ""
#This line of code creates a new instance of the boto3 S3 client, which provides an interface for interacting with Amazon S3 (Simple Storage Service) using Python.
s3 = boto3.client('s3')

#Name of bucket
bucket_name = 'perram27boeingle'

#Create a new bucket with the name above
s3.create_bucket(Bucket=bucket_name)

# user points token
points = 1000 

#Class to encrypt, decrypt, create account and print the information
class un_encrypted_account:


    def __init__(self, username, password, points):
        self.username = username
        self.password = password
        self.points = points

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'points': self.points
        }


    # The function uses the username value inputted by the user to construct a filename for the S3 object. 
    # Then creates a new S3 object bucket with the filename and JSON data as the object contents. 
    # The function prints the dictionary representation of the account information.
    def create_account(username, password, points):
        person_account = un_encrypted_account(username, password, points)
        dics = person_account.to_dict()
        data = json.dumps(dics)
        file_name = f"{username}.txt"  
        s3_client = boto3.client('s3')
        s3_client.put_object(Body=data, Bucket='perram27boeingle', Key=file_name)
        print(dics)
    

    #Allows you to log in
    def log_in(self, username_text, secret_str):
        #Creating a resource
        s3 = boto3.resource('s3')
        file_name = 'my_file.txt'

        #Reading data from the bucket
        obj = s3.Object('perram27boeingle', file_name)
        data = obj.get()['Body'].read().decode('utf-8')
        my_dic = json.loads(data)

        for each in my_dic:
            if each['username'] == username_text and each['password'] == secret_str:
                print('username:', username_text, 'points', each['points'])
            else:
                print('error')




    #Converting to bytes
    def add_to_16(value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # return bytes

    #Encryption
    def encrypt(key, password):
        
        #Initializing the Encryptor
        aes = AES.new(un_encrypted_account.add_to_16(key), AES.MODE_ECB)  

        #Performing AES encryption
        encrypt_aes = aes.encrypt(un_encrypted_account.add_to_16(password))

        #Performing encryption and encoding the result as bytes
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  

        return encrypted_text


    #Decryption
    def decrypt(key, password):

        #Initializing the Decryptor
        aes = AES.new(un_encrypted_account.add_to_16(key), AES.MODE_ECB)

        #Decoding from base64 to Bytes
        base64_decrypted = base64.decodebytes(password.encode(encoding='utf-8')) 
        
        #Performing decryption and encoding the result as a string 
        decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')

        return decrypted_text

    #Printing user information
    def printUser(self):
        #Creating a resource
        s3_client = boto3.client('s3')
        file_name = 'my_file.txt'
        response = s3_client.get_object(Bucket='perram27boeingle', Key=file_name)

        data = response['Body'].read().decode('utf-8')


        my_list = json.loads(data)
        print(my_list)


def login_screen():

    # Initializing Pygame
    pygame.init()

    # Setting up the screen
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Login Page")

    #Setting a Flag for logging in
    logged_in = False

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
    title_text = title_font.render("Login", True, title_color)
    username_label_text = label_font.render("Username", True, label_color)
    password_label_text = label_font.render("Password", True, label_color)
    signup_label_text = input_font.render("Don't have an account? Sign up here!", True, label_color)
    continue_text = signup_font.render("Continue", True, label_color)
    quit_text = signup_font.render("Quit", True, button_text_color)

    # Setting up input boxes
    username_input_box = pygame.Rect(155, 150, 200, 30)
    password_input_box = pygame.Rect(155, 250, 200, 30)
    global username_text
    global password_text






    # Setting up buttons
    continue_button = pygame.Rect(170, 350, 175, 30)
    quit_button = pygame.Rect(210, 425, 100, 30)
    signup_button = pygame.Rect(110, 285, 300, 30)



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
                if continue_button.collidepoint(mouse_pos) and logged_in == True:
                    print("Continue")
                    
                    

                    # Setting up the screen
                    screen = pygame.display.set_mode((400, 300))
                    pygame.display.set_caption("Single Player and Multiplayer Game")
                    
                    # Setting up the buttons
                    single_player_button = pygame.Rect(100, 75, 200, 50)
                    multiplayer_button = pygame.Rect(100, 175, 200, 50)

                    #Creating a while loop
                    running = True
                    if logged_in == True:
                        #Event handling if logged in
                        while running:
                            for event in pygame.event.get():
                                #Quiting or pressing the X button on the top right of the pop up screen
                                if event.type == pygame.QUIT:
                                    running = False
                                    pygame.quit()
                                    sys.exit()
                                #Clicking the single player or multiplayer button
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    if single_player_button.collidepoint(event.pos):
                                        #Accesing function in login module
                                        login.screen_two()
                                    elif multiplayer_button.collidepoint(event.pos):
                                        #Accesing function in login module
                                        login.screen_three()
                                
                            # Filling the background with white
                            screen.fill((224, 187, 130))

                            # Drawing the buttons
                            pygame.draw.rect(screen, (74, 44, 42), single_player_button)
                            pygame.draw.rect(screen, (159, 104, 65), multiplayer_button)
                            
                            # Addding text to the buttons
                            single_player_text = pygame.font.SysFont("Times New Roman", 30).render("Single Player", True, (255, 255, 255))
                            multiplayer_text = pygame.font.SysFont("Times New Roman", 30).render("Multiplayer", True, (255, 255, 255))
                            screen.blit(single_player_text, (120, 85))
                            screen.blit(multiplayer_text, (130, 185))
                            
                            # Updating the screen
                            pygame.display.update()
                            

                        pygame.quit()
                        
                
                #Clicking the Sign up line on the Login Page
                elif signup_button.collidepoint(mouse_pos):
                    print("Sign up")
                    #Accesing function in login module
                    login.sign_page()

                #Clicking the quit button
                elif quit_button.collidepoint(mouse_pos):
                    running = False

            #Event handling for typing
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    username_text = ""
                    password_text = ""  

                #If the user presses backspace in the username and password boxes
                elif event.key == pygame.K_BACKSPACE:
                    
                    if username_input_box.collidepoint(pygame.mouse.get_pos()):
                        username_text = username_text[:-1]
                    elif password_input_box.collidepoint(pygame.mouse.get_pos()):
                        password_text = password_text[:-1]

                #If the user types in the username and password boxes
                else:

                    #Gets the username 
                    if username_input_box.collidepoint(pygame.mouse.get_pos()):
                        username_text += event.unicode

                    #Gets the password
                    elif password_input_box.collidepoint(pygame.mouse.get_pos()):
                        password_text += event.unicode

                        #Checks if the password exists in the bucket an allows user to access the chess game
                        try:
                            #Gathering information form the bucket
                            file_name = f"{username_text}.txt"
                            s3_client = boto3.client('s3')
                            data = s3_client.get_object(Bucket='perram27boeingle', Key=file_name)['Body'].read().decode('utf-8')
                            dics = json.loads(data)
                            secret_str = un_encrypted_account.encrypt(key = '@$4ZOcL@BGettSfGo^#@^1w3sT*AwX$M', password = password_text)

                        #Exception Handling
                        except Exception as e:
                            print(e)
                            print('Error')
                            continue

                        #Successfull login message and changing flag to True
                        if username_text == dics['username'] and secret_str == dics['password']:
                            print('Success')
                            logged_in = True
                            print(f'Current user points：{dics["points"]}')
                            print(username_text)
                            username_text = username_text
                            break

                        #Failed Login
                        else:
                            print('not found')
                            continue
  



        # Drawing the screen, text, boxes and rendering user input onto the screen created
        screen.fill(background_color)
        pygame.draw.rect(screen, button_color, continue_button)
        pygame.draw.rect(screen, button_color, quit_button)
        screen.blit(title_text, (210, 25))
        screen.blit(username_label_text, (195, 110))
        screen.blit(password_label_text, (200, 210))
        screen.blit(signup_label_text,(110,285))
        screen.blit(continue_text, (210, 350))
        screen.blit(quit_text, (235, 425))
        pygame.draw.rect(screen, input_color, username_input_box, 2)
        pygame.draw.rect(screen, input_color, password_input_box, 2)
        pygame.draw.line(screen, input_color,(300, 308), (410, 308), 2)
        screen.blit(input_font.render(username_text, True, input_color), (username_input_box.x+5, username_input_box.y+5))
        screen.blit(input_font.render(password_text, True, input_color), (password_input_box.x+5, password_input_box.y+5))


        # Update the screen
        pygame.display.flip()
        pygame.display.update()

    #Quiting Pygame
    pygame.quit()





if __name__ == "__main__":
    login_screen()
    print(username_text)