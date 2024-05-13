import time

EXIT = False

def zfil(s, width):
# Pads the provided string with leading 0's to suit the specified 'chrs' length
# Force # characters, fill with leading 0's
    return '{:0>{w}}'.format(s, w=width)

def show_current_time():
    print("Local time : %s" %str(time.localtime()))

