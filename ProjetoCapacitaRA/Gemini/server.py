import asyncio
import websockets
import sys

# Um conjunto (set) para armazenar todos os clientes conectados
CONNECTED_CLIENTS = set()

async def handler(websocket, path):
    """
    Manipula conexões WebSocket.
    Registra novos clientes e retransmite mensagens.
    """
    # Registra o novo cliente
    CONNECTED_CLIENTS.add(websocket)
    print(f"Cliente conectado. Total de clientes: {len(CONNECTED_CLIENTS)}")
    
    try:
        # Loop para escutar mensagens do cliente
        async for message in websocket:
            # print(f"Mensagem recebida: {message}") # Descomente para depuração

            # Retransmite a mensagem para TODOS os outros clientes conectados
            # Criamos uma lista de tarefas de envio
            tasks = []
            for client in CONNECTED_CLIENTS:
                # Não envia a mensagem de volta para quem a enviou
                if client != websocket:
                    tasks.append(client.send(message))
            
            # Executa todas as tarefas de envio em paralelo
            if tasks:
                await asyncio.gather(*tasks)

    except websockets.exceptions.ConnectionClosedError:
        print("Cliente desconectado (conexão fechada).")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        # Remove o cliente do conjunto ao desconectar
        CONNECTED_CLIENTS.remove(websocket)
        print(f"Cliente removido. Total de clientes: {len(CONNECTED_CLIENTS)}")

async def main():
    """
    Inicia o servidor WebSocket.
    """
    # 0.0.0.0 escuta em todas as interfaces de rede (importante para o celular conectar)
    # Porta 8080
    async with websockets.serve(handler, "0.0.0.0", 8080):
        print("Servidor WebSocket iniciado na porta 8080 (Python)...")
        print("Escutando em todas as interfaces (0.0.0.0).")
        print("Pressione Ctrl+C para parar o servidor.")
        await asyncio.Future()  # Roda indefinidamente

if __name__ == "__main__":
    # Verifica a versão do Python para compatibilidade com asyncio
    if sys.version_info < (3, 7):
        print("Requer Python 3.7 ou superior.")
    else:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            print("\nServidor parado.")