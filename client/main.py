from client import Client
from proto import Snet
from config import Config
import sys, os

def init_client(host : str) :
    client = Client(host)
    client.init_client()
    return client

def get_header(client : Client) :
    header = bytes()
    while not header.endswith(b"\r\n\r\n") :
        line = client.read_line_from_socket()
        header += line
    else : return header

def send_meta_header(client : Client) :
    header = Snet.client_get_meta()
    client.write_to_socket(header)
    return None

def parse_meta_header(header : bytes) :
    headers = header.split(b"\r\n")
    headers = {item.split(b" : ")[0] : item.split(b" : ")[-1] for item in headers}
    name = headers[b"name"]
    size = headers[b"size"]
    buff = int(headers[b"buffer"])
    return name, size, buff

def send_dnload_header(client : Client) :
    header = Snet.client_dnloading()
    client.write_to_socket(header)
    return None

def is_uploading(header : bytes) :
    status = header.split(b"\r\n", 1)[0]
    if status == Snet.SERVERUPLD :
        return True
    else :
        raise Exception(f"\n[!] invalid header : {status} on is_dnloding")

def recv_header(client : Client) :
    header = get_header(client)
    return header

def recv_data(file : "open", client : Client) : #TODO
    part_count = 0
    buffer = Config.CLIENTRCVBUF
    for data in client.read_data_from_socket(buffer) :
