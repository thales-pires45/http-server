import socket
import threading

USERNAME = 'thales'
PASSWORD = 'pires'
host = "localhost"
port = 8000
ADDR = (host, port)


def web(conn, addr):
    print(f'\nCliente Conectado:{addr}')
    while True:
        msg = conn.recv(2048)
        if not msg:
            break
        print(msg)
        msg_split = msg.decode().split('=')
        print(msg_split)
        senha = msg_split[-1].strip()
        nome = msg_split[-2].strip().split('&')[0]

        try:
            if senha == PASSWORD and nome == USERNAME:
                print('\nLogin realizado com sucesso!')
                with open('logado.html', encoding="utf8", errors='ignore') as file:
                    html_content = file.read().replace('\n', '')

                response = f'HTTP/1.1 200 OK\r\nContent-Type: ; charset: utf-8\r\n\r\n{html_content}'

            else:
                print('\nUsuário ou senha incorretos!')

                with open('index.html', encoding="utf8", errors='ignore') as file:
                    html_content = file.read().replace('\n', '')

                response = f"HTTP/1.1 401 Unauthorized \r\nContent-Type: ; charset: utf-8\r\n\r\n{html_content}\n"

            conn.send(response.encode())
        except:
            print('Erro ao responder.')

    conn.close()
    print('Conexão encarrada')


def Main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen()

    print("Servidor inicializado na porta " + str(port))

    while True:
        conn, addr = server_socket.accept()
        # workerThread(conn, addr)
        web_thread = threading.Thread(target=web, args=(conn, addr))
        web_thread.start()



Main()