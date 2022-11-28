import socket
from threading import Thread
from time import sleep
import json
class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("127.0.0.1", 2714))
        worker = Thread(target=self.wait)
        worker.start()

    def wait(self):

        data = self.client.recv(200)
        print(data.decode())
        incoming_length = int(data.decode().split(" ")[1])
        print("Incoming length: ", incoming_length)
        self.client.send("ACK".encode())
        data = self.client.recv(incoming_length)
        sleep(1)
        self.client.send(data)

c = Client()