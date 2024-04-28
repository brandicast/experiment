import pyaudio
import threading
import wave
from alsa_err_handling import *
import time

def ChkInput():
    global STOP
    # 檢查使用者是否輸入了停止命令
    STOP = input() == "stop"


STOP = False

# 設定錄音參數
chunk = 8192
format = pyaudio.paInt32
channels = 1
rate = 48000

# 建立 PyAudio 物件
p = pyaudio.PyAudio()

# 建立錄音流
stream_record = p.open(format=format, channels=channels, rate=rate, input=True)

# 建立播放流
stream_play = p.open(format=format, channels=channels, rate=rate, output=True)

t = threading.Thread(target=ChkInput)

t.start()

# 開始錄音和播放
frames = []
while not STOP:
    # 錄製音頻
    data = stream_record.read(chunk, exception_on_overflow=False)
    frames.append(data)

    # 播放音頻
    stream_play.write(data)
    # print("data played")


# 停止錄音和播放
stream_record.stop_stream()
stream_play.stop_stream()
stream_record.close()
stream_play.close()
p.terminate()

wf = wave.open('output.wav', 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(format))
wf.setframerate(rate)
wf.writeframes(b''.join(frames))
wf.close()
