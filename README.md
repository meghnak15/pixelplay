# Pixelplay
Pixelplay is an exploration of how creative thinking and learning can be inculcated at a younger age in educational settings. This project is an industry brief with Transport for London which instructs to reuse soon-to-be-decomissioned London Underground trains for youth and social enterprise. Repurposing the LED screens on the inside of the tube for interactive learning, they are joined to create an interactive whiteboard. The design is heavily inspired by retro arcades and is entirely flat pack, for easy disassembly. Pixelplay is distributed as kits to schools where students can build the interface on their own. There are various open source codes available online to control the interface, but students are encouraged to explore with the interface and come up with their own playful interactions to benefit them in the classroom.
## Hardware
- Raspberry Pi 3B
- Adafruit RGB Matrix Bonnet (HUB75)
- Two 64×64 RGB LED matrices chained (128×64 total)
- CY-822A USB Joystick Encoder

## Dependencies

### System packages
\```bash
sudo apt-get update
sudo apt-get install -y python3-dev python3-pillow cython3 git
\```

### 1. rpi-rgb-led-matrix (rgbmatrix)
This is a C library with Python bindings — NOT installable via pip alone.

\```bash
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
make build-python HARDWARE_DESC=adafruit-hat
sudo make install-python HARDWARE_DESC=adafruit-hat
cd ..
\```

### 2. inputs (USB gamepad/joystick)
\```bash
pip3 install inputs
\```

## Run
\```bash
sudo python3 pictionaryneopixel.py
\```
> Must be run with `sudo` — the LED matrix library requires GPIO access.
