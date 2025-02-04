import http.server
import socketserver
import os

PORT = int(os.getenv("PORT", 8080))  # DigitalOcean App Platform will set PORTimport http.server
import socketserver
import os

PORT = int(os.getenv("PORT", 8080))  # DigitalOcean sets this
routes = {}  # Store route functions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get script directory
PUBLIC_DIR = os.path.join(BASE_DIR, "public")  # Path to "public" folder

# Flask-like route decorator
def route(path):
    def decorator(func):
        routes[path] = func
        return func
    return decorator

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests using Flask-like routing with HTML rendering."""
        handler = routes.get(self.path, self.serve_file)  # Check if route exists
        response = handler(self.path)

        if isinstance(response, tuple):  # If returning (content, mimetype)
            content, mimetype = response
            self.send_response(200)
            self.send_header("Content-type", mimetype)
            self.end_headers()
            self.wfile.write(content.encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 Not Found</h1>")

    def serve_file(self, path):
        """Serve files from /public/ dynamically."""
        if path.startswith("/public/"):
            filename = path.replace("/public/", "")  # Extract filename
            return render_template(filename)
        return "<h1>404 Not Found</h1>", "text/html"

# Function to render HTML files
def render_template(filename):
    filepath = os.path.join(PUBLIC_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read(), "text/html"
    return "<h1>404 Not Found</h1>", "text/html"

# Example route explicitly rendering a file
@route("/public/something.html")
def something(_):
    return render_template("something.html")

# Start the server
with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()


class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h2>Hello, from DigitalOcean!</h2>")

with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
