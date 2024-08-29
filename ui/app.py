import re
from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Button
from .screens.widgets import AlwaysInput
from textual.binding import Binding
from lib.tts import talk_text

from .screens import ManualInputScreen, KeyboardStatus, inputTables
from .screens import ModeChangeScreen


class MainApp(App[str]):

    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit", show=False, priority=True),
    ]

    MODES = {"manual_input": ManualInputScreen, "mode_change": ModeChangeScreen}

    keyboardStatus = KeyboardStatus()
    word = ""

    def on_mount(self) -> None:
        self.switch_mode("manual_input")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        sta = self.keyboardStatus
        btn = event.button
        input = self.query_one("#input", AlwaysInput)
        table = inputTables.table(sta.mode)

        def submit(btn0=btn) -> None:
            sta.timer = None
            btn0.variant = "default"

        def new():
            sta.selBtnId = btn_id
            sta.idxChar = 0
            input.insert_text_at_cursor(table.char(sta.selBtnId, sta.idxChar))
            event.button.variant = "primary"

        def next():
            sta.timer.stop()
            sta.idxChar = (sta.idxChar + 1) % table.cols[sta.selBtnId]
            input.action_delete_left()
            input.insert_text_at_cursor(table.char(sta.selBtnId, sta.idxChar))

        match btn.id:
            case None:
                pass
            case a if re.search(r"btn-\d+", a):
                btn_id = int(btn.id.split("-")[1])
                if sta.timer is None:
                    new()
                elif btn_id == sta.selBtnId:
                    next()
                else:
                    sta.timer.stop()
                    btn0 = self.query_one(f"#btn-{sta.selBtnId}", Button)
                    submit(btn0)
                    new()
                sta.timer = self.set_timer(1.2, submit, name="keyTimer")

            case "btn-Left":
                input.action_cursor_left()
            case "btn-Right":
                input.action_cursor_right()
            case "btn-Play":
                talk_text(input.value)
                input.clear()

            case "btn-Exit":
                self.exit()
            case "btn-Bs":
                input.action_delete_left()
            case "btn-Mode":
                self.switch_mode("mode_change")
            case _:
                wid = self.query_one("#in01").query_one(AlwaysInput)
                wid.value = str(event.button.id)
