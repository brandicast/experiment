# Project Background

This project is based on Raspberry Pi Pico W.  

## Development Environment

- The development envrionment is in WSL of windows.  The configuration of sharing USB device from Windows to WSL is ready. Pico is being connected via USB on /dev/ttyACM0. 

- Working folder is under /home/brandicast/github/experiment/raspberry_pi/pico/prj/epaper_waveshare.  Meaning all the files created by you should be under this folder.

- Read only those specify in "Reference to waveshare epaper devices" and ignore other folders.

## Rules for implemnentation

- Use MicroPython as coding language.  If it is necessary to use native language such as C, please ask.

- Use virtual environment called venv and install necessary packages under.

- Put all source code under .\src\

- Put all planning document under .\plans\

## Communication with Pico

- Use rshell to upload code.  If to use any other tools, please ask.

## Logs

- Keep the planning and implementation sugggestion and plans under .\plans\.  Filename with a date and version id.

## Reference to waveshare epaper devices

- Refer to /home/brandicast/github/experiment/raspberry_pi/pico/README.md for basic knowldge about Pico if necessary.
- refer to /home/brandicast/github/experiment/raspberry_pi/pico/prj/epaper/7.5inch-e-paper-b-v3-specification.pdf for the specification of the epaper display.
- refer to /home/brandicast/github/experiment/raspberry_pi/pico/prj/epaper/waveshare.py for a sample library code to display on epaper.
