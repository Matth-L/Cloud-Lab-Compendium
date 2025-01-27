import socket

def received(socket_client):
    """
    Recoit une requête et une page html au client
    """
    
    
    requete = socket_client.recv(1024).decode('utf-8')
    print(f"Requête reçue:\n{requete}")

    reponse = """HTTP/1.0 200 OK
    Content-Type: text/html; charset=utf-8

    <!DOCTYPE HTML>

    <html>
    <head>
        <title>Question 4 : serveur </title>
    </head>
    <body>
        <h1>Exercice 2 _ Serveur HTTP Simple : </h1>
        <p> Ceci est un paragraphe disponible sur l'adresse localhost:8080</p>
    </body>
    </html>
    """

    socket_client.sendall(reponse.encode('utf-8'))
    socket_client.close()

def start(hote, port):
    """
    Crée un serveur http sur le port donné
    """

    # Création du socket
    socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_serveur.bind((hote, port))

    socket_serveur.listen(5)
    print(f"Serveur à l'écoute sur {hote}:{port}")

    # Attente de connexion
    while True:
        socket_client, addr = socket_serveur.accept()
        print(f"Connexion acceptée de {addr}")
        received(socket_client)

if __name__ == "__main__":
    # Lancement du serveur
    hote = "localhost"
    port = 8080
    start(hote, port)
