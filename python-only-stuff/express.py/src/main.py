from servers.routers.router import Router
import logging

## do your route logic in here, this is the only place where routers will be handled.

main_router = Router()
main_router.get("/", lambda request: [
    request.send_response(200),
    request.send_header("Content-type", "text/html"),
    request.end_headers(),
    request.wfile.write(bytes("<p>Request: %s</p>" % request.path, "utf-8")),
    request.wfile.write(bytes("<body>", "utf-8")),
    request.wfile.write(bytes("<p>You got in here!!!!.</p>", "utf-8")),
    request.wfile.write(bytes("</body></html>", "utf-8")),
    logging.warn("Hello World")
] )

main_router.get("/test", lambda request: [
    request.send_response(200),
    request.send_header("Content-type", "text/html"),
    request.end_headers(),
    request.wfile.write(bytes("<p>Request: %s</p>" % request.path, "utf-8")),
    request.wfile.write(bytes("<body>", "utf-8")),
    request.wfile.write(bytes("<p>You got in here too!!!!.</p>", "utf-8")),
    request.wfile.write(bytes("</body></html>", "utf-8")),
    logging.warn("Hello World")
] )

main_router.post("/", lambda request: [
    logging.info(request.rfile.read(int(request.headers.get('Content-Length')))),
    request.send_response(200),
    request.send_header("Content-type", "text/html"),
    request.end_headers(),
    request.wfile.write(bytes("{ \"message\": \"Hello World\" }", "utf-8"))
])


def handleRequest(request):
    main_router.handleRequest(request)
