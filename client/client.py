import socket
from config import Config

class Client :
    def __init__(self, host : str) :
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    def init_client(self) :
        try :
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, Config.CLIENTSNDBUF)
            print(f"[+] set socket SO_SNDBUF to {Config.CLIENTSNDBUF}")
            self.sock.settimeout(Config.CLIENTTIMEOUT)
            print(f"[+] set socket timeout to {Config.SERVERTIMEOUT}")
            self.sock.connect((self.host, Config.SERVERPORT))
            print(f"[+] preparing connection to {self.host}:{self.port}")
        except socket.error as error :
            raise Exception("\n[!] " + error)
        else :
            print("[-] server inited successfully")
            return None

    def read_data_from_socket(self, buffer : int) : #TODO
        try :
            data = bytes()
            while True :
                new_data = self.conn.recv(buffer)
                if len(data) == buffer :
                    data = bytes()
                    yield new_data
                else :
                    data += new_data
        except socket.error as error :
            raise Exception("\n[!] " + error)
        else : return None

    def read_line_from_socket(self) :
        line = bytes()
        while True :
            data = self.conn.recv(1)
            if data == b"\n" :
                return line + data
            line += data

    def write_to_socket(self, data : bytes) :
        prepare : bytes = lambda x : x if isinstance(x, bytes) else x.encode()
        try :
            payload = prepare(data)
            self.conn.sendall(payload)
        except socket.error as error :
            raise Exception("\n[!] " + error)
        else :
            print(f"[+] sent {len(payload)} to client")
            return None
