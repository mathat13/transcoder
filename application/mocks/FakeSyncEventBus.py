class FakeSyncEventBus:
    def __init__(self):
        self.subscribers = {}
        self.published = []

    def subscribe(self, event_type, handler):
        self.subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event):
        if not self.subscribers:
            return

        self.published.append(event)
        for handler in self.subscribers[type(event)]:
            handler(event)

    def publish_all(self, events):
        for evt in events:
            self.publish(evt)