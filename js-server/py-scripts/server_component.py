# --- generique ou specific?
from UMediator import UMediator
from netw_node_server import *
from NetwReadyModel import NetwReadyModel
import glvars
import random
from json_transcrypt_polyfill import json_loads


# ------specific
class ServerComponent:
    def __init__(self):
        self._model = NetwReadyModel(None)
        self.mediator = glvars.mediator
        self.mediator.register('player_moves', self.on_player_moves)
        self.mediator.register('x_request_sync', self.on_x_request_sync)
        self.mediator.register('x_client_spawns', self.on_x_client_spawns)
        self.mediator.register('x_request_movement', self.on_x_request_movement)
        self._empty_world = True
        self._t_last_ai_move = None

    def disp_model(self):
        self._model.display()

    def proc_server_logic(self, info_t):
        if self._empty_world:
            return
        if self._t_last_ai_move is None:
            self._t_last_ai_move = info_t
            return

        dt = (info_t - self._t_last_ai_move)
        if dt > 3.0:
            omega = self._model.get_possible_mvt('ai')
            if len(omega) > 0:
                if len(omega) == 1:
                    choice = omega[0]
                else:
                    choice = random.choice(omega)
                self._model.move_pl('ai', choice)
                self._t_last_ai_move = info_t

    def _do_force_clients_sync(self):
        self._model.pev('x_notify_new_state', self._model.serialize())

    def on_player_moves(self, event):
        self._do_force_clients_sync()

    def on_x_request_sync(self, event):
        self._empty_world = False
        self._do_force_clients_sync()

    def on_x_client_spawns(self, event):
        pass

    def on_x_request_movement(self, event):
        print('reception on_x_request_movement par server', event)
        lp, i_str, j_str = json_loads(event)
        i, j = map(int, (i_str, j_str))
        self._model.move_pl(lp, (i, j))
        self._do_force_clients_sync()


# ------------- generique ci-dessous -----------
class Objectifier:
    def __init__(self, entries_dict):
        for k, v in entries_dict.items():
            setattr(self, k, v)
        # self.__dict__.update(entries)

def do_mediator_binding():
    med_obj = UMediator()

    netlayer = Objectifier({  # link to all that is brought from the custom netlayer
        'get_server_flag':get_server_flag,
        'start_comms':start_comms,
        'broadcast':broadcast,
        'register_mediator':register_mediator,
        'shutdown_comms':shutdown_comms
    })

    med_obj.set_network_layer(netlayer)
    glvars.set_mediator(med_obj)
    server_compo = ServerComponent()

def refresh_event_queue():
    glvars.mediator.update()

