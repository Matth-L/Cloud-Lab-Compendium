import socket

def get(host, port, path):

    # socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    # requête http
    request = f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"
    s.sendall(request.encode('utf-8'))

    # reception
    response = bytearray()
    while chunk := s.recv(4096):
        response.extend(chunk)

    # arret
    s.close()

    # on ne garde pas l'entete
    header, body = response.split(b"\r\n\r\n", 1)
    return body.decode('utf-8')

if __name__ == "__main__":
    hosts_ports = [
        ("127.0.0.1", 80),
        ("httpforever.com", 80),
        ("example.com", 80),
    ]

    path = "/"
    for host, port in hosts_ports:
        try:
            html_content = get(host, port, path)
            print(f"Contenu de {host}:")
            print(html_content)
        except Exception as e:
            print(f"Impossible de récupérer la page de {host}: {e}")
