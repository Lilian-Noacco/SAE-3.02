import sys
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
from socket import socket as sock
import socket
import mysql.connector
import datetime
import threading
from server_login_register_msg import Link
from server_utils import *

class Manage(threading.Thread):
    def __init__(self, connexion, thread_list):
        """
        Initialise la classe Manage en tant que Thread. Stocke la connexion actuelle et la liste des connexions actives.

        :param connexion: La connexion socket avec le client.
        :param thread_list: La liste des connexions actives.
        """

        threading.Thread.__init__(self)

        self.conn = connexion
        self.liste_connexions:list[sock] = thread_list
        self.MSGs = []


    def run(self):
        """
        Exécute le thread et gère la réception des messages.
        Découpe le message reçu pour identifier le type d'action (nouveau message, inscription, bannissement, etc.).
        Gère également la fermeture de la connexion si nécessaire.
        """
        check = True
        while check:
            try:
                message_recu = self.conn.recv(1024).decode()
                try:
                    msg = message_recu.split("/")
                except:
                    pass



                try:
                    banni = msg[3]
                except IndexError:
                    banni = None
                
                if not message_recu:
                    self.close_co()




                elif msg[0] == "MSG":
                    self.new_message(msg, message_recu)



                elif msg[0] == "signup":
                    self.inscri(message_recu)
                


                elif banni == "ban":
                    self.bannir(msg)

                elif banni == "kick":
                    self.kick(msg)
                


                elif msg[0] in rooms:

                    self.sender = Link(self.conn, message_recu, self.liste_connexions)
                    self.sender.start()

                    print(f'Message reçu : {message_recu}\n')

                    self.inserer(message_recu)
            except:
                check = False
                for conn in self.liste_connexions:
                    if conn != self.conn:
                        continue
                    else:
                        conn.close()
                        self.liste_connexions.remove(conn)

    def bannir(self, msg):
        """
        Gère le processus de bannissement d'un utilisateur.

        :param msg: La liste des éléments du message reçu, contenant les informations nécessaires au bannissement.
        """
        username = msg[4]
        admin = msg[1]
        self.ban(username, admin)

    def kick(self, msg):
        """
        Gère le processus d'exclusion (kick) d'un utilisateur.

        :param msg: La liste des éléments du message reçu, contenant les informations nécessaires à l'exclusion.
        """
        username = msg[4]
        admin = msg[1]
        self.exclure(username, admin)

    def exclure(self, guy_kicked, admin):
        """
        Exclut un utilisateur du serveur si l'admin a les droits requis.

        :param guy_kicked: L'identifiant de l'utilisateur à exclure.
        :param admin: L'identifiant de l'administrateur qui effectue l'exclusion.
        """
        try:
            query = f'SELECT admin from users WHERE iduser = "{admin}"'           
            c = mysql_connect.cursor()
            c.execute(query)
            element = c.fetchone()
        except Exception as err:
            print(err)

        if element[0]:
            index_conn = users_connexions['Username'].index(guy_kicked)
            connexion = users_connexions["Connexion"][index_conn]

            connexion.close()
    def ban(self, guy_banned, admin):
        """
        Bannit un utilisateur du serveur si l'admin a les droits requis.

        :param guy_banned: L'identifiant de l'utilisateur à bannir.
        :param admin: L'identifiant de l'administrateur qui effectue le bannissement.
        """
        try:
            query = f'SELECT admin from users WHERE iduser = "{admin}"'           
            c = mysql_connect.cursor()
            c.execute(query)
            element = c.fetchone()
            
        except Exception as err:
            print(err)

        if element[0]:
            
            try:
                query = f'UPDATE users SET ban = True WHERE iduser = "{guy_banned}"'           
                c = mysql_connect.cursor()
                c.execute(query)
                mysql_connect.commit()

                index_conn = users_connexions['Username'].index(guy_banned)
                connexion = users_connexions["Connexion"][index_conn]

                connexion.close()

            except Exception as err:
                print(err)

            try:
                query = f'UPDATE users SET ban = True WHERE ip = "{guy_banned}"'           
                c = mysql_connect.cursor()
                c.execute(query)
                mysql_connect.commit()
                
            except Exception as err:
                print(err)
        else:
            print("NOT PERMITTED")


    def new_message(self, msg, message_recu):
        """
        Gère la réception d'un nouveau message. Vérifie si l'expéditeur n'est pas banni avant de procéder.

        :param msg: La liste des éléments du message reçu.
        :param message_recu: Le message reçu complet.
        """
        if not self.check_ban(msg[1]):
            self.sender = Link(self.conn, message_recu, self.liste_connexions)
            self.sender.start()
        else:
            self.conn.send("BAN".encode())

    def inscri(self, message_recu):
        """
        Gère l'inscription d'un nouvel utilisateur.

        :param message_recu: Le message reçu complet contenant les informations d'inscription.
        """
        self.sender = Link(self.conn, message_recu, self.liste_connexions)
        self.sender.start()

    def close_co(self):
        """
        Ferme la connexion actuelle et la retire de la liste des connexions actives.
        """
        for conn in self.liste_connexions:
            if conn != self.conn:
                continue
            else:
                conn.close()
                self.liste_connexions.remove(conn)

    def check_ban(self, user):
        """
        Vérifie si un utilisateur est banni.

        :param user: L'identifiant de l'utilisateur à vérifier.
        :return: True si l'utilisateur est banni, False sinon.
        """
        try :
            query = (f"SELECT ban FROM users where iduser = '{user}'")            
            c = mysql_connect.cursor()
            c.execute(query)

            element = c.fetchone()
            element[0]

            if element[0] == True:
                return True
            else:
                return False

        except Exception as err:
            print(err)

    def quitter(self):
        """
        Ferme toutes les connexions actives et le socket du serveur, puis termine l'application.
        """
        for conn in self.liste_connexions:
            conn.close()
        self.server_socket.close()
        QCoreApplication.instance().quit()

    def inserer(self, message_recu):
        """
        Insère un nouveau message dans la base de données.

        :param message_recu: Le message reçu complet à insérer.
        """
        global salon, nom
        message = message_recu.split("/")

        date_Link = datetime.datetime.now()

        salon = int(message[0])

        nom = message[1]
        message = message[2]
        
        try:
            query = "INSERT INTO messages (user, texte, date, salon) VALUES (%s, %s, %s, %s)"            
            c = mysql_connect.cursor()
            data = (nom, message, date_Link, salon)
            c.execute(query, data)
            mysql_connect.commit()

        except Exception as error:
            print(f"Erreur d'insertion : {error}")



