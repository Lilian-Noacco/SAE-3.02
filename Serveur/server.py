import sys, datetime
from PyQt5.QtWidgets import *   
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import socket, threading
from socket import socket as sock
import mysql.connector
from server_thread import Manage
from server_login_register_msg import Link
from server_utils import *


class LoginWindow(QMainWindow):

    def __init__(self):
        """
        Initialise la classe LoginWindow. Elle appelle le constructeur de la superclasse (QMainWindow) et ensuite la fonction setup pour construire la disposition de l'interface graphique.
        """
        super(LoginWindow, self).__init__()
    
        self.setup()
        
        
    def setup(self):
        """
        Configure les composants initiaux de l'interface graphique pour la fenêtre de connexion. Cela inclut la définition du titre de la fenêtre, la création des étiquettes, des champs de saisie et des boutons, et leur arrangement dans une mise en page de type grille. Configure également les connexions pour les événements de clic sur les boutons et de pression sur la touche Entrée.
        """
        self.setWindowTitle("Authentification")

        self.ex = QPushButton("Quitter")
        self.ex.clicked.connect(self.exit)

        self.id = QLabel("Identifiant")
        self.editid= QLineEdit(self)
        self.editid.returnPressed.connect(self.logIn)

        self.mdp = QLabel("Mot de passe")
        self.editmdp= QLineEdit(self)
        
        self.login = QPushButton("Login")
        self.editmdp.setEchoMode(QLineEdit.Password)
        self.login.clicked.connect(self.logIn)
        self.editmdp.returnPressed.connect(self.logIn)

        f = self.editid.text()        

        widget = QWidget()
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setCentralWidget(widget)

        grid.addWidget(self.id, 0, 0, 1, 1)
        grid.addWidget(self.editid, 0, 1, 1, 2)
        
        grid.addWidget(self.mdp, 2, 0, 1, 1)
        grid.addWidget(self.editmdp, 2, 1, 1, 2)

        grid.addWidget(self.login, 3, 1, 1, 1)
        grid.addWidget(self.ex, 3, 2, 1, 1)


    def exit(self):
        """
        Termine l'application lorsqu'elle est appelée. Connectée à l'événement de clic sur le bouton 'Quitter'.
        """
        QCoreApplication.exit(0)


    def logIn(self):
        """
        Gère le processus de connexion. Récupère les identifiants de l'utilisateur à partir des champs de saisie, se connecte à la base de données pour valider ces identifiants et gère ensuite les différentes réponses possibles (acceptation, non-administrateur, banni, etc.).
        """
        global kick 
        kick = False
        user = self.editid.text()
        mdp = self.editmdp.text()
        try :
            
            query2 = ("SELECT * from users where iduser = %s and mdp = %s")
            data = (user, mdp)

            c = mysql_connect.cursor()

            c.execute(query2, data)
            result = c.fetchone()

            nom = result[0]
            mdpe = result[2]
            admin = result[3]
            ban = result[5]

            if user == nom and mdp == mdpe:
                if ban != True:
                    if admin == True:
                        self.accept()
                    else:
                        self.not_admin()
                else:
                    self.ban()
            else:
                self.wrong_user()
        except TypeError:
            self.wrong_user()
        

    def not_admin(self):
        """
        Affiche un message d'erreur lorsque l'utilisateur connecté n'a pas les droits d'administrateur.
        """
        error = QMessageBox(self)
        error.setWindowTitle("Erreur")
        error.setText("Pas la permission !")
        error.exec()

    def wrong_user(self):
        """
        Affiche un message d'erreur lorsque le nom d'utilisateur ou le mot de passe est incorrect.
        """
        error = QMessageBox(self)
        error.setWindowTitle("Erreur")
        error.setText("Nom d'utilisateur ou mot de passe incorrect.")
        error.exec()


    def accept(self):
        """
        Gère les actions à effectuer lorsque l'authentification est réussie pour un utilisateur administrateur. Initie la session et ferme la fenêtre de connexion.
        """
        self.acc = Accept()
        self.acc.start()
        w.close()

    def ban(self):
        """
        Affiche un message d'erreur lorsque l'utilisateur est banni.
        """
        error = QMessageBox(self)
        error.setWindowTitle("Erreur")
        error.setText("Vous avez été banni.")
        error.exec()
        

class Accept(threading.Thread):

    def __init__(self):
        """
        Initialise la classe Accept en tant que Thread. Configure la liste initiale des sockets de thread.
        """
        threading.Thread.__init__(self)

        self.thread_list:list[sock] = []

    
    def run(self):
        """
        Démarre le serveur socket et écoute les connexions entrantes. Lorsqu'un client se connecte, un nouveau thread de gestion (Manage) est lancé pour gérer cette connexion.
        """
        global flag, stop
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', 12345))
        self.server_socket.listen(100)
        self.host = socket.gethostname()

        try:
            while not flag:
                self.conn, self.address = self.server_socket.accept()
                print(f"Nouvelle client")

                self.thread_list.append(self.conn)
                self.receiver = Manage(self.conn, self.thread_list)
                self.receiver.start()
           
        except Exception as err:
            print(err)


if __name__ == '__main__':
 
    app = QApplication(sys.argv)

    w = LoginWindow()
    w.resize(500,500)
    w.show()

    sys.exit(app.exec()) 


