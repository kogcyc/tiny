from wsgiref.simple_server import make_server

class TinyWeb:
    def __init__(self):
        self.routes = {}

    def route(self, path):
        def wrapper(func):
            self.routes[path] = func
            return func
        return wrapper

    def wsgi_app(self, environ, start_response):
        path = environ["PATH_INFO"]
        handler = self.routes.get(path, None)

        if handler:
            response_body = handler()
            status = "200 OK"
        else:
            response_body = "404 Not Found"
            status = "404 Not Found"

        headers = [("Content-Type", "text/html")]
        start_response(status, headers)
        return [response_body.encode()]

# ====== Initialize App ======
app = TinyWeb()

@app.route("/home")
def home():
    return "Hello from the home page"

@app.route("/")
def index():
    return "<h1>TinyWeb</h1><p>hosted on Digital Ocean</p>"

# Gunicorn needs a WSGI callable
wsgi_app = app.wsgi_app
