
class Response(object):
    def __init__(self, html = None, file = None, status : int = 200):
        self.status_code : int = status
        self.html = html 
        if not html:
            if not file:
                raise TypeError("Failed to return any valid html or file")
            with open(file, "r") as f:
                self.html = f.read()