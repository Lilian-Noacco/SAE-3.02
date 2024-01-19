import socket, time

def get_external_ip():
    """
    Tente de récupérer l'adresse IP externe du client en se connectant à un serveur DNS (8.8.8.8) sur le port 80.
    Si la connexion échoue, retourne l'adresse IP locale par défaut (127.0.0.1).

    :return: L'adresse IP externe du client ou l'adresse IP locale par défaut si une erreur de socket survient.
    """

    try:
        address_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        address_socket.connect(("8.8.8.8", 80))
        external_ip_address = address_socket.getsockname()[0]
        address_socket.close()
        return external_ip_address
    except socket.error:
        return "127.0.0.1"



def main():
    def main():
        """
        Tente de connecter le socket client à l'adresse IP externe sur le port 12345. Si la connexion échoue,
        affiche un message d'attente et réessaye après un délai.
        La fonction s'appelle récursivement jusqu'à ce que la connexion soit établie.
        """
    try:
        client_socket.connect((str(external_ip), 12345))
    except:
        print("En attente d'une connexion serveur")
        time.sleep(2)   
        main()

check = True

external_ip = get_external_ip()

client_socket = socket.socket()

user = None

receive = None

chat_window = None

window = None

sign_in_window = None
