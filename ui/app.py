import re
from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Button
from .screens.widgets import AlwaysInput
from textual.binding import Binding
from lib.tts import talk_text

from .screens import (
    ManualInputScreen,
    KeyboardStatus,
    inputTables,
    AutoReplyScreen,
    handleButtonAutoReply,
    handleButtonManualInput,
    ModeChangeScreen,
    handleButtonModeChange,
    DemoScreen,
    handleButtonDemo,
)
from .screens import ModeChangeScreen


class MainApp(App[str]):

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
        Binding("ctrl+g", "mode_change", "mode change", show=False),
    ]

    MODES = {
        "manual_input": ManualInputScreen,
        "mode_change": ModeChangeScreen,
        "auto_reply": AutoReplyScreen,
        "demo": DemoScreen,
    }

    keyboardStatus = KeyboardStatus()
    word = ""

    def on_mount(self) -> None:
        self.switch_mode("manual_input")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        sta = self.keyboardStatus
        btn = event.button

        ret = False
        match self.current_mode:
            case None:
                pass
            case "mode_change":
                ret = handleButtonModeChange(self, event)
            case "manual_input":
                ret = handleButtonManualInput(self, event)
            case "auto_reply":
                ret = handleButtonAutoReply(self, event)
            case "demo":
                ret = handleButtonDemo(self, event)

        if ret:
            return

        match btn.id:
            case None:
                pass
            case _:
                self.exit(f"no handle button{btn.id}")

    def action_mode_change(self):
        self.switch_mode("mode_change")
