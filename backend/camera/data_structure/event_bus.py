class EventBus:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
            cls._instance._subscribers = {}
        return cls._instance

    def register_event(self, event_name):
        self._subscribers[event_name] = []
    
    def subscribe(self, event_name, callback):
        if event_name not in self._subscribers:
            self.register_event(event_name)
        self._subscribers[event_name].append(callback)

    def emit(self, event_name, *args, **kwargs):
        if event_name in self._subscribers:
            for callback in self._subscribers[event_name]:
                callback(*args, **kwargs)
        else:
            print(f"No subscribers for event: {event_name}")

    def unsubscribe(self, event_name, callback):
        if event_name in self._subscribers:
            self._subscribers[event_name].remove(callback)
