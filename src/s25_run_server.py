import time

import glvars
from ServerComponent import ServerComponent
from UMediator import UMediator
from netw_code import NetworkLayer


HOST = '127.0.0.1'
PORT = 60111


if __name__ == '__main__':
    netl = NetworkLayer(1)
    glvars.mediator = mediator = UMediator()
    mediator.set_network_layer(netl)

    # je crois qu'il faut attendre de s'etre register sur netlayer avant de start comms
    # sinon liste des mediators est vide
    netl.start_comms((HOST, PORT))
    serv_obj = ServerComponent()

    ff = 1
    cpt = 100
    while True:
        serv_obj.proc_server_logic(time.time())
        glvars.mediator.update(True)  # saving cycles will send updates less frequently which can avoir sync errors
        # on socket interface, but creates a bit of lag
        cpt -= 1
        if cpt <= 0:
            ff = ff ^ 1  # flip bit
            print('  .tick. ' if ff else ' .tac. ')
            cpt = 100
        time.sleep(0.1)
