import sys
import pygame
import glvars
from GameClientPlusGUI import GameClientPlusGUI
from UMediator import UMediator
from netw_code import NetworkLayer


if sys.argv[1] == 'p1':
    local_pl, remote_pl = 'p1', 'p2'
else:
    local_pl, remote_pl = 'p2', 'p1'

# - constants
USER_COMMANDS = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0)
}

# init pygame for the GUI
pygame.init()
glvars.screen = pygame.display.set_mode(glvars.scr_size)
# init network comms, create a model, and force sync it
netlayer = NetworkLayer(0)
netlayer.start_comms('127.0.0.1', 60111)
glvars.mediator = mediator = UMediator()

mediator.set_network_layer(netlayer)
cc = GameClientPlusGUI(local_pl)
cc.force_sync()  # pense a sync au démarrage en demandant l'etat
cc.mediator.update()

# - game loop
while not glvars.game_over:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            glvars.game_over = True
        elif ev.type == pygame.KEYDOWN:
            if ev.key in USER_COMMANDS:
                p = cc.player_location
                dx, dy = USER_COMMANDS[ev.key]
                targetcell = (p[0] + dx, p[1] + dy)
                cc.request_move(targetcell)
    glvars.mediator.post('paint', '', False)
    # update games_events queue, then refresh the gfx buffer
    cc.mediator.update()
    pygame.display.flip()

pygame.quit()
