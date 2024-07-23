from UMediator import UMediator
from ServerComponent import ServerComponent
from NetworkLayer2 import NetworkLayer2
import time

HOST = '127.0.0.1'
PORT = 60111


if __name__ == '__main__':
    netl = NetworkLayer2()
    serv_side_mediator = UMediator(True, netl)
    # je crois qu'il faut attendre de s'etre register sur netlayer avant de start comms
    # sinon liste des mediators est vide
    netl.start_comms((HOST, PORT))
    serv_obj = ServerComponent(serv_side_mediator)
    while True:
        serv_obj.proc_server_logic(time.time())

        serv_obj.mediator.update()
        time.sleep(0.1)
