import pyaudio

# 設定錄音參數
chunk = 1024  # 每個音訊片段的大小
sample_format = pyaudio.paInt16  # 音訊格式
channels = 1  # 聲道數
rate = 44100  # 取樣率

# 建立 pyaudio 物件
p = pyaudio.PyAudio()

# 建立錄音串流
stream = p.open(
    format=sample_format,
    channels=channels,
    rate=rate,
    input=True,
    frames_per_buffer=chunk,
)

# 開始錄音
frames = []
while True:
    # 讀取音訊片段
    data = stream.read(chunk)
    # 將音訊片段加入 frames 陣列
    frames.append(data)

# 停止錄音
stream.stop_stream()
stream.close()

# 關閉 pyaudio 物件
p.terminate()

# 將 frames 陣列轉換為音訊檔案
import wave

wf = wave.open("output.wav", "wb")
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(rate)
wf.writeframes(b"".join(frames))
wf.close()