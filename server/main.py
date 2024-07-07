from server import Server
from proto import Snet
from config import Config
from parts import Partition
import socket
import os


def response_meta(name : str) :
    fpath = Config.DEFAULTPATH
    if os.path.exists(fpath + name) :
        size = os.path.getsize(fpath + name)
        header = Snet.accept_header(name, size)
        return header
    elif name == "/" :
        flist = ", ".join(os.listdir(fpath))
        header = Snet.reject_header(name, flist)
        return header
    else :
        header = Snet.reject_header(name, "NONE")
        return header

def response_range(name : str, start : int, end : int) :
    fpath = Config.DEFAULTPATH
    size = os.path.getsize(fpath + name)
    isTruerange = end > start
    isTruesize = end <= size
    if isTruerange and isTruesize :
        header = Snet.accept_header(name, end - start)
        return header
    else :
        header = Snet.reject_header(name, "NONE")
        return header

def response_dnload(name : str, start : int, end : int) :
    size = end - start
    header = Snet.upload_header(name, size)
    return header

def main(host : str) :
    server = Server(host)
    server.init_server()
    stat, conn, addr = server.run_server()
    if stat :
        header = bytes()
        while not header.endswith("\r\n\r\n") :
            line = server.readline(conn)
            header += line
        headers = Snet.parse_header(header)
        status = header["status"]
        match status :
            case Config.CLIENTMETA :
                payload = bytes()
                ...
            case Config.CLIENTRANGE :
                ...
            case Config.CLIENTDNLOAD :
                ...
            case _ :
                raise Exception("invalid client status")
    else :
        raise Exception(server.error.items()[-1])
