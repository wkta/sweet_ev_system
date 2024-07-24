import glvars
from engine.UMediator import UMediator


class EventReadyCls:
    def __init__(self):
        super().__init__()
        self._mediator = glvars.mediator

    def pev(self, event_type, event=None, enable_event_forwarding=True):
        self._mediator.post(event_type, event, enable_event_forwarding)
