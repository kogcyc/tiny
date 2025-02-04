import http.server
import socketserver
import os
import markdown  # Converts Markdown to HTML

PORT = int(os.getenv("PORT", 8080))  # DigitalOcean sets this
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get script directory
PUBLIC_DIR = os.path.join(BASE_DIR, "public")  # Path to "public" folder

# Routing system (Flask-style)
routes = {}

def route(path):
    """Decorator to register routes."""
    def decorator(func):
        routes[path] = func
        return func
    return decorator

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests with dynamic wildcard routing."""
        for pattern, handler in routes.items():
            if pattern == self.path or (pattern.endswith("/*") and self.path.startswith(pattern[:-1])):
                response, mimetype = handler(self.path)
                self.send_response(200 if response else 404)
                self.send_header("Content-type", mimetype)
                self.end_headers()
                self.wfile.write(response.encode() if response else b"<h1>404 Not Found</h1>")
                return

        # Default 404
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>404 Not Found</h1>")

# Function to render any file in /public/
def render_public(path):
    """Serve files dynamically from the 'public' directory, converting Markdown to HTML if necessary."""
    filename = path[len("/public/"):]  # Extract filename
    filepath = os.path.join(PUBLIC_DIR, filename)

    if os.path.exists(filepath):
        # If it's an HTML file, serve as-is
        if filename.endswith(".html"):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read(), "text/html"

        # If it's a Markdown file, convert it to HTML
        elif filename.endswith(".md"):
            with open(filepath, "r", encoding="utf-8") as f:
                md_content = f.read()
                html_content = markdown.markdown(md_content)  # Convert MD to HTML
                return f"<html><body>{html_content}</body></html>", "text/html"

    return None, "text/html"  # Return 404 if the file is not found

# Wildcard route to serve any HTML or Markdown file inside /public/
@route("/public/*")
def serve_public(path):
    return render_public(path)

# Start the server
with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
