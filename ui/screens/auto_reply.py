from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Button, OptionList
from textual.reactive import reactive
from lib.tts import talk_text


global_replies: list[str] = []


class AutoReplyScreen(Screen):
    CSS_PATH = "common.tcss"
    TITLE = "HackU - auto reply"
    replies = reactive(global_replies, recompose=True)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield OptionList(*self.replies, id="list-reply")
        yield Button("返答作成", id="btn-GetReply")
        yield Button("モード選択", id="btn-ModeChange", variant="success")
        yield Button("終了", id="btn-Exit", variant="error")

    def on_option_list_option_selected(self, mes: OptionList.OptionSelected):
        global global_replies
        text = global_replies[mes.option_index]
        talk_text(text)
        mes.option_list.clear_options()


def handle_get_reply(app):
    global global_replies
    res = app.arm.get_replies()
    list_reply = app.query_one("#list-reply")
    list_reply.clear_options()
    options = list(res.values())
    global_replies = options
    list_reply.add_options(options)


def handleButtonAutoReply(app, event) -> bool:
    global global_replies
    match event.button.id:
        case None:
            pass
        case "btn-GetReply":
            handle_get_reply(app)
        case "btn-ModeChange":
            app.switch_mode("mode_change")
        case "btn-Exit":
            app.exit()
        case _:
            return False
    return True
