from server import Server
from proto import Snet
from config import Config
from partdata import Partition
import socket
from tempfile import TemporaryFile
import os
import time

def isfile(name : str) :
    return True if os.path.exists(name) else False

def meta_accept(server : Server, name : str) :
    part = Partition(name)
    send = server.writesocket
    payload = bytes()
    payload += Snet.accept_header(name, part.size)
    issent = send(payload)
    print(server)
    if issent :
        print(f"[+] meta data of {name} with {part.size} size has been sent")
    else :
        print(f"[!] meta data of {name} with {part.size} size hasn't been sent")
        print(server.error[server.writesocket.__name__])
        
def meta_reject(server : Server, name : str, files : list) :
    send = server.writesocket
    payload = bytes()
    payload += Snet.reject_header(name, ", ".join(files))
    issent = send(payload)
    print(server)
    if issent :
        print(f"[+] meta data of directory has been sent")
    else :
        print(f"[!] meta data of directory hasn't been sent")
        print(server.error[server.writesocket.__name__])

def range_accept() :...

def range_reject() :...

def setup() :
    tmp = TemporaryFile()
    host = socket.gethostbyname(socket.gethostname())
    server = Server(host)
    server.init_server()
    print(server)
    print("[+] server starts accepting")
    status, conn, addr = server.run_server()
    header = bytes()
    while not header.endswith(b"\r\n\r\n") :
        line = server.readline(conn)
        print(server)
        header += line
    else :
        headers = Snet.parse_header(header)
        status = headers["status"]
        print("[+] analysing status")
        match status :
            case Snet.CLIENTMETA :
                name = headers["name"].decode()
                if name != "/" and isfile(name) :
                    meta_accept(server, name)
                elif name == "/" :
                    files = os.lisdir(Config.DEFAULTPATH)
                    meta_reject(server, name, files)
                else :
                    meta_reject(server, name, [])
            case Snet.CLIENTRANGE :
                ...
