import base64
from Crypto.Cipher import AES
import numpy as np
import random, string
import string, secrets

points = 10000 # user points token

# DES encryption-----------------------------------------------
class un_encrypted_account:
    def __init__(self, username, password, points):
        self.username = username.lower()
        self.password = password.lower()
        self.points = points


class encryption_account:
    def __init__(self):
        self.account_management = []

    def creat_account(self, username, password, points):

        person_account = un_encrypted_account(username, password, points)
        self.account_management = np.array(self.account_management)
        self.account_management = np.append(self.account_management, person_account)
        np.save('alist.npy', self.account_management)

    def add_to_16(value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

        # 加密方法

    def encrypt(self, key, password):
        aes = AES.new(encryption_account.add_to_16(key), AES.MODE_ECB)  # 初始化加密器
        encrypt_aes = aes.encrypt(encryption_account.add_to_16(password))  # 先进行aes加密
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
        return encrypted_text

        # 解密方法

    def decrypt(self, key, password):
        aes = AES.new(encryption_account.add_to_16(key), AES.MODE_ECB)  # 初始化加密器
        base64_decrypted = base64.decodebytes(password.encode(encoding='utf-8'))  # 优先逆向解密base64成bytes
        decrypted_text = str(aes.decrypt(base64_decrypted), encoding='utf-8').replace('\0', '')  # 执行解密密并转码返回str
        return decrypted_text

    def printUser(self):
        k = np.load('alist.npy', allow_pickle=True, encoding="latin1")
        k = k.tolist()
        for eachone in k:
            print(eachone.username, "\tpassword:", eachone.password, eachone.points)


def main():
    demo = encryption_account()
    active = True
    while active:
        print('creat your account and the password will be encrypted,input exit to quit,input display to see the account information')
        order = input('choose the function')

        if order == 'sign':
            letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
            r = ''.join(secrets.choice(letters) for i in range(32))
            username = input('creat new user name:')
            password = input('creat your new password:')
            secret_str = demo.encrypt(r, password)
            clear_str = demo.decrypt(r, secret_str)
            demo.creat_account(username, secret_str, points)


        elif order == 'show':
            demo.printUser()


        else:
            print('input error')


main()


