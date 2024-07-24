"""
Classe qui aide à etre très flexible niveau communications réseau.
On peut switcher facilement d'une interface à l'autre en la construisant
à la demande, en passant deux arguments à savoir:

 Contexte , client/server

"""

import importlib


__all__ = [
    'build',
    'Objectifier'
]

# Define a mapping of parameter pairs to module names
netw_strat_table = {
    ('socket', 'client'): 'netw_socket_client',
    ('socket', 'server'): 'netw_socket_server',
    # ('ws', 'client'): 'netw_ws_client',
    # ('ws', 'server'): 'netw_ws_server',

    # ... Feel free to add more mappings as needed
}

tmp = tuple(netw_strat_table.keys())
prefx = 'netw_strategies.'
for k in tmp:
    netw_strat_table[k] = prefx+netw_strat_table[k]


class Objectifier:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def build(param1, param2) -> dict:
    """
    Helps retrieving functions from a particular netw_* module,
    based on the two given parameters.
    :param param1: info about the context/technology such as 'socket', 'ws', or 'nodejs'
    :param param2: either 'client' or 'server', nothing else
    :return: a dictionary of functions
    """

    module_name = netw_strat_table.get((param1, param2))
    if not module_name:
        raise ValueError(f"No module found for parameters: {param1}, {param2}")

    # Import the module dynamically
    module = importlib.import_module(module_name)

    # Extract the functions
    f1 = getattr(module, 'get_server_flag')
    f2 = getattr(module, 'start_comms')
    f3 = getattr(module, 'broadcast')
    f4 = getattr(module, 'register_mediator')

    return {
        'get_server_flag': f1,
        'start_comms': f2,
        'broadcast': f3,
        'register_mediator': f4,
    }

# -- just testing
# truc = Objectifier(**build('socket', 'server'))
# print(truc.broadcast)
# print(truc.get_server_flag())
