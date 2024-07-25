from json_transcrypt_polyfill import json_loads


mediators = list()
inbound_connections = list()
ref_threads = list()

__all__ = [
    'get_server_flag',
    'start_comms',
    'broadcast',
    'register_mediator',
    'shutdown_comms'
]


def get_server_flag():
    return 1


def partie_reception(raw_txt):
    print(f'reception:{raw_txt}')
    # unpack event & transmit to mediators
    parts = raw_txt.split('#')
    evtype = parts[0]
    content = parts[1]  # do not unpack json here!

    print('handle client fait le passage a un/des mediator(s) count:', len(mediators))
    for m in mediators:
        m.post(evtype, content, False)


def start_comms(host_info, port_info):
    raise NotImplementedError


def broadcast(event_type, event_content):
    msg = event_type+'#'+event_content
    # TODO check si pragma fonctionne
    __pragma__('js', '{}', 'sendToClients')(msg)


def register_mediator(x):
    global mediators
    mediators.append(x)

def shutdown_comms():
    pass
