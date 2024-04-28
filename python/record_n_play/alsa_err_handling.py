from ctypes import *

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  #print ("Alsa Error Messages")
  pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('/usr/lib/arm-linux-gnueabihf/alsa-lib/libasound_module_pcm_bluealsa.so')
# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)

JACK_ERROR_HANDLER_FUNC = CFUNCTYPE(None)
def py_jack_error_handler():
  #print ("Jack Error Messages")
  pass
jack_c_error_handler = JACK_ERROR_HANDLER_FUNC(py_jack_error_handler)
jack = cdll.LoadLibrary('libjack.so.0')
# Set error handler
jack.jack_set_error_function(jack_c_error_handler)


#asound = cdll.LoadLibrary('/usr/lib/arm-linux-gnueabihf/libjack.so.0')











