import asyncio
import websockets

# Armazena os clientes conectados
connected = set()

async def handler(websocket, path):
    # Adiciona o novo cliente à lista
    connected.add(websocket)
    try:
        async for message in websocket:
            # Repassa a mensagem para todos os outros clientes conectados
            for conn in connected:
                if conn != websocket:
                    await conn.send(message)
    finally:
        # Remove o cliente quando desconectar
        connected.remove(websocket)

# Inicializa o servidor WebSocket na porta 8080
start_server = websockets.serve(handler, "0.0.0.0", 8080)

print("Servidor WebSocket rodando em ws://localhost:8080 ...")

# Executa o servidor
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
