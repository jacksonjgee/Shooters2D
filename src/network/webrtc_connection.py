import sys


class WebRTCConnection:
    def __init__(self):
        self.is_browser = (
            sys.platform == "emscripten"
        )

        self.is_supported = False
        self.window = None

        if not self.is_browser:
            return

        import platform

        self.window = platform.window

        self._install_javascript_bridge()

        self.is_supported = bool(
            self.window.shootersRTC.isSupported
        )

        self.window.console.log(
            "Shooters2D WebRTC bridge installed",
            self.is_supported
        )

    def _install_javascript_bridge(self):
        javascript_code = """
        (() => {
            if (window.shootersRTC) {
                return;
            }

            window.shootersRTC = {
                isSupported:
                    typeof RTCPeerConnection !== "undefined",

                peerConnection: null,
                dataChannel: null,

                role: null,
                status: "idle",

                offerCode: "",
                answerCode: "",
                errorMessage: "",

                receivedMessages: [],

                waitForIceGathering(peerConnection) {
                    return new Promise((resolve) => {
                        if (
                            peerConnection.iceGatheringState
                            === "complete"
                        ) {
                            resolve();
                            return;
                        }

                        const handleStateChange = () => {
                            if (
                                peerConnection.iceGatheringState
                                === "complete"
                            ) {
                                peerConnection.removeEventListener(
                                    "icegatheringstatechange",
                                    handleStateChange
                                );

                                resolve();
                            }
                        };

                        peerConnection.addEventListener(
                            "icegatheringstatechange",
                            handleStateChange
                        );
                    });
                },

                configureDataChannel(channel) {
                    this.dataChannel = channel;

                    channel.onopen = () => {
                        this.status = "connected";

                        console.log(
                            "WebRTC data channel connected"
                        );
                    };

                    channel.onclose = () => {
                        this.status = "closed";

                        console.log(
                            "WebRTC data channel closed"
                        );
                    };

                    channel.onerror = (error) => {
                        this.status = "error";
                        this.errorMessage =
                            "Data channel error";

                        console.error(
                            "WebRTC data channel error:",
                            error
                        );
                    };

                    channel.onmessage = (event) => {
                        this.receivedMessages.push(
                            event.data
                        );
                    };
                },

                resetConnection() {
                    if (this.dataChannel) {
                        this.dataChannel.close();
                    }

                    if (this.peerConnection) {
                        this.peerConnection.close();
                    }

                    this.peerConnection = null;
                    this.dataChannel = null;

                    this.role = null;
                    this.status = "idle";

                    this.offerCode = "";
                    this.answerCode = "";
                    this.errorMessage = "";

                    this.receivedMessages = [];
                },

                async startHost() {
                    try {
                        this.resetConnection();

                        this.role = "host";
                        this.status = "creating_offer";

                        this.peerConnection =
                            new RTCPeerConnection();

                        const channel =
                            this.peerConnection.createDataChannel(
                                "game",
                                {
                                    ordered: true
                                }
                            );

                        this.configureDataChannel(
                            channel
                        );

                        const offer =
                            await this.peerConnection.createOffer();

                        await this.peerConnection
                            .setLocalDescription(
                                offer
                            );

                        await this.waitForIceGathering(
                            this.peerConnection
                        );

                        const description = {
                            type:
                                this.peerConnection
                                    .localDescription.type,

                            sdp:
                                this.peerConnection
                                    .localDescription.sdp
                        };

                        this.offerCode = btoa(
                            JSON.stringify(description)
                        );

                        this.status = "offer_ready";

                        console.log(
                            "WebRTC host offer ready"
                        );
                    } catch (error) {
                        this.status = "error";
                        this.errorMessage = String(error);

                        console.error(
                            "WebRTC host error:",
                            error
                        );
                    }
                },

                async startJoin(offerCode) {
                    try {
                        this.resetConnection();

                        this.role = "client";
                        this.status = "creating_answer";

                        const offerDescription = JSON.parse(
                            atob(offerCode)
                        );

                        this.peerConnection =
                            new RTCPeerConnection();

                        this.peerConnection.ondatachannel = (
                            event
                        ) => {
                            this.configureDataChannel(
                                event.channel
                            );
                        };

                        await this.peerConnection
                            .setRemoteDescription(
                                offerDescription
                            );

                        const answer =
                            await this.peerConnection
                                .createAnswer();

                        await this.peerConnection
                            .setLocalDescription(
                                answer
                            );

                        await this.waitForIceGathering(
                            this.peerConnection
                        );

                        const description = {
                            type:
                                this.peerConnection
                                    .localDescription.type,

                            sdp:
                                this.peerConnection
                                    .localDescription.sdp
                        };

                        this.answerCode = btoa(
                            JSON.stringify(description)
                        );

                        this.status = "answer_ready";

                        console.log(
                            "WebRTC answer ready"
                        );
                    } catch (error) {
                        this.status = "error";
                        this.errorMessage = String(error);

                        console.error(
                            "WebRTC join error:",
                            error
                        );
                    }
                },

                async acceptAnswer(answerCode) {
                    try {
                        this.status = "accepting_answer";
                        this.errorMessage = "";

                        if (!this.peerConnection) {
                            throw new Error(
                                "Host peer connection does not exist"
                            );
                        }

                        const answerDescription = JSON.parse(
                            atob(answerCode)
                        );

                        await this.peerConnection
                            .setRemoteDescription(
                                answerDescription
                            );

                        this.status = "connecting";

                        console.log(
                            "WebRTC host accepted answer"
                        );
                    } catch (error) {
                        this.status = "error";
                        this.errorMessage = String(error);

                        console.error(
                            "WebRTC accept-answer error:",
                            error
                        );
                    }
                },

                send(message) {
                    if (!this.dataChannel) {
                        return false;
                    }

                    if (
                        this.dataChannel.readyState
                        !== "open"
                    ) {
                        return false;
                    }

                    this.dataChannel.send(
                        message
                    );

                    return true;
                },

                receiveAll() {
                    const messages =
                        this.receivedMessages.slice();

                    this.receivedMessages = [];

                    return JSON.stringify(
                        messages
                    );
                }
            };
        })();
        """

        self.window.eval(
            javascript_code
        )

    def start_host(self):
        if not self.is_supported:
            return False

        self.window.shootersRTC.startHost()

        return True

    def start_join(self, offer_code):
        if not self.is_supported:
            return False

        if not offer_code:
            return False

        self.window.shootersRTC.startJoin(
            offer_code
        )

        return True

    def accept_answer(self, answer_code):
        if not self.is_supported:
            return False

        if not answer_code:
            return False

        self.window.shootersRTC.acceptAnswer(
            answer_code
        )

        return True

    def send(self, message):
        if not self.is_supported:
            return False

        if not message:
            return False

        return bool(
            self.window.shootersRTC.send(
                message
            )
        )

    def receive_all(self):
        if not self.is_supported:
            return []

        import json

        messages_json = str(
            self.window.shootersRTC.receiveAll()
        )

        return json.loads(
            messages_json
        )

    def reset(self):
        if not self.is_supported:
            return

        self.window.shootersRTC.resetConnection()

    def get_role(self):
        if not self.is_supported:
            return None

        role = self.window.shootersRTC.role

        if role is None:
            return None

        return str(role)

    def get_status(self):
        if not self.is_supported:
            return "unsupported"

        return str(
            self.window.shootersRTC.status
        )

    def get_offer_code(self):
        if not self.is_supported:
            return ""

        return str(
            self.window.shootersRTC.offerCode
        )

    def get_answer_code(self):
        if not self.is_supported:
            return ""

        return str(
            self.window.shootersRTC.answerCode
        )

    def get_error_message(self):
        if not self.is_supported:
            return "WebRTC is unavailable"

        return str(
            self.window.shootersRTC.errorMessage
        )

    def is_connected(self):
        return (
            self.get_status() == "connected"
        )