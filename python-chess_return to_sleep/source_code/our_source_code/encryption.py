import base64
from Crypto.Cipher import AES
import numpy as np
import random, string
import string, secrets
import boto3
import json

#This line of code creates a new instance of the boto3 S3 client, which provides an interface for interacting with Amazon S3 (Simple Storage Service) using Python.

s3 = boto3.client('s3')

#Name of bucket
bucket_name = 'perram27boeingle'

#Create a new bucket with the name above
s3.create_bucket(Bucket=bucket_name)

#user points token
points = 1000 

# DES encryption-----------------------------------------------
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
    def log_in(self, username_l, secret_str):
        #Creating a resource
        s3 = boto3.resource('s3')

        # Reading data from the bucket
        file_name = 'my_file.txt'
        obj = s3.Object('perram27boeingle', file_name)
        data = obj.get()['Body'].read().decode('utf-8')
        my_dic = json.loads(data)

        for each in my_dic:
            if each['username'] == username_l and each['password'] == secret_str:
                print('username:', username_l, 'points', each['points'])
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


    #print function for administrator
    def printUser(self):
       #Creating a resource
        s3_client = boto3.client('s3')

        file_name = 'my_file.txt'
        response = s3_client.get_object(Bucket='perram27boeingle', Key=file_name)

        data = response['Body'].read().decode('utf-8')


        my_list = json.loads(data)
        print(my_list)


#principle function
def main():
    username = 'a'
    password = 'b'
    ap = un_encrypted_account(username, password, points)

    active = True
    while active:
        print('create your account and the password will be encrypted,input exit to quit,input show to see the account information')
        order = input('choose the function')

        if order == 'sign_up':

            print('error password, please try it again')


        elif order == 'log_in':
            while True:
                try:
                    username = input('username：')
                    password = input('password：')
                    file_name = f"{username}.txt"  
                    s3_client = boto3.client('s3')
                    data = s3_client.get_object(Bucket='perram27boeingle', Key=file_name)['Body'].read().decode('utf-8')
                    dics = json.loads(data)
                    secret_str = ap.encrypt('@$4ZOcL@BGettSfGo^#@^1w3sT*AwX$M', password)
                except Exception as e:
                    print('Error')
                    continue
                if username == dics['username'] and secret_str == dics['password']:
                    print('Success！')
                    print(f'Current user points：{dics["points"]}')
                    break
                else:
                    print('Error')
                    continue

            while True:
                command = input("Please enter the operation to perform (enter 'q' to exit)：")
                if command == 'q':
                    break
                elif command == 'win':
                    dics['points'] += 10
                    print(f"Congratulations：{dics['points']}")
                elif command == 'lose':
                    dics['points'] -= 10
                    print(f"Good try, better luck next time{dics['points']}")
                else:
                    print('Error')
            return


        elif order == 'show':
            ap.printUser()


        elif order == 'exit':
            active = False



        else:
            print('input error')


