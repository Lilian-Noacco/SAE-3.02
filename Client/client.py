import sys, datetime
from PyQt5.QtWidgets import *   
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from client_utils import *
from client_threads import MessageReceiver, MessageSender

class RegistrationWindow(QWidget):
    global receive
    def __init__(self):
        """
        Initialise la fenêtre d'inscription. Configure les widgets, les labels, les champs de saisie et le bouton d'inscription.
        """
        super().__init__()


        self.register()

        self.setWindowTitle("REGISTRATION CLIENT")
        grid = QGridLayout()
        self.setLayout(grid)

        self.id_label = QLabel("Identifiant")
        self.edit_id = QLineEdit(self)
        
        self.mdp_label = QLabel("Mot de passe")

        self.edit_mdp = QLineEdit(self)
        self.edit_mdp.setEchoMode(QLineEdit.Password)
        
        self.confirm_mdp_label = QLabel("Confirmer Mot de passe")
        
        self.edit_confirm_mdp = QLineEdit(self)
        self.edit_confirm_mdp.setEchoMode(QLineEdit.Password)
        
        self.pseudo_label = QLabel("Pseudo")
        
        self.edit_pseudo = QLineEdit(self)
        
        self.register_button = QPushButton("Inscription")
        self.register_button.clicked.connect(self.sign_up)

        grid.addWidget(self.id_label, 0, 0)
        grid.addWidget(self.edit_id, 1, 0)
        
        grid.addWidget(self.mdp_label, 2, 0)
        grid.addWidget(self.edit_mdp, 3, 0)

        grid.addWidget(self.confirm_mdp_label, 4, 0)
        grid.addWidget(self.edit_confirm_mdp, 5, 0)

        grid.addWidget(self.pseudo_label, 6, 0)
        grid.addWidget(self.edit_pseudo, 7, 0)

        grid.addWidget(self.register_button, 8, 0)

    def sign_up(self):
        """
        Gère le processus d'inscription. Récupère les informations saisies par l'utilisateur, vérifie leur validité, puis envoie un message de demande d'inscription au serveur si tout est correct.
        """

        name = self.edit_id.text()
        password = self.edit_mdp.text()
        confirm_password = self.edit_confirm_mdp.text()
        pseudo = self.edit_pseudo.text()

        if name == "" or password == "" or pseudo == "":
            return
        else:
            if confirm_password == password:
                message = f"signup/{name}/{password}/{external_ip}/{pseudo}"
                self.sender = MessageSender(message)
                self.sender.start() 
            else:
                self.invalid_password()

    def invalid_password(self):
        """
        Affiche un message d'erreur lorsque les mots de passe saisis ne correspondent pas.
        """
        self.signin = QMessageBox()
        self.signin.setWindowTitle("ERREUR")
        self.signin.setText("Les mots de passe ne correspondent pas")
        self.signin.show()
        self.signin.hide()


    def register(self):
        """
        Affiche un message confirmant l'inscription réussie.
        """
        self.signin = QMessageBox()
        self.signin.setWindowTitle("Inscription")
        self.signin.setText("Inscription Réussie ! Veuillez vous connecter.")
        self.signin.show()
        self.signin.hide()

    def reset(self):
        """
        Réinitialise la fenêtre d'inscription, fermant le message de confirmation et rappelant la fonction register().
        """
        self.signin.close()
        self.register()


