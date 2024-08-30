from ui import MainApp
from lib.auto_reply import AutoReplyManager

if __name__ == "__main__":
    arm = AutoReplyManager()
    app = MainApp()
    app.arm = arm
    reply = app.run()
    print(reply)
