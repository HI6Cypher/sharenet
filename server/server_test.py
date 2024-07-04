from server import Server
import socket
with Server("localhost") as serv :
    assert serv.init_server() == True, serv.error
    print(str(serv))
    stat, conn, addr = serv.run_server()
    assert stat == True, serv.error
    if stat :
        assert isinstance(conn, socket.socket), serv.error
# Server.readline and Server.readsocket Server.writesocket work fine
