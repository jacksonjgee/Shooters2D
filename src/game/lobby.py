import sys

import pygame

from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)


class Lobby:
    def __init__(self):
        self.screen_name = "main"

        self.input_text = ""
        self.input_active = False

        self.message = ""
        self.clipboard_target = None

        self.title_font = pygame.font.Font(
            None,
            72
        )

        self.button_font = pygame.font.Font(
            None,
            34
        )

        self.status_font = pygame.font.Font(
            None,
            28
        )

        self.input_font = pygame.font.Font(
            None,
            24
        )

        self._create_rectangles()
        self._install_clipboard_bridge()

    def _create_rectangles(self):
        centre_x = SCREEN_WIDTH // 2

        button_width = 280
        button_height = 60

        self.host_button = pygame.Rect(
            centre_x - button_width // 2,
            300,
            button_width,
            button_height
        )

        self.join_button = pygame.Rect(
            centre_x - button_width // 2,
            390,
            button_width,
            button_height
        )

        self.code_input_rect = pygame.Rect(
            centre_x - 350,
            300,
            700,
            50
        )

        self.paste_button = pygame.Rect(
            centre_x - 210,
            380,
            190,
            55
        )

        self.submit_button = pygame.Rect(
            centre_x + 20,
            380,
            190,
            55
        )

        self.copy_button = pygame.Rect(
            centre_x - 140,
            380,
            280,
            55
        )

        self.back_button = pygame.Rect(
            centre_x - 100,
            560,
            200,
            50
        )

    def _install_clipboard_bridge(self):
        self.window = None
        self.clipboard_supported = False

        if sys.platform != "emscripten":
            return

        import platform

        self.window = platform.window

        javascript_code = """
        (() => {
            if (window.shootersClipboard) {
                return;
            }

            window.shootersClipboard = {
                status: "idle",
                pastedText: "",
                errorMessage: "",

                async requestPaste() {
                    try {
                        this.status = "reading";
                        this.errorMessage = "";

                        if (!navigator.clipboard) {
                            throw new Error(
                                "Clipboard API unavailable"
                            );
                        }

                        this.pastedText =
                            await navigator.clipboard.readText();

                        this.status = "ready";
                    } catch (error) {
                        this.status = "error";
                        this.errorMessage = String(error);

                        console.error(
                            "Clipboard paste error:",
                            error
                        );
                    }
                },

                async copyText(text) {
                    try {
                        this.status = "writing";
                        this.errorMessage = "";

                        if (!navigator.clipboard) {
                            throw new Error(
                                "Clipboard API unavailable"
                            );
                        }

                        await navigator.clipboard.writeText(
                            text
                        );

                        this.status = "copied";
                    } catch (error) {
                        this.status = "error";
                        this.errorMessage = String(error);

                        console.error(
                            "Clipboard copy error:",
                            error
                        );
                    }
                },

                consumePastedText() {
                    const text = this.pastedText;

                    this.pastedText = "";
                    this.status = "idle";

                    return text;
                },

                clearStatus() {
                    this.status = "idle";
                }
            };
        })();
        """

        self.window.eval(
            javascript_code
        )

        self.clipboard_supported = True

    def handle_event(
        self,
        event,
        network_session
    ):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._handle_mouse_click(
                    mouse_position=event.pos,
                    network_session=network_session
                )

            return

        if event.type == pygame.TEXTINPUT:
            if self.input_active:
                self._add_input_text(
                    event.text
                )

            return

        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_BACKSPACE:
            if self.input_active:
                self.input_text = (
                    self.input_text[:-1]
                )

            return

        paste_shortcut = (
            event.key == pygame.K_v
            and (
                event.mod & pygame.KMOD_CTRL
                or event.mod & pygame.KMOD_META
            )
        )

        if paste_shortcut and self.input_active:
            self._request_paste()
            return

        if event.key in (
            pygame.K_RETURN,
            pygame.K_KP_ENTER
        ):
            self._submit_current_code(
                network_session
            )

    def _handle_mouse_click(
        self,
        mouse_position,
        network_session
    ):
        if self.screen_name == "main":
            if self.host_button.collidepoint(
                mouse_position
            ):
                self._start_host(
                    network_session
                )

            elif self.join_button.collidepoint(
                mouse_position
            ):
                self.screen_name = "joining"
                self.input_text = ""
                self.input_active = True
                self.message = (
                    "Paste the host offer code."
                )

            return

        if self.back_button.collidepoint(
            mouse_position
        ):
            self._return_to_main()
            return

        if self.screen_name == "hosting":
            self._handle_hosting_click(
                mouse_position=mouse_position,
                network_session=network_session
            )

        elif self.screen_name == "joining":
            self._handle_joining_click(
                mouse_position=mouse_position,
                network_session=network_session
            )

    def _handle_hosting_click(
        self,
        mouse_position,
        network_session
    ):
        status = network_session.get_status()

        if status != "offer_ready":
            return

        # Copy the generated host offer.
        if self.copy_button.collidepoint(
            mouse_position
        ):
            self._copy_text(
                network_session.get_offer_code()
            )

            self.message = (
                "Offer copied. Send it to your friend."
            )

            return

        # These rectangles must match where the answer
        # input and buttons are drawn.
        host_input_rect = (
            self.code_input_rect.copy()
        )
        host_input_rect.y = 495

        paste_rect = self.paste_button.copy()
        paste_rect.y = 555

        submit_rect = self.submit_button.copy()
        submit_rect.y = 555

        if host_input_rect.collidepoint(
            mouse_position
        ):
            self.input_active = True
            return

        self.input_active = False

        if paste_rect.collidepoint(
            mouse_position
        ):
            self.input_active = True
            self._request_paste()

        elif submit_rect.collidepoint(
            mouse_position
        ):
            self._accept_answer(
                network_session
            )

    def _handle_joining_click(
        self,
        mouse_position,
        network_session
    ):
        status = network_session.get_status()

        if status == "answer_ready":
            if self.copy_button.collidepoint(
                mouse_position
            ):
                self._copy_text(
                    network_session.get_answer_code()
                )

                self.message = (
                    "Answer copied. Send it to the host."
                )

            return

        if self.code_input_rect.collidepoint(
            mouse_position
        ):
            self.input_active = True

        else:
            self.input_active = False

        if self.paste_button.collidepoint(
            mouse_position
        ):
            self.input_active = True
            self._request_paste()

        elif self.submit_button.collidepoint(
            mouse_position
        ):
            self._start_join(
                network_session
            )

    def _start_host(
        self,
        network_session
    ):
        started = network_session.start_host()

        if not started:
            self.message = (
                "WebRTC could not start."
            )
            return

        self.screen_name = "hosting"
        self.input_text = ""
        self.input_active = False
        self.message = (
            "Creating host offer..."
        )

    def _start_join(
        self,
        network_session
    ):
        offer_code = self.input_text.strip()

        if not offer_code:
            self.message = (
                "Paste an offer code first."
            )
            return

        started = network_session.start_join(
            offer_code
        )

        if started:
            self.input_active = False
            self.message = (
                "Creating answer..."
            )
        else:
            self.message = (
                "Could not create answer."
            )

    def _accept_answer(
        self,
        network_session
    ):
        answer_code = self.input_text.strip()

        if not answer_code:
            self.message = (
                "Paste the answer code first."
            )
            return

        accepted = network_session.accept_answer(
            answer_code
        )

        if accepted:
            self.input_active = False
            self.message = (
                "Connecting..."
            )
        else:
            self.message = (
                "Could not accept answer."
            )

    def _submit_current_code(
        self,
        network_session
    ):
        if not self.input_active:
            return

        if self.screen_name == "joining":
            self._start_join(
                network_session
            )

        elif self.screen_name == "hosting":
            self._accept_answer(
                network_session
            )

    def _return_to_main(self):
        self.screen_name = "main"
        self.input_text = ""
        self.input_active = False
        self.message = ""

    def _add_input_text(
        self,
        text
    ):
        maximum_length = 10000

        remaining_length = (
            maximum_length
            - len(self.input_text)
        )

        if remaining_length <= 0:
            return

        self.input_text += text[
            :remaining_length
        ]

    def _request_paste(self):
        if not self.clipboard_supported:
            self.message = (
                "Clipboard paste is unavailable."
            )
            return

        self.window.shootersClipboard.requestPaste()

        self.message = (
            "Reading clipboard..."
        )

    def _copy_text(self, text):
        if not text:
            self.message = (
                "There is no code to copy."
            )
            return

        if not self.clipboard_supported:
            self.message = (
                "Clipboard copy is unavailable."
            )
            return

        self.window.shootersClipboard.copyText(
            text
        )

    def update(self, network_session):
        self._update_clipboard()

        status = network_session.get_status()

        if status == "error":
            self.message = (
                network_session.last_error
                or "Connection error."
            )

        elif status == "offer_ready":
            if self.screen_name == "hosting":
                if not self.input_active:
                    self.message = (
                        "Copy the offer and send it "
                        "to your friend."
                    )

        elif status == "answer_ready":
            if self.screen_name == "joining":
                self.message = (
                    "Copy the answer and send it "
                    "back to the host."
                )

        elif status == "connecting":
            self.message = (
                "Waiting for connection..."
            )

        if network_session.is_connected():
            return "playing"

        return "lobby"

    def _update_clipboard(self):
        if not self.clipboard_supported:
            return

        status = str(
            self.window.shootersClipboard.status
        )

        if status == "ready":
            pasted_text = str(
                self.window.shootersClipboard
                    .consumePastedText()
            )

            self.input_text = (
                pasted_text.strip()
            )

            self.message = (
                "Code pasted."
            )

        elif status == "copied":
            self.window.shootersClipboard.clearStatus()

        elif status == "error":
            error_message = str(
                self.window.shootersClipboard
                    .errorMessage
            )

            self.message = (
                f"Clipboard error: {error_message}"
            )

            self.window.shootersClipboard.clearStatus()

    def draw(
        self,
        screen,
        network_session
    ):
        screen.fill(
            (25, 25, 30)
        )

        if self.screen_name == "main":
            self._draw_main_screen(
                screen
            )

        elif self.screen_name == "hosting":
            self._draw_host_screen(
                screen=screen,
                network_session=network_session
            )

        elif self.screen_name == "joining":
            self._draw_join_screen(
                screen=screen,
                network_session=network_session
            )

    def _draw_main_screen(self, screen):
        self._draw_title(
            screen
        )

        self._draw_button(
            screen=screen,
            rect=self.host_button,
            text="Host Game"
        )

        self._draw_button(
            screen=screen,
            rect=self.join_button,
            text="Join Game"
        )

    def _draw_host_screen(
        self,
        screen,
        network_session
    ):
        self._draw_title(
            screen
        )

        status = network_session.get_status()

        self._draw_status(
            screen,
            status
        )

        if status == "offer_ready":
            self._draw_code_preview(
                screen=screen,
                code=network_session.get_offer_code(),
                y_position=300,
                label="Host offer created"
            )

            self._draw_button(
                screen=screen,
                rect=self.copy_button,
                text="Copy Host Offer"
            )

            instruction = (
                "After your friend sends back an "
                "answer, paste it below."
            )

            self._draw_instruction(
                screen=screen,
                text=instruction,
                y_position=465
            )

            self._draw_input_box(
                screen,
                y_override=495
            )

            paste_rect = self.paste_button.copy()
            submit_rect = self.submit_button.copy()

            paste_rect.y = 555
            submit_rect.y = 555

            self._draw_button(
                screen=screen,
                rect=paste_rect,
                text="Paste Answer"
            )

            self._draw_button(
                screen=screen,
                rect=submit_rect,
                text="Accept Answer"
            )

        else:
            self._draw_instruction(
                screen=screen,
                text=self.message,
                y_position=340
            )

        self._draw_message(
            screen
        )

    def _draw_join_screen(
        self,
        screen,
        network_session
    ):
        self._draw_title(
            screen
        )

        status = network_session.get_status()

        self._draw_status(
            screen,
            status
        )

        if status == "answer_ready":
            self._draw_code_preview(
                screen=screen,
                code=network_session.get_answer_code(),
                y_position=300,
                label="Answer created"
            )

            self._draw_button(
                screen=screen,
                rect=self.copy_button,
                text="Copy Answer"
            )

        else:
            self._draw_instruction(
                screen=screen,
                text="Paste the host offer code:",
                y_position=260
            )

            self._draw_input_box(
                screen
            )

            self._draw_button(
                screen=screen,
                rect=self.paste_button,
                text="Paste Offer"
            )

            self._draw_button(
                screen=screen,
                rect=self.submit_button,
                text="Create Answer"
            )

        self._draw_message(
            screen
        )

        self._draw_button(
            screen=screen,
            rect=self.back_button,
            text="Back"
        )

    def _draw_title(self, screen):
        title = self.title_font.render(
            "Shooters 2D",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                110
            )
        )

        screen.blit(
            title,
            title_rect
        )

    def _draw_status(
        self,
        screen,
        status
    ):
        status_surface = self.status_font.render(
            f"Status: {status}",
            True,
            (210, 210, 210)
        )

        status_rect = status_surface.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                190
            )
        )

        screen.blit(
            status_surface,
            status_rect
        )

    def _draw_instruction(
        self,
        screen,
        text,
        y_position
    ):
        surface = self.status_font.render(
            text,
            True,
            (220, 220, 220)
        )

        rect = surface.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                y_position
            )
        )

        screen.blit(
            surface,
            rect
        )

    def _draw_input_box(
        self,
        screen,
        y_override=None
    ):
        input_rect = self.code_input_rect.copy()

        if y_override is not None:
            input_rect.y = y_override

        border_colour = (
            (120, 170, 255)
            if self.input_active
            else (190, 190, 190)
        )

        pygame.draw.rect(
            screen,
            (35, 35, 42),
            input_rect,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            border_colour,
            input_rect,
            2,
            border_radius=6
        )

        if self.input_text:
            visible_text = (
                self.input_text[:38]
            )

            if len(self.input_text) > 38:
                visible_text += "..."

        else:
            visible_text = (
                "Click here, type, or paste code"
            )

        text_surface = self.input_font.render(
            visible_text,
            True,
            (235, 235, 235)
        )

        screen.blit(
            text_surface,
            (
                input_rect.x + 12,
                input_rect.centery
                - text_surface.get_height() // 2
            )
        )

    def _draw_code_preview(
        self,
        screen,
        code,
        y_position,
        label
    ):
        label_surface = self.status_font.render(
            label,
            True,
            (230, 230, 230)
        )

        label_rect = label_surface.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                y_position
            )
        )

        screen.blit(
            label_surface,
            label_rect
        )

        preview = code[:50]

        if len(code) > 50:
            preview += "..."

        preview_surface = self.input_font.render(
            preview,
            True,
            (170, 190, 220)
        )

        preview_rect = preview_surface.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                y_position + 40
            )
        )

        screen.blit(
            preview_surface,
            preview_rect
        )

    def _draw_message(self, screen):
        if not self.message:
            return

        surface = self.status_font.render(
            self.message,
            True,
            (190, 210, 190)
        )

        rect = surface.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 45
            )
        )

        screen.blit(
            surface,
            rect
        )

    def _draw_button(
        self,
        screen,
        rect,
        text
    ):
        mouse_position = pygame.mouse.get_pos()

        if rect.collidepoint(mouse_position):
            colour = (95, 105, 125)
        else:
            colour = (70, 80, 100)

        pygame.draw.rect(
            screen,
            colour,
            rect,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            rect,
            2,
            border_radius=8
        )

        label = self.button_font.render(
            text,
            True,
            (255, 255, 255)
        )

        label_rect = label.get_rect(
            center=rect.center
        )

        screen.blit(
            label,
            label_rect
        )