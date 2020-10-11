
class Request(object):
    def __init__(self, data, address):
        self.address = address
        self.method, self.path, self.mode = None, None, None 
        self.headers = {}
        
        self.success = True
        self.success = self._parse(data)
    
    def _parse(self, raw):
        raw = raw.split('\n')
        try:
            print(raw[0])
            self.method, self.path, self.mode = raw[0].split()
            for i, value in enumerate(raw[1::]):
                if i >= 20:  # something is going on
                    return False
                if not ":" in value:
                    continue 
                splitted = value.split(":")
                if not len(splitted) == 2: 
                    continue 
                self.headers[splitted[0].lower().replace("-", '_')] = splitted[1].strip()
            return all([
                self.headers, self.method, self.path, self.mode
            ])
        except (IndexError, ValueError):
            return False