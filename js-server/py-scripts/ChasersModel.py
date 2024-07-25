import random
from engine.helpers import EventReadyCls
from json_transcrypt_polyfill import json_dumps


class ChasersModel(EventReadyCls):
    MAXSCORE = 2

    def __init__(self):
        super().__init__()
        self.winner = 0  # when this isnt zero, therefore game is over
        self.taken = list()
        self.world = [
            ['.' for _ in range(4)] for _ in range(6)
        ]
        self.positions = dict()
        for sym in ('p1', 'p2', 'ai'):
            self._spawn(sym)
        self.score = {
            'p1': 0, 'p2': 0
        }

    def _find_free_random_loc(self):
        r_loc = [random.randint(0, 5), random.randint(0, 3)]
        while r_loc in self.taken:
            r_loc = [random.randint(0, 5), random.randint(0, 3)]
        return r_loc

    @staticmethod
    def enemy(x):
        if x == 'p1':
            return 'p2'
        if x == 'p2':
            return 'p1'
        raise ValueError('not recognized x argument: ' + str(x))

    def _calc_matching_rank_in_taken(self, a, b):
        for k, elt in enumerate(self.taken):
            if elt[0] == a and elt[1] == b:
                return k

    def move_pl(self, sym, ij_target):
        dmg = False
        ci, cj = self.positions[sym]
        ti, tj = ij_target

        if self.world[ti][tj] == 'ai':
            self.score[sym] += 1
            if self.score[sym] >= self.__class__.MAXSCORE:
                self.winner = 1 if sym == 'p1' else 2
            dmg = True

        self.world[ci][cj] = '.'

        # this dirty trick is for avoiding
        # a NASTY TRANSCRYPT BUG:
        # instead of simply writing:
        # self.taken.remove([ci,cj]) I have to do ...
        taken_cp = [k for k in self.taken if not (ci == k[0] and cj == k[1])]
        # and...
        self.taken = taken_cp

        self.positions[sym] = ij_target
        self.world[ti][tj] = sym
        self.taken.append([ti, tj])
        if dmg:
            self._spawn('ai')
            ret = True
        else:
            ret = False

        print('avant pev:', [ti, tj], sym)
        self.pev('player_moves', json_dumps({'cell': [ti, tj], 'who': sym}))
        if ret:
            actor_msg = '{"who":"p1"}' if sym == 'p1' else '{"who":"p2"}'
            self.pev('player_scores', actor_msg)
            if self.winner is not None:
                self.pev('player_wins', actor_msg)

    def display(self):
        for ligne in range(4):
            for col in range(6):
                print(self.world[col][ligne].ljust(5), end='')
            print()
        x, y = self.score['p1'], self.score['p2']
        print(f'score p1: {x}  |  score p2: {y} ', end='')
        if self.winner != 0:
            print('WINNER ->', self.winner)
        else:
            print()

    def _spawn(self, sym):
        p = self._find_free_random_loc()
        self.taken.append(p)
        self.positions[sym] = p
        i, j = p
        self.world[i][j] = sym

    def get_possible_mvt(self, player):
        if player in ('p1', 'p2'):
            opponents = (self.enemy(player),)
        else:
            opponents = ('p1', 'p2')  # ai is scared by players

        omega = [tuple(self.positions[player]) for _ in range(4)]
        for k_rank, offset in enumerate([(-1, 0), (1, 0), (0, -1), (0, 1)]):
            cval = self.positions[player]
            omega[k_rank] = (cval[0] + offset[0], cval[1] + offset[1])

        bad_loc = set()
        for elt in omega:
            if not (0 <= elt[0] < 6):
                bad_loc.add(elt)
            elif not (0 <= elt[1] < 4):
                bad_loc.add(elt)
            elif elt in map(self.positions.__getitem__, opponents):
                bad_loc.add(elt)

        for y in bad_loc:
            omega.remove(y)
        return omega
