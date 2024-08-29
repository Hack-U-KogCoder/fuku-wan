from dataclasses import dataclass
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Header, Footer, Label, Static
from .widgets import AlwaysInput
from textual.timer import Timer
from textual.binding import Binding
from .input_table import TABLE_EN, TABLE_JP, InputTable, InputTableGroup

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
        yield Button("exit", id="btn-Exit")
        yield Button("BS", id="btn-Bs")
        yield Button("mode", id="btn-Mode")


DnTable = {
    "Left": "0",
    "Play": "1",
    "Right": "2",
    "9": "Exit",
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
    TITLE = "HackU"

    BINDINGS = [
        Binding("ctrl+k", "cursor_up", "cursor up", show=True),
        Binding("ctrl+j", "cursor_down", "cursor down", show=True),
        Binding("ctrl+l", "cursor_next", "cursor next", show=True),
    ]

    keyboardStatus = KeyboardStatus()
    word = ""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("What do you want to tell?", id="question")
        yield AlwaysInput(id="input")
        yield Keyboard(id="keyboard")
        yield Footer()

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
