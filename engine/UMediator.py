import random
from collections import deque


class UMediator:
    def __init__(self, is_server: bool, networklayer):
        self.ident = self.gen_id()
        self.listeners = {}
        self.event_queue = deque()
        self._server_flag = 0 if (not is_server) else 1

        self.network_layer = networklayer
        networklayer.register_mediator(self)

    @staticmethod
    def gen_id():
        omega = [chr(c) for c in range(ord('a'), ord('z') + 1)] + [str(e) for e in range(0, 10)]
        lst = [random.choice(omega) for _ in range(12)]
        return "".join(lst)

    def register(self, event_type, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def unregister(self, event_type, listener):
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)
            if not self.listeners[event_type]:
                del self.listeners[event_type]

    @staticmethod
    def is_special_event(event_type):
        return event_type.startswith('cross_')

    def _basic_notify(self, event_type, event):
        if event_type in self.listeners:
            for listener_cb in self.listeners[event_type]:
                listener_cb(event)

    def post(self, event_type, event, enable_event_forwarding=True):
        print(f'  postage event [{event_type}, {event}] sur Mediator:', self.ident)
        self.event_queue.append((event_type, event, enable_event_forwarding))

    def update(self) -> int:
        y = cpt = len(self.event_queue)
        while cpt > 0:
            event_type, event, enable_event_forwarding = self.event_queue.popleft()
            if self.is_special_event(event_type) and enable_event_forwarding:
                self.handle_special_event(event_type, event)
            else:
                self._basic_notify(event_type, event)
            cpt -= 1
        return y

    def server_side_flag(self) -> int:
        return self._server_flag

    def handle_special_event(self, event_type, event):
        suffix = " by server" if self._server_flag else "by client"+self.ident
        print(f"Special event [{event_type}, {event}] forwarded"+suffix)

        target_hint = self._server_flag ^ 1  # flip the flag
        self.network_layer.broadcast(event_type, event, target_hint)
