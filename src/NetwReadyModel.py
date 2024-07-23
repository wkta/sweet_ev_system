import json
import sys

sys.path.append('..')
from ModelWithEvents import ModelWithEvents


class NetwReadyModel(ModelWithEvents):
    def __init__(self, med, localplayer):
        super().__init__(med)
        self.localplayer = localplayer

    # GENERIC ++

    # def serialize(self):
    #    raise NotImplementedError

    # def load_state(self, given_serial):
    #    raise NotImplementedError

    def push_changes(self):
        self.mediator.post('cross_push_changes', self.serialize())

    # SPECIFIC ++
    def serialize(self):
        return json.dumps(
            {'world':self.world, 'p1':self.score['p1'], 'p2':self.score['p2'], 'winner':self.winner}
        )

    def load_state(self, given_serial):
        dico_full = json.loads(given_serial)

        infos_st = dico_full['world']
        self.taken.clear()
        for lig in range(4):
            for c in range(6):
                code = infos_st[c][lig]
                if code in ('p1', 'p2', 'ai'):
                    self.positions[code] = (c, lig)
                    self.taken.add((c, lig))
                self.world[c][lig] = code
        self.score['p1'] = dico_full['p1']
        self.score['p2'] = dico_full['p2']
        self.winner = dico_full['winner']

    # - would work if not authoritative server principle

    # def move_pl(self, sym, ij_target):
    #     super().move_pl(sym, ij_target)
    #     self.push_changes()

    def remote_move_pl(self, c, lig):
        self.mediator.post('cross_move_player', json.dumps([self.localplayer, c, lig]))
