import sys
import socket 
from enum import Enum 
from functools import wraps
from typing import Dict, Callable, Union
from lib.response import Response
from lib.handlers import TcpHandler


events_list = (
    "accept" # when a new request has been accepted 
    "before" # before the server has started listening
)


class Sews(TcpHandler):
    def __init__(self):
        super().__init__()
    
    def register(self, event):
        def deco(func):
            def wrapper(*a, **options):
                if not isinstance(event, str):
                    raise TypeError("Invalid argument event, must be string.")
                self.events[event] = func
                return func(*a, **options)
            return wrapper()
        return deco
    
    def route(self, path):
        def deco(func):
            def wrapper(*a, **kw):
                if not isinstance(path, str):
                    raise TypeError("Invalid argument path, must be string.")
                self.registerRoute(path, func)
            return wrapper()
        return deco

    def registerRoute(self, route, func):
        if not callable(func):
            raise ValueError("Function argument must be callable.")
        self.routes[route] = func


if __name__ == "__main__":
    server = Sews()
    
    @server.route("/")
    def home(req):
        print(req.headers)
        print(req.method)
        return Response(html="<h1>hi</h1>", status=200)
        
    server.serve("localhost", 5545)