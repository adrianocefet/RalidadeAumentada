// server.js
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

let clientes = [];

wss.on('connection', ws => {
  clientes.push(ws);
  ws.on('message', msg => {
    // Repasse para todos menos quem enviou (ou todos mesmo)
    clientes.forEach(c => { if (c !== ws && c.readyState === 1) c.send(msg); });
  });
  ws.on('close', () => {
    clientes = clientes.filter(c => c !== ws);
  });
});
