import pyaudio
import threading
import wave


class Recorder:

    isRecording = False
    STOP = False
    chunk = format = channels = rate = -1
    output_filename = 'output.wav'

    def __init__(self) -> None:
        # 設定錄音參數
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100

    def start(self):
        self.isRecording = True
        self.STOP = False
        threading.Thread(target=self.record).start()

    def stop(self):
        self.STOP = True

    def record(self):
        # 建立 PyAudio 物件
        p = pyaudio.PyAudio()

        # 建立錄音流
        stream_record = p.open(
            format=self.format, channels=self.channels, rate=self.rate, input=True)

        # 開始錄音和播放
        frames = []
        while not self.STOP:
            data = stream_record.read(self.chunk)
            frames.append(data)

        # 停止錄音和播放
        stream_record.stop_stream()
        stream_record.close()
        p.terminate()

        wf = wave.open(self.output_filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        self.isRecording = False
