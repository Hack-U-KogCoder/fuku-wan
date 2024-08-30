import socket
import json
import re


class AutoReplyManager:
    HOST = "127.0.0.1"
    PORT = 65432

    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.HOST, self.PORT))
        self.s = s

    def close(self):
        self.s.close()

    def get_replies(self):
        s = self.s
        s.sendall(b"REQUEST")
        notification = s.recv(1024).decode()
        if notification.startswith("RESPONSE:"):
            saved_filepath = notification[9:]
            res_json = json.loads(saved_filepath)["content"]
            print(f"返答案: {res_json}")
            return json.loads(re.sub(r"^json\n", "", res_json.replace("```", "")))
        else:
            return {"??": "わからない"}
