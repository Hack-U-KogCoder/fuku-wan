from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Button


class AutoReplyScreen(Screen):
    CSS_PATH = "common.tcss"
    TITLE = "HackU - auto reply"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Button("mode", id="btn-ModeChange")


def handleButtonAutoReply(app, event) -> bool:
    match event.button.id:
        case None:
            pass
        case "btn-ModeChange":
            app.switch_mode("mode_change")
        case _:
            return False
    return True
