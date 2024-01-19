from PyQt5.QtWidgets import *   
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from client_utils import *


class MessageSender(QThread):
    """
    Initialise la classe MessageSender comme un QThread. Stocke le message à envoyer au serveur.

    :param message: Le message à envoyer au serveur.
    """

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        """
        Exécute le thread, envoyant le message au serveur. Encode le message en bytes avant l'envoi.
        """
        client_socket.send(self.message.encode())

rooms = ["1","2","3","4","5"]

class MessageReceiver(QThread):
    LOGIN = pyqtSignal()
    msg = pyqtSignal(str)
    inscri_signal = pyqtSignal()

    def __init__(self):
        """
        Initialise la classe MessageReceiver comme un QThread.
        """

        super().__init__()

    def run(self):
        """
        Exécute le thread, recevant les messages du serveur.
        Traite les messages reçus et émet des signaux correspondants à leur contenu pour les actions appropriées dans
        l'interface utilisateur.
        """
        global check
        while check:
            reponse = client_socket.recv(1024).decode("utf-8")
            try:
                msg_parts = reponse.split("/")
                
            except:
                pass

            if not reponse:
                print("Serveur inaccessible.")
                check = False
                time.sleep(5)
                QCoreApplication.exit(0)
            

            elif reponse == "CONNEXION REUSSIE":
                self.LOGIN.emit()
            
            else: 
                try:
                    if msg_parts[0] in rooms:
                        try:
                            message = f"{msg_parts[0]}/{msg_parts[1]}/{msg_parts[2]}/{msg_parts[3]}"
                        except IndexError:
                            message = f"{msg_parts[0]}/{msg_parts[1]}/{msg_parts[2]}"
                        self.msg.emit(message)
                        
                    elif reponse == "doublon":
                        self.doublon()

                    elif reponse == "BAN":
                        self.BAN()
                        
                    elif reponse == "inscrit":
                        self.inscrit()

                    elif reponse == "fail":
                        self.echec()
                    else:
                        print(f'Serveur : {reponse}')
                
                except IndexError:
                    pass

    def doublon(self):
        """
        Affiche un message d'erreur lorsque le nom d'utilisateur est déjà pris (doublon détecté lors de l'inscription).
        """
        
        error = QMessageBox()

        error.setWindowTitle("Erreur")

        error.setText("Utilisateur déjà existant")
        error.exec()

    def inscrit(self):
        """
        Affiche un message confirmant que l'inscription a été réussie.
        """
        
        error = QMessageBox()

        error.setWindowTitle("Inscription")

        error.setText("Vous avez été inscrit avec succès")
        error.exec()

    def BAN(self):
        """
        Affiche un message d'erreur indiquant que l'utilisateur a été banni.
        """
        
        error = QMessageBox()

        error.setWindowTitle("Erreur")

        error.setText("VOUS ÊTES BANNI")
        error.exec()


    def echec(self):
        """
        Affiche un message d'erreur indiquant que l'inscription a échoué.
        """
        error = QMessageBox()

        error.setWindowTitle("Erreur")

        error.setText("Echec lors de l'inscription")
        error.exec()