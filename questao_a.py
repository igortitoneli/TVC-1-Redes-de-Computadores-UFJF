from socket import socket
from threading import Thread

from utils import get_args, start_server


def handle_client(client_socket: socket, client_address):
    print()
    print(f"[+] Nova conexão de {client_address}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Mensagem recebida de {client_address}")
            client_socket.sendall(data)  # Ecoa de volta
    except Exception as e:
        print(f"[!] Erro com {client_address}: {e}")
    finally:
        # Ao fim da conexão, destrói a thread criada para liberar memória
        print(f"[-] Conexão encerrada com {client_address}")
        client_socket.close()
        print()


def main(args):
    server_socket = start_server(
        host=args.host,
        port=args.port,
    )

    try:
        while True:
            # Cria uma nova thread a cada novo cliente
            client_socket, client_address = server_socket.accept()
            client_thread = Thread(
                target=handle_client, args=(client_socket, client_address)
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[!] Servidor finalizado.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    args = get_args()
    main(args)
