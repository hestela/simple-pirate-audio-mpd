#!/usr/bin/env python3
import time

from PIL import Image, ImageDraw

from st7789 import ST7789

BUTTON_A = 5
BUTTON_B = 6
BUTTON_X = 16
BUTTON_Y = 24

SPI_PORT = 0
SPI_CS = 1
SPI_DC = 9
BACKLIGHT = 13

WIDTH = 240
HEIGHT = 240

buffer = Image.new("RGB", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(buffer)

# Draw a black square on entire screen
draw.rectangle((0, 0, 240, 240), (0, 0, 0))

display = ST7789(
    port=SPI_PORT,
    cs=SPI_CS,
    dc=SPI_DC,
    backlight=BACKLIGHT,
    width=WIDTH,
    height=HEIGHT,
    rotation=90,
    spi_speed_hz=80 * 1000 * 1000,
)

display.display(buffer)
time.sleep(1.0 / 60)
display.set_backlight(0)
