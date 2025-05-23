from socket import socket
import threading
import queue

from config import MAX_THREADS
from utils import get_args, start_server


# Fila de clientes
client_queue = queue.Queue(maxsize=MAX_THREADS)


def client_handler():
    while True:
        client_socket, client_address = client_queue.get()  # Aguarda cliente
        try:
            print(f"[+] Cliente conectado: {client_address}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                client_socket.sendall(data)  # Eco
        except Exception as e:
            print(f"[!] Erro com {client_address}: {e}")
        finally:
            print(f"[-] Cliente desconectado: {client_address}")
            client_socket.close()
            client_queue.task_done()  # Marca como finalizado


def create_thread_poll(max_threads: int = MAX_THREADS) -> None:
    print(f"[+] Iniciando pool de {max_threads} threads...")
    for _ in range(max_threads):
        t = threading.Thread(target=client_handler, daemon=True)
        t.start()


def close_client(client_socket: socket, client_address):
    print(f"[!] Conexão recusada: {client_address} (todas as threads ocupadas)")
    client_socket.sendall(b"Servidor ocupado. Tente novamente mais tarde.\n")
    client_socket.close()


def main(args):
    server_socket = start_server(
        host=args.host,
        port=args.port,
    )

    create_thread_poll()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            if not client_queue.full():
                client_queue.put((client_socket, client_address))
            else:
                close_client(client_socket, client_address)
    except KeyboardInterrupt:
        print("\n[!] Servidor encerrado.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    args = get_args()
    main(args)
