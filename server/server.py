import socket
from config import Config

class Server :
    def __init__(self, host : str) :
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.conn = None

    def init_server(self) :
        try :
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print("[+] set socket option to REUSEADDR")
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, Config.SERVERSNDBUF)
            print(f"[+] set socket SO_SNDBUF to {Config.SERVERSNDBUF}")
            self.sock.settimeout(Config.SERVERTIMEOUT)
            print(f"[+] set socket timeout to {Config.SERVERTIMEOUT}")
            self.sock.bind((self.host, Config.SERVERPORT))
            print(f"[*] binding on {self.host}:{Config.SERVERPORT}")
            self.sock.listen(Config.SERVERBACKLOG)
            print(f"[*] listen on socket with {Config.SERVERBACKLOG} backlog")
        except socket.error as error :
            raise Exception("\n[!] " + error)
        else :
            print("[-] server inited successfully")
            return None

    def run_server(self) :
        try :
            print("[*] start socket.accept()")
            conn, addr = self.sock.accept()
            print(f"[*] new client {addr[0]}:{addr[1]} received")
        except socket.timeout as error :
            print("[!] TimeOut")
            exit()
        except socket.error as error :
            raise Exception("\n[!] " + error)
        else :
            self.conn = conn
            self.conn.settimeout(Config.SERVERTIMEOUT)
            return conn, addr

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
