import json
import socket
import threading

# from core.events import EngineEvTypes, EvManager, EvListener


client_socket = None
receiver_thread = None


def receive_updates(clisocket, li_media):
    global nlayer_obj
    # ev_manager = EvManager.instance()
    while True:
        data = clisocket.recv(1024)
        if not data:
            break
        msg_payload = data.decode()
        print(' client recoit update:', msg_payload)

        print(len(li_media))
        parts = msg_payload.split('#')
        evtype = parts[0]
        evcontent = parts[1]

        for mee in li_media:
            mee.post(evtype, evcontent, False)


def start_client(li_mediators):
    global client_socket, receiver_thread
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 60111))
    receiver_thread = threading.Thread(target=receive_updates, args=(client_socket, li_mediators))
    receiver_thread.start()


class NetworkLayer:
    def __init__(self):
        self._mediators = []
        start_client(self._mediators)

    def register_mediator(self, mediator):
        self._mediators.append(mediator)

    # in the simulation we use :
    def broadcast(self, event_type, event, target_mtype):
        if event_type == 'netw_exit':
            stop_network()
            return
        if target_mtype == 1:  # to server
            json_str = json.dumps(event)
            serial = f'{event_type}#{json_str}'
            send_rawtext(serial)
            return
        raise ValueError

        # target_mtype : who we target 1 to target the server
        #for a_mediator in self._mediators:
        #    if a_mediator.server_side_flag() == target_mtype:
        #        a_mediator.post(event_type, event, enable_event_forwarding=False)

    # def send_special_event(self, event_type, event, source_mediator):
    #     message = process_data(event_type, event)
    #     # Call JavaScript function to send data
    #     print('netw layer pushing::', message)
    #     __pragma__('js', '{}', 'sendToClients')(message)
    #
    # def inject_packed_ev(self, serialized_event):
    #     tmp = serialized_event.split('#')
    #     evtype = tmp[0]
    #     evcontent = json_loads(tmp[1])
    #     for m in self.mediators:
    #         m.post(evtype, evcontent, False)


def stop_network():
    global receiver_thread, client_socket
    if receiver_thread:
        receiver_thread.join()
    if client_socket:
        client_socket.close()


def send_rawtext(x):
    global client_socket
    client_socket.sendall(x.encode())
    print('NetworkLayer transmet sur socket....',x)
