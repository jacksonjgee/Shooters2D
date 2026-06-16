class NetworkSession:
    def __init__(self, connection):
        self.connection = connection

        self.offer_printed = False
        self.last_error = None

    def start_host(self):
        started = self.connection.start_host()

        if started:
            self.offer_printed = False

        return started

    def update(self):
        status = self.connection.get_status()

        if status == "error":
            self.last_error = (
                self.connection.get_error_message()
            )

            self.connection.window.console.error(
                "WebRTC error:",
                self.last_error
            )

            return

        if (
            status == "offer_ready"
            and not self.offer_printed
        ):
            offer_code = (
                self.connection.get_offer_code()
            )

            self.connection.window.console.log(
                "Host offer code:",
                offer_code
            )

            self.offer_printed = True

    def get_status(self):
        return self.connection.get_status()

    def get_role(self):
        return self.connection.get_role()

    def is_connected(self):
        return self.connection.is_connected()

    def get_offer_code(self):
        return self.connection.get_offer_code()

    def get_answer_code(self):
        return self.connection.get_answer_code()

    def start_join(self, offer_code):
        return self.connection.start_join(
            offer_code
        )

    def accept_answer(self, answer_code):
        return self.connection.accept_answer(
            answer_code
        )