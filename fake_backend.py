from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

KEY = "test123"
count = 0
class H(BaseHTTPRequestHandler):
    def do_POST(self):
        global count
        key =self.headers.get("X-API-Key")
        if key !=KEY:
            self.send_response(401)
            self.end_headers()
            return
        size = self.headers.get("Content-Length",0)
        self.rfile.read(int(size))
        if self.path.endswith("/movement"):
            count = min(25, count + 1)
            print("boarded,count =", count)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

HTTPServer(("0.0.0.0", 8000),H).serve_forever()
