import logging
import dotenv
import os
from servers.requesthandler import RequestHandler
from servers.httpserver import CustomServer

# load .env file
dotenv.load_dotenv(dotenv.find_dotenv())
# setup server specifications
hostname = os.getenv("HOSTNAME")
port = int(os.getenv("PORT"))

# setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler()
    ]
)

## This file is the main entry of the server. please do all router specific stuff in the main.py


webServer = CustomServer(hostname, port, RequestHandler)
logging.info(f'Server started at http://{hostname}:{port}')

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    pass

webServer.server_close()
logging.info("Server stopped.")
