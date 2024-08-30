from dataclasses import dataclass
import re
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Label, Static
from .widgets import AlwaysInput
from textual.timer import Timer
from textual.binding import Binding
from .input_table import TABLE_EN, TABLE_JP, InputTable, InputTableGroup
from lib.tts import talk_text

inputTables = InputTableGroup(tables=[InputTable(TABLE_JP), InputTable(TABLE_EN)])


class Keyboard(Static):
    """Display a greeting."""

    def compose(self) -> ComposeResult:
        tb = inputTables.table(0)
        yield Button("←", id="btn-Left")
        yield Button("▶", id="btn-Play")
        yield Button("→", id="btn-Right")
        for i in range(tb.rows):
            yield Button(tb.char(i, 0), id=f"btn-{i}")
        yield Button("全削除", id="btn-Clear", variant="error")
        yield Button("削除", id="btn-Bs", variant="warning")
        yield Button("モード選択", id="btn-Mode", variant="success")


DnTable = {
    "Left": "0",
    "Play": "1",
    "Right": "2",
    "9": "Clear",
    "10": "Bs",
    "11": "Mode",
}

UpTable = {v: k for k, v in DnTable.items()}


@dataclass
class KeyboardStatus:
    timer: Timer | None = None
    selBtnId: int = 0
    idxChar: int = 0
    mode: int = 0


class ManualInputScreen(Screen):
    CSS_PATH = "common.tcss"
    TITLE = "ふくワン"

    BINDINGS = [
        Binding("ctrl+k", "cursor_up", "cursor up"),
        Binding("ctrl+j", "cursor_down", "cursor down"),
        Binding("ctrl+l", "cursor_next", "cursor next"),
    ]

    keyboardStatus = KeyboardStatus()
    word = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("気持ちを伝えるワン!", id="question")
        yield AlwaysInput(id="input")
        yield Keyboard(id="keyboard")

    def action_cursor_up(self) -> None:
        if self.focused is not None and self.focused.id is not None:
            if self.focused.id == "input":
                pass
            else:
                btn_id = self.focused.id.split("-")[1]

                if btn_id in UpTable:
                    target = self.query_one("#btn-" + UpTable[btn_id])
                else:
                    if not btn_id.isdecimal():
                        return
                    target_id = str(int(btn_id) - 3)
                    target = self.query_one("#btn-" + target_id)
            target.focus()

    def action_cursor_down(self) -> None:
        if self.focused is not None and self.focused.id is not None:
            if self.focused.id == "input":
                target = self.query_one("#btn-Play")
            else:
                btn_id = self.focused.id.split("-")[1]

                if btn_id in DnTable:
                    target = self.query_one("#btn-" + DnTable[btn_id])
                else:
                    if not btn_id.isdecimal():
                        return
                    target_id = str(int(btn_id) + 3)
                    target = self.query_one("#btn-" + target_id)
            target.focus()

    def action_cursor_next(self) -> None:
        self.focus_next()


def handleButtonManualInput(app, event) -> bool:
    """
    True: mach exists. False: not exists
    """
    sta = app.keyboardStatus
    btn = event.button
    input = app.query_one("#input", AlwaysInput)
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
                btn0 = app.query_one(f"#btn-{sta.selBtnId}", Button)
                submit(btn0)
                new()
            sta.timer = app.set_timer(1.2, submit, name="keyTimer")

        case "btn-Left":
            input.action_cursor_left()
        case "btn-Right":
            input.action_cursor_right()
        case "btn-Play":
            talk_text(input.value)
            input.clear()

        case "btn-Clear":
            input.clear()
        case "btn-Bs":
            input.action_delete_left()
        case "btn-Mode":
            app.switch_mode("mode_change")
        case _:
            return False
    return True
