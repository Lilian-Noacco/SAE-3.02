import sys
import time
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
import socket, mysql.connector, datetime, threading
from socket import socket as sock
from server_utils import *
#from servGraph import *


class Link(threading.Thread):
    def __init__(self, connexion, message:str, thread_list):
        """
        Initialise la classe Link en tant que Thread. Stocke la connexion, le message initial et la liste des connexions actuelles.

        :param connexion: La connexion socket avec le client.
        :param message: Le message initial envoyé par le client.
        :param thread_list: La liste des connexions actives.
        """

        threading.Thread.__init__(self)
        self.conn = connexion
        self.msg = message
        self.liste_connexions:list[sock] = thread_list

    def run(self):
        """
        Exécute le thread et gère la réception des messages.
        Découpe le message initial pour identifier le type d'action(connexion, inscription, etc.).
        Gère également l'envoi du message à tous les clients connectés.
        """

        print(self.msg)
        try:
            message =  self.msg.split("/")
        except:
            pass
        

        if message[0] == "MSG":
            self.LOGIN(message)

        if message[0] == "signup":
            self.signUp(message)

        try:
            try:
                for conn in self.liste_connexions:
                    conn.send(self.msg.encode())

            except ConnectionRefusedError as err:
                print(err)
            except ConnectionResetError as err:
                print(err)

        except Exception as err:
            print(err)

    def LOGIN(self, message):
        """
        Gère le processus de connexion d'un utilisateur.
        Vérifie les identifiants de l'utilisateur dans la base de données et envoie une réponse au client selon que les
        identifiants sont corrects ou non.

        :param message: La liste des éléments du message reçu, contenant l'identifiant et le mot de passe.
        """

        try:
            query2 = ("SELECT * from users where iduser = %s and mdp = %s")
            data = (message[1], message[2])            
            c = mysql_connect.cursor()
            c.execute(query2, data)
            element = c.fetchone()
            iduser = element[0]
            mdp = element[2]
            print(message[1], message[2])
            try:
                if (iduser == message[1] and mdp == message[2]):
                    print(175)
                    LOGINmsg = "CONNEXION REUSSIE"
                    self.conn.send(LOGINmsg.encode())
                    self.get_messages_MSGs()
                    users_connexions["Connexion"].append(self.conn)
                    users_connexions["Username"].append(iduser)
                    return
                
                else:
                    self.wrong_user()
                    ERROR = "fail"
                    self.conn.send(ERROR.encode())
                    
            except:
                print("loupé")
        except:
            print("L'utilisateur n'existe pas")

    def signUp(self, message):
        """
        Gère le processus d'inscription d'un nouvel utilisateur.
        Enregistre les informations de l'utilisateur dans la base de données et envoie une réponse au client selon que
        l'inscription est réussie ou non.

        :param message: La liste des éléments du message reçu, contenant les informations nécessaires à l'inscription.
        """
        print("Inscription")
        try:
            nom = message[1]
            mdp = message[2]
            add_ip = message[3]
            pseudo = message[4]

            query2 = ("INSERT INTO users (iduser, ip, mdp, pseudo) VALUES (%s, %s, %s, %s)")            
            c = mysql_connect.cursor()

            data = (nom, add_ip, mdp, pseudo)
            c.execute(query2, data)

            mysql_connect.commit()

            inscrit = "inscrit"
            self.conn.send(inscrit.encode())
            
            c.close() 

        except mysql.connector.errors.IntegrityError:
            error = "doublon"
            self.conn.send(error.encode())

        except TypeError:
            pass

    def quitter(self):
        """
        Termine l'application lorsque cette fonction est appelée.
        """
        QCoreApplication.instance().quit()

    def send_all(self, message):
        """
        Envoie un message à tous les clients connectés.

        :param message: Le message à envoyer.
        """
        print(f"Send everyone : {message}")

    
    def get_messages_MSGs(self):
        """
        Récupère tous les messages de la base de données et les envoie au client connecté.
        Utilisé après une connexion réussie pour synchroniser l'historique des messages.
        """
        liste_msg = []

        query = ("SELECT user, texte, date, salon FROM messages;")            
        c = mysql_connect.cursor()
        c.execute(query)
        element = c.fetchall() #dictionnaire 
        for num in range(len(element)):
            user = element[num][0]
            texte = element[num][1]
            date = element[num][2]
            salon = element[num][3]
            msge = (f"{salon}/{user}/{texte}/{date}/MSGs")
            print(msge)
            liste_msg.append(msge)
            time.sleep(0.02)
            self.conn.send(msge.encode())  

    def wrong_user(self):
        """
        Affiche un message d'erreur lorsque l'identifiant ou le mot de passe est incorrect.
        Utilisée lors de la vérification des informations de connexion.
        """
        error = QMessageBox(self)
        error.setWindowTitle("Erreur")
        error.setText("Identifiant ou mot de passe incorrect.")
        error.exec()



        