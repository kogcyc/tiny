import http.server
import socketserver
import os

PORT = int(os.getenv("PORT", 8080))  # DigitalOcean App Platform will set PORT

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h2>Hello, from DigitalOcean!</h2>")

with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
