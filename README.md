# Pixelplay
Pixelplay is an exploration of how creative thinking and learning can be inculcated at a younger age in educational settings. This project is an industry brief with Transport for London which instructs to reuse [soon-to-be-decomissioned London Underground trains](https://tfl.gov.uk/travel-information/improvements-and-projects/piccadilly-line-upgrade) for youth and social enterprise. Repurposing the LED screens on the inside of the tube for interactive learning, they are joined to create an interactive whiteboard. The design is heavily inspired by retro arcades and is entirely flat pack, for easy disassembly. Pixelplay is distributed as kits to schools where students can build the interface on their own. There are various open source codes available online to control the interface, but students are encouraged to explore with the interface and come up with their own playful interactions to benefit them in the classroom.

<img width="4000" height="2667" alt="image_4" src="https://github.com/user-attachments/assets/52c0ab0b-601c-4558-b5c7-8172d9d1f2a8" />

## Hardware
- [Raspberry Pi (A Pi 3B model was used to build this interface)](https://www.raspberrypi.com/products/)
- [Adafruit RGB Matrix Bonnet (HUB75)](https://thepihut.com/products/adafruit-rgb-matrix-bonnet-for-raspberry-pi-ada3211?srsltid=AfmBOoosZDMMtj-f10rmDFJNFyiaX33VN8n1SeQn5fzrlHAI6YYLXVva)
- [Two 64×64 RGB LED matrices chained (128×64 total)](https://thepihut.com/products/rgb-full-colour-led-matrix-panel-3mm-pitch-64x64-pixels?srsltid=AfmBOop42c_z0unLDgqJ-aGlvVcxaNV0BmpcAfSwvAHKaUJlHmw07-vn)
- [CY-822A USB Joystick Encoder](https://www.amazon.co.uk/Owootecc-Encoder-Raspberry-RetroPie-Project/dp/B08SC973C8/ref=sr_1_7?dib=eyJ2IjoiMSJ9.Pf6MCyiHeNSp3QWT-Pg_3TNg49vao6xSFWqJyu_yDKJzDAlKCIJSyp6au7yBU4bZZwQv9DhTdmp19x4Nw-wX12EyicAVuB25yMj-r78_MK4Gt2stAiTKU2I7cX1fzW1eExPVR0bqKFdLMGF08iM6yxf0sOaM_KkXkc_YjuO9tAYNtKlekOAEK5JtNnNDGVQsYEI9a_dZAbBEv0BAkBgbvCJ3k39xpZIWpVBDYiA-k9Y.cOY_TSOJnPpEZa17JAdR7IYqdlVzdLVGUy-JP-sVcVk&dib_tag=se&keywords=usb+encoder&qid=1781171508&sr=8-7)
- [Sanwa 8-way Arcade Joystick](https://thepihut.com/products/official-sanwa-8-way-arcade-joystick-jlf-tp-8yt?srsltid=AfmBOorLUa7LGwAmgUolZb-G-nuV5N1DA3dvOWlVBI_9W441qnJ27IlM&variant=37569028161731)
- [30mm Arcade Button](https://thepihut.com/products/arcade-button-30mm-translucent-bright-green)
- [60mm Arcade Button](https://thepihut.com/products/large-arcade-button-with-led-60mm-yellow)
- [5V 10A Power Supply](https://www.amazon.co.uk/Current-Universal-Wireless-Multi-Device-Charging/dp/B0GBVHZVKD/ref=asc_df_B0GBVHZVKD?mcid=53a3aa93003f331f8587fc9761ada322&tag=googshopuk-21&linkCode=df0&hvadid=784327053521&hvpos=&hvnetw=g&hvrand=4537974544107928026&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9045888&hvtargid=pla-2478174132636&psc=1&hvocijid=4537974544107928026-B0GBVHZVKD-&hvexpln=0&gad_source=1)
<img width="4000" height="2667" alt="image_1" src="https://github.com/user-attachments/assets/7c6d730a-1636-4511-9d7d-dba7a81d2c38" />
<img width="6720" height="4480" alt="wiring" src="https://github.com/user-attachments/assets/0631e933-9bce-46b9-8e43-ad2c7210ec60" />

## Hardware Files
The .stl files are 3d print files for casings for your Raspberry Pi and Zero delay USB encoder. There are also .DXF files for your wooden casings, and unless mentioned, they need to be laser cut with 6mm wood. These are all the files for Pixelplay Single - for the Duo option, you will need to laser cut a second set of the same files, except for the side panels. 

## Pixelplay Single Assembly
The bonnet is not directly sitting on the Pi due to the 5V 10 A power supply connected to the bonnet, making the Pi very hot. The bonnet is connected to the Pi with jumper wires, leaving out the 5V and 3.3V connections. For reference, a pinout of the Raspberry Pi 3B is attached.
<img width="2064" height="1185" alt="raspberrypi_pinout" src="https://github.com/user-attachments/assets/fe96c447-efca-437b-aada-4aabf8790281" />
<img width="3561" height="3561" alt="IMG_9217" src="https://github.com/user-attachments/assets/3bb4b080-69de-40d4-a577-baaad38a02a5" />


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
