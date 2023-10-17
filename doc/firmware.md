# Firmware

This project is built on top of MicroPython. As I type those lines, the latest MicroPython version is 1.21 and was released on Oct 6 2023.

However, we can not use the [ESP32-C3 artefact built from MicroPython](https://micropython.org/download/ESP32_GENERIC_C3/) as it misses a [PR](https://github.com/micropython/micropython/pull/9583) that we need for this project. Indeed, the ESP32-C3 does not manage the wake-up events from deepsleep like the other ESP32. Due to this, MicroPython does not implement any wake-up event except timer wake-up. We indeed need to be able to wake up the ESP32 when you press on any buttons.

This documents aims to explain how to correctly build a MicroPython that suits our needs

## Build MicroPython firmware

MicroPython uses the ESP-IDF SDK in order to build ESP32 artefacts. You can see in the `ports/esp32/README.md` file that it uses the 5.0.2 SDK version. You can also see that by running the following lines in the REPL of a flashed firmware on a ESP32-C3 chip:

```python
>>> import platform
>>> platform.platform()
MicroPython-1.21.0-riscv-IDFv5.0.2-with-newlib4.1.0

>>> import os
>>> os.uname()
(sysname='esp32', nodename='esp32', release='1.21.0', version='v1.21.0 on 2023-10-06', machine='ESP32C3 module with ESP32C3')
```

Let's get the micropython repository ready:

```bash
git clone git@github.com:micropython/micropython.git
cd micropython
git checkout v1.21.0
gh pr checkout 9583
git rebase v1.21.0
```

The `ports/esp32/README.md` files explains very well how to build a MicroPython firmware for the ESP32 target, but in a nutshell, here is what you need to do:

```bash
git clone -b v5.0.2 --recursive https://github.com/espressif/esp-idf.git
cd esp-idf
./install.sh
source export.sh

cd ../micropython
make -C mpy-cross
cd ports/esp32
make BOARD=ESP32_GENERIC_C3 submodules
make BOARD=ESP32_GENERIC_C3
```

The generated firmware will be here: `build-ESP32_GENERIC_C3/firmware.bin`

Next step: deploy the firmware to the target!

## Deploy MicroPython firmware

If you are lucky, you can just run the following commands: 

```bash
esptool.py --chip esp32c3 --port /dev/ttyACM0 erase_flash
esptool.py --chip esp32c3 --port /dev/ttyACM0 --baud 460800 write_flash -z 0x0 firmware.bin
```

This works on a non-modified ESP32-C3 module. As soon as I removed the LDO that was on the module, this would not work anymore... Indeed, I would get the following error when running the erase_flash command.

```
Serial port /dev/ttyUSB0
Connecting....
Detecting chip type... Unsupported detection protocol, switching and trying again...
Connecting....
Detecting chip type... ESP8266
Chip is ESP8266EX
Features: WiFi
Crystal is 26MHz
MAC: 34:94:54:61:ac:3b
Uploading stub...
Running stub...
Stub running...

A fatal error occurred: Unable to verify flash chip connection (No serial data received.).
```

The [stub](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/flasher-stub.html) seems to be blocked somehow...

By doing what [lewisxhe suggested](https://github.com/Xinyuan-LilyGO/T-Display-S3/issues/162), you should be able to run the erase command

```
insert USB, press and hold BOOT, do not release the boot button, then press RST. Finally, release the boot
```

After this procedure, run the erase_flash command and voilà!

The write_flash command should run without any issue!