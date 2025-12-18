class FakeLogger:
    def __init__(self):
        self.messages = []
        self.errors = []

    def publish_message(self, message: str) -> bool:
        self.messages.append(message)
        return True

    def publish_error(self, message: str) -> bool:
        self.errors.append(message)
        return True