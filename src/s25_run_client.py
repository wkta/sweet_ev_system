import sys

import pygame

import glvars
from GameClientPlusGUI import GameClientPlusGUI
from NetworkLayer import NetworkLayer


# from ext_mediators import ServerMediator
# from ServerComponent import ServerComponent


if sys.argv[1] == 'p1':
    local_pl, remote_pl = 'p1', 'p2'
else:
    local_pl, remote_pl = 'p2', 'p1'


pygame.init()
glvars.screen = pygame.display.set_mode(glvars.scr_size)

# init network comms
netlayer = NetworkLayer()

# init other stuff
cc = GameClientPlusGUI(netlayer, local_pl)

# serv_mediator = ServerMediator(netlayer)  # s'auto enregistre
# remote_software = ServerComponent(serv_mediator)

user_cmds = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0)
}

# ----------
#  temp
# ----------
clients = [cc,]

# sync initiale !

cc._model.push_changes()  # pense a sync au démarrage
cpt = None
while cpt is None or cpt > 0:
    cpt = 0
    cpt += clients[0].mediator.update()


# game loop
while not glvars.game_over:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            glvars.game_over = True
        elif ev.type == pygame.KEYDOWN:
            if ev.key in user_cmds:
                p = cc.get_player_loc()
                print('loc:', p)
                targetcell = (p[0] + user_cmds[ev.key][0], p[1] + user_cmds[ev.key][1])
                print('target:', targetcell)
                cc.request_move(targetcell)

    # do the full event update
    cpt = None
    while cpt is None or cpt > 0:
        cpt = 0
        cpt += clients[0].mediator.update()

    # gfx update
    cc.on_paint(None)
    pygame.display.flip()

pygame.quit()
