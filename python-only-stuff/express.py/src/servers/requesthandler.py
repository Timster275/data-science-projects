from http.server import BaseHTTPRequestHandler
from main import handleRequest
import logging

class RequestHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        logging.info(f"{self.address_string()} {args}")

    def do_GET(self):
        self.log_message = self.log_message
        handleRequest(self)

    def do_POST(self):
        self.log_message = self.log_message
        handleRequest(self)

       

    