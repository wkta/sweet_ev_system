import time

import glvars
import netlayer_factory
from ServerComponent import ServerComponent
from UMediator import UMediator


HOST = '127.0.0.1'
PORT = 60111


# handy linking.
# But could it work with trascrypt'pragmas'?
# from netw_socket_serv import *
# precursor = {
#     'get_server_flag': get_server_flag,     # server-side, its like a constant but ok we need it
#     'start_comms': start_comms,             # called in the server's body -->ok can stay pure JS
#     'broadcast': broadcast,                 # called by UMediator only. Line 76
#     'register_mediator': register_mediator  # called only by UMediator line 15, so mediator can receive post call in return
# }
# class Objectifier:
#     def __init__(self, **entries):
#         self.__dict__.update(entries)
# netw_layer = Objectifier(**precursor)
# --- end handy linking ---
from netlayer_factory import *

netw_layer = Objectifier(**netlayer_factory.build('socket', 'server'))


if __name__ == '__main__':
    glvars.mediator = mediator = UMediator()
    mediator.set_network_layer(netw_layer)

    # je crois qu'il faut attendre de s'etre register sur netlayer avant de start comms
    # sinon liste des mediators est vide
    netw_layer.start_comms(HOST, PORT)

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
