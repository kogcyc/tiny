import http.server
import socketserver
import os
import markdown  # Converts Markdown to HTML

PORT = int(os.getenv("PORT", 8080))  # DigitalOcean sets this
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get script directory
PUBLIC_DIR = os.path.join(BASE_DIR, "public")  # Path to "public" folder
MD_DIR = os.path.join(PUBLIC_DIR, "md")  # Path to "public/md" folder

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
                self.wfile.write(response.encode() if response else self.render_404().encode())
                return

        # Default 404 if no route matches
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.render_404().encode())

    def render_404(self):
        """Render custom 404 page from /public/404.html."""
        content, _ = render_public("404.html")
        return content if content else "<h1>404 Not Found</h1><p>Page not found.</p>"

# Function to render any file in /public/
def render_public(filename):
    """Serve files dynamically from the 'public' directory."""
    filepath = os.path.join(PUBLIC_DIR, filename)

    if os.path.exists(filepath) and filename.endswith(".html"):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read(), "text/html"
    return None, "text/html"

# Function to render Markdown files from /public/md/
def render_public_md(filename):
    """Serve Markdown files as HTML from 'public/md' directory."""
    filepath = os.path.join(MD_DIR, filename)

    if os.path.exists(filepath) and filename.endswith(".md"):
        with open(filepath, "r", encoding="utf-8") as f:
            md_content = f.read()
            html_content = markdown.markdown(md_content)  # Convert MD to HTML
            return f"<html><body>{html_content}</body></html>", "text/html"
    return None, "text/html"

# Wildcard route to serve HTML files inside /public/
@route("/public/*")
def serve_public(path):
    filename = path[len("/public/"):]  # Extract filename from URL
    return render_public(filename)

# Wildcard route to serve Markdown files inside /public/md/
@route("/public/md/*")
def serve_public_md(path):
    filename = path[len("/public/md/"):]  # Extract filename from URL
    return render_public_md(filename)

# Route for home page
@route("/")
def serve_home(_):
    return render_public("index.html")

# Start the server
with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
