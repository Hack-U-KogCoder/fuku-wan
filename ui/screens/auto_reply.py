from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Button, OptionList
from textual.reactive import reactive


class AutoReplyScreen(Screen):
    CSS_PATH = "common.tcss"
    TITLE = "HackU - auto reply"
    replies = reactive(["test", "host", "west", "best"], recompose=True)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield OptionList(*self.replies)
        yield Button("mode", id="btn-ModeChange")
        yield Button("Exit", id="btn-Exit")

    def on_option_list_option_selected(self, mes: OptionList.OptionSelected):
        self.replies = ["a", "b", "c", "d"]
        # self.refresh()
        # raise ValueError(f"{mes.option_list}, {mes.option_index}, {self.replies}")


def handleButtonAutoReply(app, event) -> bool:
    match event.button.id:
        case None:
            pass
        case "btn-ModeChange":
            app.switch_mode("mode_change")
        case "btn-Exit":
            app.exit()
        case _:
            return False
    return True
