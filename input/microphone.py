import socket
import pyaudio
import struct
from collections import deque
import time
import threading
import wave
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_SECRET"))
audio_file_path = "audio/audio.wav"


def record_audio(stream, audio_buffer, chunk, channels, is_recording):
    while True:
        if is_recording[0]:
            try:
                data = stream.read(chunk, exception_on_overflow=False)
                audio_buffer.append(data)
            except IOError as e:
                if audio_buffer:
                    audio_buffer.append(audio_buffer[-1])
                else:
                    audio_buffer.append(b"\x00" * chunk * channels * 2)
        else:
            time.sleep(0.1)


def save_audio(audio_data, channels, rate, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    with wave.open(audio_file_path, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(rate)
        wf.writeframes(audio_data)


def transcription():
    with open(audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            language="ja",
            response_format="verbose_json",
            file=audio_file,
            # prompt = "話者分離をしてください"
        )
    return transcript


def replyGPT(transcript):
    msg = """あなたには会話の文字起こしを読み、会話に対する返答を考えてもらいます。
    返答は4つ考えてもらい、それぞれ「中立系」、「肯定系」、「否定系」、「素直系」です。
    「中立系」は話者の発言に対して、否定も肯定もしない返答です。
    ただし、会話の内容が質問文である場合、返答はその質問に対する回答としてください。
    「肯定系」、「否定系」は話者の発言に対して、肯定或いは否定を行います。
    「素直系」は話者の発言に対して、「ありがとう」や「ごめんなさい」、「こんにちは」などの非常に単純な返答を行います。
    それぞれの返答の内容は、50文字以内の文章で表してください。
    出力形式はJSONで、以下のフォーマットに沿ってください
    {
        "neutrality" : <ここに中立系の文章>,
        "positivity" : <ここに肯定系の文章>,
        "negativity" : <ここに否定形の文章>,
        "honesty" : <ここに素直系の文章>
    }

    以下に会話の文字起こしを添付します。
    """

    msg += str(transcript)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": [{"type": "text", "text": f"{msg}"}]},
        ],
    )

    # print(response.choices[0].message.json())
    return response


def record_and_save_audio():
    HOST = "127.0.0.1"
    PORT = 65432

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    MAX_SECONDS = 30
    SAVE_DIR = "audio"
    INPUT_DEVICE_INDEX = int(os.getenv("INPUT_DEVICE_INDEX",'0'))

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=INPUT_DEVICE_INDEX, frames_per_buffer=CHUNK
    )

    audio_buffer = deque(maxlen=int(RATE / CHUNK * MAX_SECONDS))
    is_recording = [True]

    recording_thread = threading.Thread(
        target=record_audio, args=(stream, audio_buffer, CHUNK, CHANNELS, is_recording)
    )
    recording_thread.daemon = True
    recording_thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        # print("接続待機中...")
        conn, addr = s.accept()
        # print(f"接続しました: {addr}")

        try:
            while True:
                conn.setblocking(True)
                conn.settimeout(1.0)
                try:
                    request = conn.recv(1024)
                    if request == b"REQUEST":
                        # print("音声データの要求を受信しました")

                        is_recording[0] = False

                        audio_data = b"".join(audio_buffer)

                        saved_filepath = save_audio(
                            audio_data, CHANNELS, RATE, SAVE_DIR
                        )
                        # print(f"サーバーで音声を保存しました: {saved_filepath}")

                        transcript = transcription()
                        response = replyGPT(transcript)

                        notification = f"RESPONSE:{response.choices[0].message.json()}"
                        conn.sendall(notification.encode())

                        audio_buffer.clear()
                        is_recording[0] = True

                except socket.timeout:
                    pass
                except ConnectionResetError:
                    # print("クライアントとの接続が切断されました")
                    break
                except Exception as e:
                    print(f"Error : {e}")

                time.sleep(0.001)
        except Exception as e:
            print(f"Error : {e}")
        finally:
            is_recording[0] = False
            stream.stop_stream()
            stream.close()
            p.terminate()


if __name__ == "__main__":
    record_and_save_audio()
