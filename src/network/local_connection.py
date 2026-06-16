class LocalConnection:
    def __init__(self):
        self.host_inbox = []
        self.client_inbox = []

    def send_to_host(self, message_json):
        self.host_inbox.append(message_json)

    def send_to_client(self, message_json):
        self.client_inbox.append(message_json)

    def receive_for_host(self):
        messages = self.host_inbox.copy()
        self.host_inbox.clear()
        return messages

    def receive_for_client(self):
        messages = self.client_inbox.copy()
        self.client_inbox.clear()
        return messages