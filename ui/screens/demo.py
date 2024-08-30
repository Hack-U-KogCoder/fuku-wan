import re
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Button
from textual.binding import Binding
from lib.tts import talk_text

PHRASES = [
    "どうも、ぼく、ふくワンだワン",
    "ポイズンだワン！",
    "うんうん",
    "誠に申し訳ありませんでした",
    "ありがとうございました！",
]


class DemoScreen(Screen):
    CSS_PATH = "common.tcss"
    TITLE = "ふくワン - プリセット"

    BINDINGS = [
        Binding("ctrl+k", "cursor_up", "cursor up"),
        Binding("ctrl+j", "cursor_down", "cursor down"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        for i in range(len(PHRASES)):
            yield Button(PHRASES[i], id=f"btn-{i}")
        yield Button("モード選択", id="btn-ModeChange", variant="success")

    def action_cursor_up(self) -> None:
        self.focus_previous()

    def action_cursor_down(self) -> None:
        self.focus_next()


def handleButtonDemo(app, event) -> bool:
    btn = event.button
    match event.button.id:
        case None:
            pass
        case a if re.search(r"btn-\d+", a):
            btn_id = int(btn.id.split("-")[1])
            talk_text(PHRASES[btn_id])
        case "btn-ModeChange":
            app.switch_mode("mode_change")
        case _:
            return False
    return True
