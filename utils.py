import argparse
from socket import AF_INET, SOCK_STREAM, socket

from config import HOST, PORT


def start_server(host: str = HOST, port: int = PORT) -> socket:
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"[+] Servidor ouvindo em {host}:{port}")
    return server


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Teste assíncrono de múltiplas conexões."
    )
    parser.add_argument(
        "--total",
        type=int,
        default=30,
        help="Número total de clientes simulados",
    )
    parser.add_argument(
        "--host",
        type=str,
        default=HOST,
        help="Host",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=PORT,
        help="Porta",
    )
    return parser.parse_args()
