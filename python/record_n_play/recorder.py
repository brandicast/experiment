import pyaudio
import threading
import wave


class Recorder:

    isRecording = False
    startRecording = False
    isPlaying = False
    chunk = format = channels = rate = -1

    def __init__(self) -> None:
        # 設定錄音參數
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 48000 #44100

    def start(self):
        self.isRecording = True
        self.startRecording = True
        threading.Thread(target=self.record).start()

    def stop(self):
        self.startRecording = False

    def record(self, output_filename='output.wav'):
        # 建立 PyAudio 物件
        p = pyaudio.PyAudio()

        # 建立錄音流
        stream_record = p.open(
            format=self.format, channels=self.channels, rate=self.rate, input=True)

        # 開始錄音
        frames = []
        while self.startRecording:
            data = stream_record.read(self.chunk)
            frames.append(data)

        # 停止錄音和播放
        stream_record.stop_stream()
        stream_record.close()
        p.terminate()

        wf = wave.open(output_filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        self.isRecording = False

    def play(self, wave_filename='output.wav'):
        if not self.isPlaying and not self.isRecording:
            threading.Thread(target=self.playWav, args=(wave_filename,)).start()

    def playWav(self, wave_filename='output.wav'):
        self.isPlaying = True 
        p = pyaudio.PyAudio()
        # 建立播放流
        stream_play = p.open(format=self.format, channels=self.channels, rate=self.rate, output=True)
        # Open the sound file 
        wf = wave.open(wave_filename, 'rb')
        # Read data in chunks
        data = wf.readframes(self.chunk)
        
        while data != b'' and not self.isRecording:
            stream_play.write(data)
            data = wf.readframes(self.chunk)
            print (".", end="")
            
        wf.close()
        stream_play.close()
        p.terminate()
        self.isPlaying = False
        print ("Play finished")

