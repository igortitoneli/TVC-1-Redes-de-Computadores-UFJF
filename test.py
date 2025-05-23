import asyncio

from config import HOST, PORT
from utils import get_args


async def testar_conexao_async(
    host: str = HOST,
    port: int = PORT,
    mensagem: str = "Olá do cliente async",
):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        print(f"[+] Conectado ao servidor {host}:{port}")

        writer.write(mensagem.encode())
        await writer.drain()

        resposta = await reader.read(1024)
        print(f"[Servidor] Resposta: {resposta.decode().strip()}")

        writer.close()
        await writer.wait_closed()
    except ConnectionRefusedError:
        print("[!] Conexão recusada: o servidor não está disponível.")
    except Exception as e:
        print(f"[!] Erro inesperado: {e}")


async def main(args):
    tarefas = [
        testar_conexao_async(
            host=args.host,
            port=args.port,
            mensagem=f"Mensagem {i}",
        )
        for i in range(args.total)
    ]
    await asyncio.gather(*tarefas)


if __name__ == "__main__":
    args = get_args()
    asyncio.run(main(args))
