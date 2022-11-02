import logging

class Router():
    def __init__(self):
        self.handlers = []

    def get(self, path, handler):
        self.handlers.append((path, handler))

    def post(self, path, handler):
        self.handlers.append((path, handler))
    
    # def use(self, path, handler):
    #     self.handlers.append((path, handler))

    def handleRequest(self, request):
        for path, handler in self.handlers:
            if request.path == path:
                handler(request)
