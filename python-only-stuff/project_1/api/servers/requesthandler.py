from http.server import BaseHTTPRequestHandler
import logging
class RequestHandler(BaseHTTPRequestHandler):
    


    def log_message(self, format, *args):
        logging.info(f"{self.address_string()} {args}")
    def do_GET(self):
        self.log_message = self.log_message
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    