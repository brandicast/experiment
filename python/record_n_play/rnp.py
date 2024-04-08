from recorder import Recorder

rec = Recorder()

while True:
    cmd = input('Command :')
    if cmd == 'start':
        rec.start()
    elif cmd == 'stop':
        rec.stop()
    elif cmd == 'quit':
        exit()
    elif cmd == 'status':
        print("Recording status : " +
              ("is recording" if rec.isRecording else " is stopped"))
    else:
        print("No [" + cmd + "] command, please try again")
