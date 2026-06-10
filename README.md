# Pixelplay
Pixelplay is an exploration of how creative thinking and learning can be inculcated at a younger age in educational settings. This project is an industry brief with Transport for London which instructs to reuse soon-to-be-decomissioned London Underground trains for youth and social enterprise. Repurposing the LED screens on the inside of the tube for interactive learning, they are joined to create an interactive whiteboard. The design is heavily inspired by retro arcades and is entirely flat pack, for easy disassembly. Pixelplay is distributed as kits to schools where students can build the interface on their own. There are various open source codes available online to control the interface, but students are encouraged to explore with the interface and come up with their own playful interactions to benefit them in the classroom.

<img width="4000" height="2667" alt="image_4" src="https://github.com/user-attachments/assets/52c0ab0b-601c-4558-b5c7-8172d9d1f2a8" />

## Hardware
- Raspberry Pi (A Pi 3B model was used to build this interface)
- Adafruit RGB Matrix Bonnet (HUB75)
- Two 64×64 RGB LED matrices chained (128×64 total)
- CY-822A USB Joystick Encoder

<img width="4000" height="2667" alt="image_1" src="https://github.com/user-attachments/assets/7c6d730a-1636-4511-9d7d-dba7a81d2c38" />
<img width="6720" height="4480" alt="wiring" src="https://github.com/user-attachments/assets/0631e933-9bce-46b9-8e43-ad2c7210ec60" />

## Hardware Files
The .stl files are 3d print files for casings for your Raspberry Pi and Zero delay USB encoder. There are also .DXF files for your wooden casings, and unless mentioned, they need to be laser cut with 6mm wood. These are all the files for Pixelplay Single - for the Duo option, you will need to laser cut a second set of the same files, except for the side panels. 

## Pixelplay Single Assembly
The bonnet is not directly sitting on the Pi due to the 5V 10 A power supply connected to the bonnet, making the Pi very hot. The bonnet is connected to the Pi with jumper wires, leaving out the 5V and 3.3V connections. For reference, a pinout of the Raspberry Pi 3B is attached.
<img width="2064" height="1185" alt="raspberrypi_pinout" src="https://github.com/user-attachments/assets/fe96c447-efca-437b-aada-4aabf8790281" />

<img width="842" height="595" alt="wiring_instructions" src="https://github.com/user-attachments/assets/b41e39e8-25fd-469d-9ff8-0b0afaf4cb76" />

<img width="922" height="643" alt="assembly_instruction_screwing" src="https://github.com/user-attachments/assets/ccf71243-33de-49d1-a407-079871c74d8d" />


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

## Button Detection

If your joystick encoder has different button codes, run this snippet to find them:

```bash
sudo python3 -c "
from inputs import get_gamepad
while True:
    for e in get_gamepad():
        if e.ev_type not in ('Sync', 'Misc'):
            print(e.ev_type, e.code, e.state)"
```

Press each button and note the code printed. Then update these lines in `pictionaryneopixel.py`:

```python
BTN_CLEAR = "BTN_BASE4"   # button that clears the canvas
BTN_COLOR = "BTN_BASE6"   # button that cycles colour
```

Replace `BTN_BASE4` and `BTN_BASE6` with whatever codes your encoder prints.
