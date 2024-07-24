import json
import socket
import threading


class NetworkLayer:
    def __init__(self):
        self._mediators = []

        self.client_socket = None
        self.receiver_thread = None
        self.start_client(self._mediators)

    def register_mediator(self, mediator):
        self._mediators.append(mediator)

    # in the simulation we use :
    def broadcast(self, event_type, event, target_mtype):
        if event_type == 'netw_exit':
            self.stop_network()
            return
        if target_mtype == 1:  # to server
            json_str = json.dumps(event)
            serial = f'{event_type}#{json_str}'
            self.send_rawtext(serial)
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


    def receive_updates(self, clisocket, li_media):
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

    def start_client(self, li_mediators):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1', 60111))
        receiver_thread = threading.Thread(target=self.receive_updates, args=(self.client_socket, li_mediators))
        receiver_thread.start()

    def stop_network(self):
        if self.receiver_thread:
            self.receiver_thread.join()
        if self.client_socket:
            self.client_socket.close()

    def send_rawtext(self, x):
        self.client_socket.sendall(x.encode())
        print('NetworkLayer transmet sur socket....',x)


class NetworkLayer2:
    def __init__(self):
        self.gl_state = None
        self.mediators = []

        self.connections = list()
        self.thr = list()
        self.compteur = 0

    def _broadcast_cross_msg(self, data: str):
        broken_c = set()

        for client in self.connections:
            try:
                client.sendall(data.encode())
            except Exception as err:
                print('!!connection err!!', err)
                broken_c.add(client)

        for c in broken_c:
            self.connections.remove(c)
            print(' A connexion has just dropped')

    def handle_client(self, socklisten):
        conn, addr = socklisten.accept()  # blocking call
        self.connections.append(conn)
        with conn:
            print(f'Connection added, source:{addr}')
            # conn.send('hello'.encode())
            while True:
                data = conn.recv(1024)
                if not data:
                    print('error receiving data')
                    break
                txt_info = data.decode()
                print(f'reception:{txt_info}')

                # unpack event & transmit to mediators
                parts = txt_info.split('#')
                evtype = parts[0]
                content = json.loads(parts[1])
                print('handle client fait le passage a un/des mediator(s) count:', len(self.mediators))
                for m in self.mediators:
                    m.post(evtype, content, False)

    def start_comms(self, given_socket_config):
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so.bind(given_socket_config)
        so.listen()
        hostinfo, portinfo = given_socket_config
        print(f'Server ready! Config: {hostinfo}:{portinfo}...')
        print('mediators:', self.mediators)

        # ---------BUG incompréhensible!! J'ai besoin de 2 connexions pr que le client fonctionne bien-------
        for _ in range(2):
            given_thread = threading.Thread(target=self.handle_client, args=(so,))
            given_thread.start()

    def _shutdown_server(self):
        for connection in self.connections:
            connection.close()
        self.thr.join()

    def register_mediator(self, mediator):
        self.mediators.append(mediator)

    # in the simulation we use :
    def broadcast(self, event_type, event, target_mtype):
        if event_type == 'netw_exit':
            self._shutdown_server()
            return
        if target_mtype == 0:  # to clients
            self._broadcast_cross_msg(
                event_type+'#'+event
            )
            return
        raise ValueError

        # target_mtype : who we target 1 to target the server
        #for a_mediator in self._mediators:
        #    if a_mediator.server_side_flag() == target_mtype:
        #        a_mediator.post(event_type, event, enable_event_forwarding=False)
