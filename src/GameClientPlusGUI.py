import pygame

import glvars
from NetwReadyModel import NetwReadyModel
from UMediator import UMediator


P1_COLOR = 'blue'
P2_COLOR = 'red'
AI_COLOR = 'green'


class GameClientPlusGUI:
    def __init__(self, netlayer, player_sym):
        self.mediator = UMediator(False, netlayer)

        self._model = NetwReadyModel(self.mediator, player_sym)

        self.mediator.register('cross_sync_state', self.on_cross_sync_state)
        self.mediator.register('paint', self.on_paint)

        # for handling updates
        self.ft = pygame.font.Font(None, 28)
        self.scorep1_label = None
        self.scorep1_label = None
        self._update_labels()

    def _update_labels(self):
        self.scorep1_label = self.ft.render('p1:'+str(self._model.score['p1']), False, 'darkblue')
        self.scorep2_label = self.ft.render('p2:'+str(self._model.score['p2']), False, 'darkblue')

    @property
    def local_player(self):
        return self._model.localplayer

    def disp_model(self):
        glvars.screen.fill('gray')
        cellsize = 64
        p1_pos = self._model.positions['p1']
        p2_pos = self._model.positions['p2']
        ai_pos = self._model.positions['ai']

        # draw squares + entities
        for lig in range(4):
            for c in range(6):
                a, b = c*64, lig*64
                pygame.draw.rect(
                    glvars.screen, 'black',
                    (a, b, cellsize-1, cellsize-1),
                    0  # filled shape
                )
                if c == p1_pos[0] and lig == p1_pos[1]:
                    pygame.draw.rect(
                        glvars.screen, P1_COLOR,
                        (a, b, 30, 30), 6  # line width 6
                    )
                elif c == p2_pos[0] and lig == p2_pos[1]:
                    pygame.draw.rect(
                        glvars.screen, P2_COLOR,
                        (a, b, 30, 30), 6
                    )
                elif c == ai_pos[0] and lig == ai_pos[1]:
                    pygame.draw.circle(
                        glvars.screen, AI_COLOR,
                        (a+24, b+24), 16, 0
                    )
        # add labels
        glvars.screen.blit(self.scorep1_label, (80, 270))
        glvars.screen.blit(self.scorep2_label, (290, 270))

    def get_player_loc(self) -> tuple:
        return self._model.positions[self.local_player]

    def request_move(self, wanted_cell):
        possib = self._model.get_possible_mvt(self.local_player)
        print(wanted_cell)
        if wanted_cell in possib:
            self._model.remote_move_pl(*wanted_cell)
        else:
            print('ignored mvt to blocked cell')

    # -------------------------
    # callbacks
    # -------------------------
    def on_cross_sync_state(self, evcontent):
        print(f' client {self.mediator.ident} va charger un state!')
        self._model.load_state(evcontent)
        self._update_labels()

    def on_paint(self, evcontent):
        self.disp_model()
