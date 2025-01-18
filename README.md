# Pico Waveshare

Applications developed for a Pico 2 W device to run on a [Pico-Captouch-ePaper-2.9](https://www.waveshare.com/wiki/Pico-CapTouch-ePaper-2.9). Waveshare provide a small amount of code that can be used to interact with the ePaper display via Python. This functions as a very light-weight SDK.

## Setup

### Flashing MicroPython

The Pico needs to be flashed with it's correct version of micro-python before beginning any development. The online repository can be found [here](https://micropython.org/download/RPI_PICO2_W/). While holding the `BOOTSEL` button on the bottom of the Pico, plug it into computer. Drag the `.uf2` file containing MicroPython into the drive visible for the Pico. The Pico should restart when this happens.

### Uploading Code

To upload code to the RPI Pico 2 W, I used the VSCode extension ([setup instruction here](https://www.raspberrypi.com/news/pico-vscode-extension/)).

To upload code, import the project under the `src/` directory, using the RPI VSCode extention. Select `upload_project` to upload all code in the `src` folder to the Pico.

**It should be noted that when uploading Python code to the Pico, the script `main.py` is what will run by default when power is supplied to the device.**