class AuthenticationWindow(QMainWindow):
    global window, chat_window, sign_in_window
    def __init__(self):
        """
        Initialise la fenêtre d'authentification. Configure la mise en page et les widgets de la fenêtre.
        """
        super(AuthenticationWindow, self).__init__()
        self.setup()
        
    def setup(self):
        """
        Configure la fenêtre d'authentification, ajoutant les widgets, les champs de saisie et les boutons.
        Démarre également le thread de réception des messages.
        """
        global receive
        self.setWindowTitle("LOGIN CLIENT")

        self.id_label = QLabel("Identifiant")
        self.edit_id = QLineEdit(self)
        self.mdp_label = QLabel("Mot de passe")
        self.edit_mdp = QLineEdit(self)
        self.edit_mdp.setEchoMode(QLineEdit.Password)
        self.LOGIN_button = QPushButton("LOGIN")
        self.LOGIN_button.clicked.connect(self.LOGIN_message)
        self.sign_in_button = QPushButton("Inscription")
        self.sign_in_button.clicked.connect(self.sign_in)

        widget = QWidget()
        grid = QGridLayout()
        widget.setLayout(grid)
        self.setCentralWidget(widget)

        grid.addWidget(self.id_label, 1, 0, 1, 1)
        grid.addWidget(self.edit_id, 1, 1, 1, 2)
        
        grid.addWidget(self.mdp_label, 2, 0, 1, 1)
        grid.addWidget(self.edit_mdp, 2, 1, 1, 2)

        grid.addWidget(self.sign_in_button, 0, 0, 1, 3)
        grid.addWidget(self.LOGIN_button, 4, 0, 1, 3)

        receive = MessageReceiver()
        receive.start()
        receive.LOGIN.connect(self.authentified)

    def LOGIN_message(self):
        """
        Gère le processus de connexion.
        Récupère les informations saisies par l'utilisateur et envoie un message de demande de connexion au serveur.
        """
        global user
        user = self.edit_id.text()
        message2 = self.edit_mdp.text()

        message = f"MSG/{user}/{message2}"
        self.sender = MessageSender(message)
        self.sender.start()

    def authentified(self):
        """
        Gère les actions à effectuer une fois l'utilisateur authentifié.
        Affiche la fenêtre de chat et ferme la fenêtre de connexion.
        """
        chat_window.show()
        window.close()

    def sign_in(self):
        """
        Affiche la fenêtre d'inscription.
        """
        sign_in_window.show()



