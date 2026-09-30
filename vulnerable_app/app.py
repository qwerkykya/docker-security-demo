import http.server
import socketserver

PORT = 8080

class VulnerableHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        response_text = "<h1>Уязвимый сервис запущен!</h1><p>Работает от root без ограничений.</p>"
        self.wfile.write(response_text.encode('utf-8'))

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), VulnerableHTTPRequestHandler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        httpd.serve_forever()