import json

from Model import Model


class ModelWithEvents(Model):
    def __init__(self, med):
        super().__init__()
        self.mediator = med

    def move_pl(self, sym, ij_target):
        y = super().move_pl(sym, ij_target)
        self.mediator.post('player_moves', json.dumps({'cell': ij_target, 'who': sym}))
        if y:
            actor_msg = '{"who":"p1"}' if sym == 'p1' else '{"who":"p2"}'
            self.mediator.post('player_scores', actor_msg)
            if self.winner is not None:
                self.mediator.post('player_wins', actor_msg)
