from http.server import HTTPServer
import logging

class CustomServer(HTTPServer):
    def __init__(self, hostname, port, handler):
        super().__init__((hostname, port), handler)
        