import socket
from config import Config

class Server :
    def __init__(self, host : str) :
        self.host = host
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.error = dict()
        self.status = list()
        self.read = None

    def __repr__(self) :
        return self.status[-1] if self.status else str()

    def __str__(self) :
        return "\n".join(self.status)

    def __enter__(self) :
        return self

    def __exit__(self, exception_type, exception_value, exception_track) :
        self.sock.close()
        return None

    def __iter__(self) :
        self.read = self.readsocket()
        return self.read

    def __next__(self) :
        return next(self.read)

    def init_server(self) :
        try :
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, Config.SERVERSNDBUF)
            self.sock.settimeout(Config.SERVERTIMEOUT)
            self.sock.bind((self.host, Config.SERVERPORT))
            self.sock.listen(Config.SERVERBACKLOG)
        except Exception as error :
            self.error[self.init_server.__name__] = error
            raise socket.error(error)
        else :
            string = f"[+] setting socket SO_SNDBUF {Config.SERVERSNDBUF}\n"
            string += "[+] binding on socket\n"
            string += f"[+] listen on socket with {Config.SERVERBACKLOG} backlog"
            self.status.append(string)
            return None

    def run_server(self) :
        try :
            conn, addr = self.sock.accept()
        except Exception as error :
            self.error[self.run_server.__name__] = error
            return False, None, None
        else :
            self.conn = conn
            self.conn.settimeout(Config.SERVERTIMEOUT)
            return True, conn, addr

    def readsocket(self, buffer : int = Config.SERVERRCVBUF) :
        len_data = 0
        try :
            while True :
                data = self.conn.recv(buffer)
                len_data += len(data)
                self.status.append("[+] read {len_data} from socket")
                yield data
        except Exception as error :
            self.error[self.readsocket.__name__] = error

    def readline(self, sock : socket.socket) :
        line = bytes()
        while True :
            data = sock.recv(1)
            if data == b"\n" :
                self.status.append("[+] read a line")
                return line + data
            line += data

    def writesocket(self, sock : socket.socket, data : bytes) :
        prepare : bytes = lambda x : x if isinstance(x, bytes) else x.encode()
        try :
            payload = prepare(data)
            len_ = sock.sendall(payload)
        except Exception as error :
            self.error[self.writesocket.__name__] = error
            return False
        else :
            self.status.append(f"[+] sent {len(payload)} to client")
            return True
