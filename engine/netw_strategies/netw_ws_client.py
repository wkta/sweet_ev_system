import threading
import json
import websocket


__all__ = [
    'get_server_flag',
    'start_comms',
    'broadcast',
    'register_mediator'
]

mediators = list()
inbound_connections = list()
ref_threads = list()

# old?
_client_socket = None
_receiver_thread = None

# ----------- private stuff --------------
def ws_on_message(ws, message):
    ev_manager = EvManager.instance()
    serial = message
    print(f'Received shared variable update: {serial}')
    ev_manager.post(EngineEvTypes.NetwReceive, serial=serial)


def ws_on_error(ws, error):
    print(f"WebSocket error: {error}")


def ws_on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed")


def ws_on_open(ws):
    global client_socket
    client_socket = ws
    print("WebSocket connection opened")


def _receive_updates(host_info, port_info):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        f'ws://{host_info}:{port_info}/',
        on_open=ws_on_open, on_message=ws_on_message, on_error=ws_on_error,
        on_close=ws_on_close
    )
    ws.run_forever()


def get_server_flag():
    return 0


def partie_reception(raw_txt):
    print(f'reception:{raw_txt}')
    # unpack event & transmit to mediators
    parts = raw_txt.split('#')
    evtype = parts[0]
    content = json.loads(parts[1])
    print('handle client fait le passage a un/des mediator(s) count:', len(mediators))
    for m in mediators:
        m.post(evtype, content, False)


def start_comms(host_info, port_info):
    global _receiver_thread
    _receiver_thread = threading.Thread(target=_receive_updates, args=(host_info, port_info))
    _receiver_thread.start()


def broadcast(event_type, event_content):
    global inbound_connections
    # emit to clientS
    richmsg = f'{event_type}#{event_content}'
    global _client_socket
    if _client_socket:
        _client_socket.send(richmsg.encode())


def register_mediator(x):
    global mediators
    mediators.append(x)


def shutdown_comms():
    global _receiver_thread, _client_socket
    if _receiver_thread:
        _receiver_thread.join()
    if client_socket:
        client_socket.close()

# -------------------------------------


#
# class NetwPusher(EvListener):
#     def on_netw_send(self, ev):
#         send_data((ev.evt+'#"'+ev.serial+'"').encode())  # after the sym #: you need to find real json format!!!
#
#     def on_exit_network(self, ev):
#         stop_network()
#
#     def turn_on(self):
#         super().turn_on()
#         start_client()
