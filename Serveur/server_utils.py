import sys
import time
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
import socket, mysql.connector, datetime, threading
from socket import socket as sock

mysql_connect = mysql.connector.connect(
    host='localhost', #host
    user='toto', #utilisateur
    password='',
    database='sae301' #nom de la db
)

c = mysql_connect.cursor()

check = True

rooms = ["1","2","3","4","5"]


flag = False
stop = False

users_connexions = {"Connexion" : [], "Username" : []}