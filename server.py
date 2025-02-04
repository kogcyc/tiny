import http.server
import socketserver
import os

PORT = int(os.getenv("PORT", 8080))  # DigitalOcean sets this
routes = {}  # Dictionary to store route functions

# Flask-like route decorator
def route(path):
    def decorator(func):
        routes[path] = func
        return func
    return decorator

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests using a Flask-like routing system."""
        handler = routes.get(self.path, self.not_found)  # Get the function or 404
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(handler().encode())

    def not_found(self):
        return "<h1>404 Not Found</h1><p>The requested page does not exist.</p>"

# Define routes using the @route decorator
@route("/")
def home():
    return "<h1>Welcome to the Home Page!</h1>"

@route("/about")
def about():
    return "<h1>About</h1><p>This is a simple Python server with Flask-style routing.</p>"

@route("/contact")
def contact():
    return "<h1>Contact</h1><p>Email: hello@example.com</p>"

# Start the server
with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
