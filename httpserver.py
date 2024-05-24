from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import base64

USER = "admin"
PASSWORD = "password"

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not self.authenticate():
            self.send_authenticate_header()
            return

        if self.path == "/":
            self.handle_welcome()
        elif self.path == "/info":
            self.handle_info()
        elif self.path == "/pic":
            self.handle_pic()
        else:
            self.handle_not_found()

    def send_authenticate_header(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="PyHTTPServer"')
        self.end_headers()
        self.wfile.write(b"Please log in to access this content.")

    def authenticate(self):
        auth_header = self.headers.get("Authorization")
        if auth_header:
            auth_type, auth_token = auth_header.split()
            if auth_type.lower() == "basic":
                decoded_token = base64.b64decode(auth_token).decode("utf-8")
                username, password = decoded_token.split(":")
                return username == USER and password == PASSWORD
        return False

    def handle_welcome(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Welcome to the Server!</h1>")

    def handle_info(self):
        data = {"message": "This is dynamic information."}
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def handle_pic(self):
        image_path = os.path.join("static", "5G-Wireless-Technology.png")
        if os.path.exists(image_path):
            self.serve_file(image_path, "image/png")
        else:
            self.handle_not_found()

    def handle_not_found(self):
        self.send_error(404, "Page not found.")

    def serve_file(self, path, content_type):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        with open(path, "rb") as file:
            self.wfile.write(file.read())

def run_server():
    server_address = ('', 8038)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print("Starting the server on port 8038...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
