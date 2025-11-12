/*
Servidor WebSocket mínimo para repassar mensagens entre o Controlador e o Display.
Requisitos: Node.js 18+ e o pacote "ws".

Como executar:
  1) npm init -y
  2) npm i ws
  3) node server.js
O servidor escutará em ws://localhost:8080
*/

// server.js
import { WebSocketServer } from 'ws';

const wss = new WebSocketServer({ port: 8080 });
console.log('WebSocket server ouvindo em ws://localhost:8080');

wss.on('connection', (ws) => {
  console.log('Cliente conectado');
  ws.on('message', (msg) => {
    // Repassa a todos (broadcast)
    for (const client of wss.clients) {
      if (client.readyState === 1) { // WebSocket.OPEN
        client.send(msg.toString());
      }
    }
  });
  ws.on('close', () => console.log('Cliente desconectado'));
});
