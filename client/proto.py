class Snet :
    SERVERMETA : bytes = b"METAS"
    SERVERUPLD : bytes = b"UPLODING"
    CLIENTMETA : bytes = b"GETMETA"
    CLIENTDNLD : bytes = b"DNLODING"
    CLIENTCNCL : bytes = b"CANCEL"

    def __init__(self) :
        self.header = bytes()

    def parse_header(self, header : bytes) :
        header = header.split(b"\r\n")
        status = header[0]
        match status :
            case self.SERVERMETA :
                name = header[1].split(" : ")[-1]
                size = header[2].split(" : ")[-1]
                sndbuf = header[3].split(" : ")[-1]
                headers = {
                    "status" : status,
                    "name" : name,
                    "size" : size,
                    "sndbuf" : sndbuf
                    }
                return headers
            case self.SERVERUPLD :
                headers = {
                    "status" : status
                    }
                return headers
            case self.CLIENTDNLD :
                headers = {
                    "status" : status
                    }
                return headers
            case self.CLIENTCNCL :
                headers = {
                    "status" : status
                    }
            case _ :
                raise Exception(f"invalid status : {status}")

    def server_meta(name : str, size : int, sndbuf : int) -> bytes :
        payload = bytes()
        payload += self.SERVERMETA
        payload += b"\r\n"
        payload += b"name : %b" % name.encode()
        payload += b"\r\n"
        payload += b"size : %b" % str(size).encode()
        payload += b"\r\n"
        payload += b"buffer : %b" % str(sndbuf).encode()
        payload += b"\r\n\r\n"
        return payload

    def server_uploding(self) -> bytes :
        payload = bytes()
        payload += self.SERVERUPLD
        payload += b"\r\n\r\n"
        return payload

    def client_get_meta(self) -> bytes :
        payload = bytes()
        payload += self.CLIENTMETA
        payload += b"\r\n\r\n"
        return payload

    def client_dnloding(self) -> bytes :
        payload = bytes()
        payload += self.CLIENTDNLD
        payload += b"\r\n\r\n"
        return payload

    def client_cancel(self) -> bytes :
        payload = bytes()
        payload += self.CLIENTCNCL
        payload += b"\r\n\r\n"
        return payload
