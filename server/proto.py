class Snet :
    SERVERACCEPT : str = b"STAT1" # meta -> stat1, stat0
    SERVERREJECT : str = b"STAT0" # range -> stat1, stat0
    SERVERUPLOAD : str = b"UPLOADING" # downloading(client) -> uploading, stat0 (server)
    CLIENTMETA : str = b"GETMETA"
    CLIENTRANGE : str = b"GETRANGE"
    CLIENTDNLOAD : str = b"DOWNLOADING"

    def __init__(self) :
        self.header = bytes()
        self.parsed = dict()

    def parse_header(self, header : bytes) :
        header = header.split(b"\r\n")
        status = header[0].split(b" ", 1)[0]
        name = header[0].split(b" ")[-1]
        match status :
            case self.SERVERACCEPT :
                headers = {
                    "status" : status,
                    "name" : name,
                    "length" : int(header[1].split(b" : ")[-1])
                    }
                self.parsed = headers
                return headers
            case self.SERVERREJECT :
                headers = {
                    "status" : status,
                    "name" : name,
                    "files" : header[1].split(b" : ")[-1].split(b", ")
                    }
                self.parsed = headers
                return headers
            case self.SERVERUPLOAD :
                headers = {
                    "status" : status,
                    "name" : name,
                    "length" : int(header[1].split(b" : ")[-1])
                    }
                self.parsed = headers
                return headers
            case self.CLIENTMETA :
                headers = {
                    "status" : status,
                    "name" : name
                    }
                self.parsed = headers
                return headers
            case self.CLIENTRANGE :
                headers = {
                    "status" : status,
                    "name" : name,
                    "start" : int(header[1].split(b" : ")[-1]),
                    "end" : int(header[2].split(b" : ")[-1])
                    }
                self.parsed = headers
                return headers
            case self.CLIENTDNLOAD :
                headers = {
                    "status" : status,
                    "name" : name
                    }
                self.parsed = headers
                return headers
            case _ :
                raise Exception("client header doesn't match")

    def meta_header(self, name : str) :
        payload = bytes()
        payload += self.CLIENTMETA
        payload += b" %s\r\n" % (name.encode())
        payload += b"\r\n"
        self.header = payload
        return payload

    def range_header(self, name : str, start : int, end : int) :
        payload = bytes()
        payload += self.CLIENTRANGE
        payload += b" %s\r\n" % (name.encode())
        payload += b"start : %d" % (start)
        payload += b"\r\n"
        payload += b"end : %d" % (end)
        payload += b"\r\n\r\n"
        self.header = payload
        return payload

    def dnload_header(self, name : str) :
        payload = bytes()
        payload += self.CLIENTDNLOAD
        payload += b" %s\r\n" % (name.encode())
        payload += b"\r\n"
        self.header = payload
        return payload

    def accept_header(self, name : str, length : int) :
        payload = bytes()
        payload += self.SERVERACCEPT
        payload += b" %s\r\n" % (name.encode())
        payload += b"length : %d" % (length)
        payload += b"\r\n\r\n"
        self.header = payload
        return payload

    def reject_header(self, name : str, files : str) :
        payload = bytes()
        payload += self.SERVERREJECT
        payload += b" %s\r\n" % (name.encode())
        payload += b"files : %s" % (files.encode())
        payload += b"\r\n\r\n"
        self.header = payload
        return payload

    def upload_header(self, name : str, length : int) :
        payload = bytes()
        payload += self.SERVERUPLOAD
        payload += b" %s\r\n" % (name.encode())
        payload += b"length : %d" % (length)
        payload += b"\r\n\r\n"
        self.header = payload
        return payload
