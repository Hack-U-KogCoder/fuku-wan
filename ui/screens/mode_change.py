from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Button


class ModeChangeScreen(Screen):
    CSS_PATH = "common.tcss"
    TITLE = "HackU - mode change"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Button("マニュアル", id="btn-ManualMode")
        yield Button("AI応答", id="btn-AutoReplyMode")
        yield Button("終了", id="btn-Exit", variant="error")


def handleButtonModeChange(app, event) -> bool:
    match event.button.id:
        case None:
            pass
        case "btn-ManualMode":
            app.switch_mode("manual_input")
        case "btn-AutoReplyMode":
            app.switch_mode("auto_reply")
        case "btn-Exit":
            app.exit()
        case _:
            return False
    return True
