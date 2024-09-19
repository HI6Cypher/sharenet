from server import Server
from proto import Snet
from config import Config
import sys, os

def get_file(path : str) :
    if os.path.exists(path) :
        name = path.split("/")[-1]
        size = os.path.getsize(path)
        file = open(path, "rb")
        return name, size, file
    else :
        raise Exception(f"[!] file {name} not found!")

def init_server(host : str) :
    server = Server(host)
    server.init_server()
    return server

def start_accepting(server : Server) :
    conn, addr = server.run_server()
    return conn, addr

def get_header(server : Server) :
    header = bytes()
    while not header.endswith(b"\r\n\r\n") :
        line = server.read_line_from_socket()
        header += line
    else : return header

def is_get(header : bytes) :
    status = header.split(b"\r\n", 1)[0]
    return True if status == Snet.CLIENTMETA else False

def is_dnloding(header : bytes) :
    status = header.split(b"\r\n", 1)[0]
    match status :
        case Snet.CLIENTDNLD :
            return True
        case Snet.CLIENTCNCL :
            return False
        case _ :
            raise Exception(f"\n[!] invalid header : {status} on is_dnloding")

def send_meta_header(name : str, size : int, sndbuf : int, server : Server) :
    header = Snet.server_meta(name, size, sndbuf)
    server.write_to_socket(header)
    return None

def recv_response(server : Server) :
    header = get_header(server)
    return header

def send_data(file : "open", server : Server) :
    header = Snet.server_uploding()
    part_count = 0
    isheader_sent = False
    buffer = Config.SERVERSNDBUF
    while True :
        if not isheader_sent :
            server.write_to_socket(header)
            isheader_sent = True
            del header
        data = file.read(buffer)
        if data :
            server.write_to_socket(data)
            part_count += 1
        else :
            print("[-] file has been sent")
            break
    return part_count

def main(host : str, path : str) :
    name, size, file = get_file(path)
    server = init_server(host)
    conn, addr = start_accepting(server)
    header = get_header(server)
    if is_get(header) :
        buffer = Config.SERVERSNDBUF
        send_meta_header(name, size, buffer, server)
        response_header = recv_response(server)
        if is_dnloding(response_header) :
            part_count = send_data(file, server)
            print(f"[-] data's sent in {part_count} parts")
            return True
        else : return False
    else : return False

if __name__ == "__main__" :
    if len(sys.argv) == 2 :
        path = sys.argv[1]
        host = input("host (default 192.168.43.241) : ")
        host = host if host else "192.168.43.241"
        while True :
            os.system("clear || cls")
            print("[*] start sharing...")
            status = main(host, path)
            if status :
                print("[*] stop sharing...")
                break
            else :
                again = input("do you wanna start sharing again? [y/N] ")
                if again : continue
                else : break
    else :
        print("invalid argument")