class ChatClientWindow(QWidget):
    global receive
    def __init__(self):
        """
        Initialise la fenêtre de chat du client. Configure la mise en page et les widgets de la fenêtre.
        """
        super().__init__()

        layout = QGridLayout()
        self.setWindowTitle("CHAT CLIENT")
        self.setLayout(layout)
        tab = QTabWidget(self)

        # General
        self.general_tab = QWidget(self)
        self.general_layout = QGridLayout()  
        self.general_tab.setLayout(self.general_layout)

        self.chat_general = QTextEdit(self)
        self.chat_general.setReadOnly(True)
        self.txt_general = QLineEdit(self)  
        self.txt_general.returnPressed.connect(lambda: self.send_message("1"))
        self.send_general = QPushButton('Envoyer le message', self)
        self.send_general.clicked.connect(lambda: self.send_message("1"))

        # General layout
        self.general_layout.addWidget(self.chat_general, 2, 0, 5, 3)
        self.general_layout.addWidget(self.txt_general, 7, 0, 1, 3)
        self.general_layout.addWidget(self.send_general, 8, 0, 1, 3)
        
        # Blabla
        self.blabla_tab = QWidget(self)
        self.blabla_layout = QGridLayout()      
        self.blabla_tab.setLayout(self.blabla_layout)

        self.chat_blabla = QTextEdit(self)
        self.chat_blabla.setReadOnly(True)
        self.txt_blabla = QLineEdit(self)  
        self.txt_blabla.returnPressed.connect(lambda: self.send_message("2"))
        self.send_blabla = QPushButton('Envoyer', self) 
        self.send_blabla.clicked.connect(lambda: self.send_message("2"))

        # Blabla layout
        self.blabla_layout.addWidget(self.chat_blabla, 2, 0, 5, 3)
        self.blabla_layout.addWidget(self.txt_blabla, 7, 0)
        self.blabla_layout.addWidget(self.send_blabla, 7, 2, alignment=Qt.AlignmentFlag.AlignRight)

        # Comptabilité
        self.compta_tab = QWidget(self)
        self.compta_layout = QGridLayout()  
        self.compta_tab.setLayout(self.compta_layout)

        self.chat_compta = QTextEdit(self)
        self.chat_compta.setReadOnly(True)
        self.txt_compta = QLineEdit(self)
        self.txt_compta.returnPressed.connect(lambda: self.send_message("3"))
        self.send_compta = QPushButton('Envoyer', self)
        self.send_compta.clicked.connect(lambda: self.send_message("3"))

        # Comptabilité layout
        self.compta_layout.addWidget(self.chat_compta, 2, 0, 5, 3)
        self.compta_layout.addWidget(self.txt_compta, 7, 0)
        self.compta_layout.addWidget(self.send_compta, 7, 2, alignment=Qt.AlignmentFlag.AlignRight)

        # Informatique
        self.info_tab = QWidget(self)
        self.info_layout = QGridLayout()  
        self.info_tab.setLayout(self.info_layout)

        self.chat_info = QTextEdit(self)
        self.chat_info.setReadOnly(True)
        self.txt_info = QLineEdit(self)  
        self.txt_info.returnPressed.connect(lambda: self.send_message("4"))
        self.send_info = QPushButton('Envoyer', self)
        self.send_info.clicked.connect(lambda: self.send_message("4"))

        # Informatique layout
        self.info_layout.addWidget(self.chat_info, 2, 0, 5, 3)
        self.info_layout.addWidget(self.txt_info, 7, 0)
        self.info_layout.addWidget(self.send_info, 7, 2, alignment=Qt.AlignmentFlag.AlignRight)

        # Marketing
        self.market_tab = QWidget(self)
        self.market_layout = QGridLayout()  
        self.market_tab.setLayout(self.market_layout)

        self.chat_market = QTextEdit(self)
        self.chat_market.setReadOnly(True)
        self.txt_market = QLineEdit(self)  
        self.txt_market.returnPressed.connect(lambda: self.send_message("5"))
        self.send_market = QPushButton('Envoyer', self)
        self.send_market.clicked.connect(lambda: self.send_message("5"))

        # Marketing layout
        self.market_layout.addWidget(self.chat_market, 2, 0, 5, 3)
        self.market_layout.addWidget(self.txt_market, 7, 0)
        self.market_layout.addWidget(self.send_market, 7, 2, alignment=Qt.AlignmentFlag.AlignRight)

        # Ajouter les fenêtres
        tab.addTab(self.general_tab, 'Général')
        tab.addTab(self.blabla_tab, 'Blabla')
        tab.addTab(self.compta_tab, 'Comptabilité')
        tab.addTab(self.info_tab, 'Informatique')
        tab.addTab(self.market_tab, 'Marketing')

        # Layout de la fenêtre principale
        layout.addWidget(tab, 0, 0)

        receive.msg.connect(self.add_chat)

    def send_message(self, room):
        """
        Envoie un message au serveur.
        Récupère le texte saisi par l'utilisateur et le numéro de la salle, puis envoie le message au serveur.

        :param room: Le numéro de la salle où le message doit être envoyé.
        """
        global user
        global message
        global chat
        chat = room
        if chat == "1":
            message = f"{chat}/{user}/{self.txt_general.text()}"
        elif chat == "2":
            message = f"{chat}/{user}/{self.txt_blabla.text()}"
        elif chat == "3":
            message = f"{chat}/{user}/{self.txt_compta.text()}"
        elif chat == "4":
            message = f"{chat}/{user}/{self.txt_info.text()}"
        elif chat == "5":
            message = f"{chat}/{user}/{self.txt_market.text()}"
        self.sender = MessageSender(message)
        self.sender.start()

    def add_chat(self, msg:str):
        """
        Ajoute un message à la fenêtre de chat correspondante. Traite le message reçu et l'affiche dans le chat approprié.

        :param msg: Le message reçu à afficher.
        """
        
        message_parts = msg.split("/")

        try:
            date = message_parts[3].split(" ")[1]
            date = f"{date.split(':')[0]}:{date.split(':')[1]}"
        except IndexError:
            date = datetime.datetime.now().strftime("%H:%M")

        if message_parts[0] == "1":
            message = f"{date} : {message_parts[1]} : {message_parts[2]}"
            self.chat_general.append(message)


        elif message_parts[0] == "2":
            message = f"{date} : {message_parts[1]} : {message_parts[2]}"
            self.chat_blabla.append(message)


        elif message_parts[0] == "3":
            message = f"{date} : {message_parts[1]} : {message_parts[2]}"
            self.chat_compta.append(message)


        elif message_parts[0] == "4":
            message = f"{date} : {message_parts[1]} : {message_parts[2]}"
            self.chat_info.append(message)


        elif message_parts[0] == "5":
            message = f"{date} : {message_parts[1]} : {message_parts[2]}"
            self.chat_market.append(message)
main()
if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = AuthenticationWindow()
    window.resize(500, 500)
    window.show()

    chat_window = ChatClientWindow()
    chat_window.resize(1000,1000)

    sign_in_window = RegistrationWindow()
    sign_in_window.resize(500,500)  

    sys.exit(app.exec())
