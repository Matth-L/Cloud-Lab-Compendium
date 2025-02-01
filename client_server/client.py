import socket
import ssl

def get(host, port, path, use_https=False):
    # socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if use_https:
        context = ssl.create_default_context()
        s = context.wrap_socket(s, server_hostname=host)
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
    return response.decode('utf-8')

if __name__ == "__main__":
    hosts_ports = [
        ("127.0.0.1", 8080, False),
        ("example.com", 80, False),
        ("google.ca", 443, True),
    ]

    path = "/"
    for host, port, use_https in hosts_ports:
        try:
            html_content = get(host, port, path, use_https)
            print(f"Contenu de {host}:")
            print(html_content)
        except Exception as e:
            print(f"Impossible de récupérer la page de {host}: {e}")
