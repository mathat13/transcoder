class FakeEventBus:
    def __init__(self):
        self.subscribers = {}
        self.published = []

    def subscribe(self, event_type, handler):
        self.subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event):
        for handler in self.subscribers[type(event)]:
            handler(event)

    def publish_all(self, events):
        for evt in events:
            self.published.append(evt)
            for handler in self.subscribers.get(type(evt), []):
                handler(evt)