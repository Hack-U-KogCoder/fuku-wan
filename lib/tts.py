import subprocess

# テキストファイル
TEXT_FILE = "input.txt"

# openjtalk
X_DIC = "/var/lib/mecab/dic/open-jtalk/naist-jdic"
M_VOICE = "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice"
R_SPEED = "0.7"
OW_WAVFILE = "output.wav"


def talk_text(t):
    if t == "":
        t = "ワン！"
    open_jtalk = ["open_jtalk"]
    xdic = ["-x", X_DIC]
    mvoice = ["-m", M_VOICE]
    rspeed = ["-r", R_SPEED]
    vol = ["-jm", "1.8"]
    owoutwav = ["-ow", OW_WAVFILE]
    cmd = open_jtalk + xdic + mvoice + rspeed + vol + owoutwav

    # open_jtalkコマンドの実行
    c = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    c.stdin.write(t.encode("utf-8"))
    c.stdin.close()
    c.wait()

    # aplayを使って音声を再生
    aplay = ["aplay", OW_WAVFILE]
    wr = subprocess.run(aplay, capture_output=True, text=True)


def main():
    with open(TEXT_FILE) as f:
        for line in f:
            talk_text(line)


if __name__ == "__main__":
    main()
