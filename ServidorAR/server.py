import http.server, ssl, socketserver, os, socket

PORT = int(os.environ.get("PORT", "8443"))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.client_address[0], fmt % args))

def get_ip():
    ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
    return ip

httpd = socketserver.TCPServer(("0.0.0.0", PORT), Handler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

ip = get_ip()
print("\nHTTPS ativo!")
print(f"PC (localhost): https://localhost:{PORT}")
print(f"Rede (celular): https://{ip}:{PORT}\n")
print("Observação: aceite o aviso de certificado autoassinado no celular.")
print("Ctrl+C para encerrar.\n")

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nEncerrando…")
