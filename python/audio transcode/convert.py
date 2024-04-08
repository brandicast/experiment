from os import path
import os
from pydub import AudioSegment
from pydub.utils import mediainfo


# files                                                                         
directory = r"C:/本機分享/2020-09-23 L1 課文對話錄音/"
src = "0924 L1課文.m4a"
dst = "test.wav"

print (os.path.isdir(directory))
print (os.path.isfile(directory+src))

# convert wav to mp3                                                            
sound = AudioSegment.from_file(directory+ src)

print ("dBFS        :" + str(sound.dBFS))
print ("Channels    :" + str(sound.channels))
print ("Sample Width:" + str(sound.sample_width))
print ("Framerate   :" + str(sound.frame_rate))
print ("Frame Width :" + str(sound.frame_width))
print ("RMS         :" + str(sound.rms))    
print ("Max         :" + str(sound.max))
print ("max_dBFS    :" + str(sound.max_dBFS))
print ("duration_seconds:" + str(sound.duration_seconds))
print ("frame_count   :" + str(sound.frame_count()))


print (mediainfo(directory+ src))

sound.export(dst, format="wav")