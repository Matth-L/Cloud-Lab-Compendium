import socket
import os

def received(socket_client):
    """
    Reçoit une requête et envoie une page HTML au client
    """
    requete = socket_client.recv(1024).decode('utf-8')
    print(f"Requête reçue:\n{requete}")

    # Analyser la requête pour obtenir le chemin du fichier demandé
    first_line = requete.split('\r\n')[0]
    parts = first_line.split(' ')

    if len(parts) < 2:
        response = "HTTP/1.0 400 Bad Request\r\n\r\n"
        socket_client.sendall(response.encode('utf-8'))
        socket_client.close()
        return

    method, path = parts[0], parts[1]

    if method != "GET":
        response = "HTTP/1.0 405 Method Not Allowed\r\n\r\n"
        socket_client.sendall(response.encode('utf-8'))
        socket_client.close()
        return

    # Vérifier si le fichier existe
    file_path = path.lstrip('/')
    if file_path == "":
        file_path = "index.html"

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        response = f"""HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8

{content}
"""
    else:
        response = """HTTP/1.0 404 Not Found
Content-Type: text/html; charset=utf-8

<!DOCTYPE HTML>
<html>
<head>
    <title>404 Not Found</title>
</head>
<body>
    <h1>404 Not Found</h1>
    <p>Le fichier demandé n'existe pas.</p>
</body>
</html>
"""

    socket_client.sendall(response.encode('utf-8'))
    socket_client.close()

def start(hote, port):
    """
    Crée un serveur HTTP sur le port donné
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
