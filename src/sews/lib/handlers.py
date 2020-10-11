import sys
import socket
from typing import Dict, Callable, Union
from lib.request import Request
from lib.response import Response

class Ports:
    HTTP = 80
    HTTPS = 443

class TcpHandler(socket.socket):
    def __init__(self):
        super().__init__(
            socket.AF_INET, 
            socket.SOCK_STREAM
        )
        self.prints = True
        self.listening = False
        
        # data
        self.events : Dict[str, Callable] = {}
        self.routes : Dict[str, Callable] = {}
    
    def onConnect(self, con, address):
        data = con.recv(4080)
        if isinstance(data, bytes):
            data = data.decode('utf-8')
        parsed =  Request(data, address)
        func = self.routes.get(parsed.path.lower())
        print(self.routes, parsed.success)
        if not parsed.success or not func: # 404 
            return con.send(b"HTTP/1.1 404 Not Found")
        resp = func(parsed)
        if not isinstance(resp, Response):
            raise TypeError("Invalid response from function {func}".format(func=func))
        
        con.send("HTTP/1.1 {0} OK\n{1}".format(resp.status_code, resp.html).encode('utf-8'))
        
    def serve(self, host : str, port : Union[int, Ports] = Ports.HTTP) -> None:
        self.listening = not self.listening
        if not self.listening:
            return # already listening
        self.bind((host, port))
        sys.stdout.write("[Sews] Serving on http://{0}:{1}\n".format(host, port))
        self.listen()
        try:
            while self.listening:
                con, address = self.accept()
                self.onConnect(con, address)
        except KeyboardInterrupt:
            print("intrrrupt")
            self.close()