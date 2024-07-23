from NetwReadyModel import NetwReadyModel
import json
import random


class ServerComponent:
    def __init__(self, mediator):
        self.mediator = mediator
        self._model = NetwReadyModel(mediator, None)

        self.mediator.register('cross_push_changes', self.on_cross_push_changes)
        self.mediator.register('player_moves', self.on_ai_movement)
        self.mediator.register('cross_move_player', self.on_cross_move_player)

        # for implem logic only:
        self._last_t_ai_moves = None
        self._empty_world = True  # if no player has ever logged in, set to True

    # important for being able to use the 'Massiv debug' function
    def disp_model(self):
        self._model.display()

    def proc_server_logic(self, info_t):
        if self._empty_world:
            return
        if self._last_t_ai_moves is None:
            self._last_t_ai_moves = info_t
            return

        dt = info_t - self._last_t_ai_moves
        if dt > 4.0:
            omega = self._model.get_possible_mvt('ai')
            if len(omega) == 0:
                return

            if len(omega) == 1:
                choice = omega[0]
            else:
                choice = random.choice(omega)
            self._model.move_pl('ai', choice)
            self._last_t_ai_moves = info_t

    # ---------------
    # callbacks
    # ---------------
    def on_ai_movement(self, event):
        # force clients to sync
        self.mediator.post('cross_sync_state', self._model.serialize())

    def on_cross_push_changes(self, event):
        self._empty_world = False
        print('serv:reception event pour enregistrer model OK', event)
        self._model.load_state(event)
        self.mediator.post('cross_sync_state', self._model.serialize())

    def on_cross_move_player(self, event):
        print('ds move player serv side')
        print(event)

        lp, i_str, j_str = json.loads(event)
        i = int(i_str)
        j = int(j_str)
        print('server: target recog:', lp, i, j)
        self._model.move_pl(lp, (i, j))
        self.mediator.post('cross_sync_state', self._model.serialize())
