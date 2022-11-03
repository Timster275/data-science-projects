from servers.routers.router import Router
import logging
main_router = Router()
def func(request):
    request.send_response(200)
    request.send_header("Content-type", "text/html")
    request.end_headers()
    request.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
    request.wfile.write(bytes("<p>Request: %s</p>" % request.path, "utf-8"))
    request.wfile.write(bytes("<body>", "utf-8"))
    request.wfile.write(bytes("<p>You got in here!!!!.</p>", "utf-8"))
    request.wfile.write(bytes("</body></html>", "utf-8"))
    logging.warn("Hello World")

main_router.get("/", func)

def handleRequest(request):
    main_router.handleRequest(request)
