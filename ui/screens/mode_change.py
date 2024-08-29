from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header


class ModeChangeScreen(Screen):
    CSS_PATH = "common.tcss"
    TITLE = "HackU - mode change"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
