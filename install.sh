#!/bin/bash
set -e

echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-dev python3-pillow cython3 git

echo "Installing rpi-rgb-led-matrix..."
git clone https://github.com/hzeller/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
make build-python HARDWARE_DESC=adafruit-hat
sudo make install-python HARDWARE_DESC=adafruit-hat
cd ..

echo "Installing Python dependencies..."
pip3 install inputs

echo "Done! Run with: sudo python3 pictionaryneopixel.py"
