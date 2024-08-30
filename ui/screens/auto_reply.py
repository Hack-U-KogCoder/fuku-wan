from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Button, OptionList
from textual.reactive import reactive
from textual.binding import Binding
from lib.tts import talk_text


global_replies: list[str] = []


class AutoReplyScreen(Screen):
    CSS_PATH = "common.tcss"
    TITLE = "ふくワン - 自動応答"
    replies = reactive(global_replies, recompose=True)

    BINDINGS = [
        Binding("ctrl+k", "cursor_up", "cursor up"),
        Binding("ctrl+j", "cursor_down", "cursor down"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield OptionList(*self.replies, id="list-reply")
        yield Button("ワン!ワン!", id="btn-GetReply", variant="primary")
        yield Button("モード選択", id="btn-ModeChange", variant="success")

    def on_option_list_option_selected(self, mes: OptionList.OptionSelected):
        global global_replies
        text = global_replies[mes.option_index]
        talk_text(text)
        mes.option_list.clear_options()
        self.query_one("#btn-GetReply").focus()

    def action_cursor_up(self) -> None:
        if self.focused.highlighted is None:
            self.focused.highlighted = 0
        elif self.focused.id == "list-reply":
            self.focused.highlighted -= 1
        else:
            self.focus_previous()

    def action_cursor_down(self) -> None:
        if self.focused.highlighted is None:
            self.focused.highlighted = 0
        elif self.focused.id == "list-reply":
            self.focused.highlighted += 1
        else:
            self.focus_next()


def handle_get_reply(app):
    global global_replies
    res = app.arm.get_replies()
    list_reply = app.query_one("#list-reply")
    list_reply.clear_options()
    options = list(res.values())
    global_replies = options
    list_reply.add_options(options)
    list_reply.focus()


def handleButtonAutoReply(app, event) -> bool:
    global global_replies
    match event.button.id:
        case None:
            pass
        case "btn-GetReply":
            handle_get_reply(app)
        case "btn-ModeChange":
            app.switch_mode("mode_change")
        case _:
            return False
    return True
