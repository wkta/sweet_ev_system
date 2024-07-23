import json
import socket
import threading


gl_state = None  # GameModel()
mediators = []


class NetworkLayer2:
    def __init__(self):
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
        global mediators
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
                print('handle client fait le passage a un/des mediator(s) count:', len(mediators))
                for m in mediators:
                    m.post(evtype, content, False)

    def start_comms(self, given_socket_config):
        global mediators
        so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        so.bind(given_socket_config)
        so.listen()
        hostinfo, portinfo = given_socket_config
        print(f'Server ready! Config: {hostinfo}:{portinfo}...')
        print('mediators:', mediators)

        # ---------BUG incompréhensible!! J'ai besoin de 2 connexions pr que le client fonctionne bien-------
        for _ in range(2):
            given_thread = threading.Thread(target=self.handle_client, args=(so,))
            given_thread.start()

    def _shutdown_server(self):
        for connection in self.connections:
            connection.close()
        self.thr.join()

    def register_mediator(self, mediator):
        global mediators
        mediators.append(mediator)

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
