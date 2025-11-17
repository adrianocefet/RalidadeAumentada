# Servidor WebSocket mínimo em Python para retransmitir mensagens entre clientes
# Requisitos: Python 3.10+ e o pacote "websockets"
# Instalação:  pip install websockets
# Execução:    python server.py
# O displayAR.html e o controle.html devem apontar para ws://localhost:8080

import asyncio
import os
from websockets.server import serve

CLIENTS = set()

async def broadcast(message: str, sender=None):
    to_remove = set()
    for ws in CLIENTS:
        try:
            await ws.send(message)
        except Exception:
            to_remove.add(ws)
    for ws in to_remove:
        CLIENTS.discard(ws)

async def handler(ws):
    CLIENTS.add(ws)
    try:
        async for msg in ws:
            # Repassa qualquer payload recebido (texto) para todos os conectados
            await broadcast(msg, sender=ws)
    except Exception:
        pass
    finally:
        CLIENTS.discard(ws)

async def main():
    host = os.getenv("WS_HOST", "0.0.0.0")
    port = int(os.getenv("WS_PORT", "8080"))
    # origins=None aceita qualquer origem. Ajuste conforme necessidade de segurança.
    async with serve(handler, host, port, ping_interval=20, ping_timeout=20, origins=None):
        print(f"WebSocket server ouvindo em ws://{host}:{port}")
        await asyncio.Future()  # roda indefinidamente

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Encerrado pelo usuário")

