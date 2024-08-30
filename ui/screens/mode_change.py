from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Button
from textual.binding import Binding


class ModeChangeScreen(Screen):
    CSS_PATH = "common.tcss"
    TITLE = "ふくワン - モード選択"

    BINDINGS = [
        Binding("ctrl+k", "cursor_up", "cursor up"),
        Binding("ctrl+j", "cursor_down", "cursor down"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Button("マニュアル", id="btn-ManualMode", variant="primary")
        yield Button("AI応答", id="btn-AutoReplyMode", variant="success")

    def action_cursor_up(self) -> None:
        self.focus_previous()

    def action_cursor_down(self) -> None:
        self.focus_next()


def handleButtonModeChange(app, event) -> bool:
    match event.button.id:
        case None:
            pass
        case "btn-ManualMode":
            app.switch_mode("manual_input")
        case "btn-AutoReplyMode":
            app.switch_mode("auto_reply")
        case _:
            return False
    return True
