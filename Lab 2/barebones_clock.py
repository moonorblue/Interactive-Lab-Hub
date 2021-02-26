import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
import random
from adafruit_rgb_display.rgb import color565

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.


buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

timer = False
timer_start = 0
timer_end = 0
x1 = 50
x2 = 35
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    time_str = time.strftime("%m/%d/%Y \n%H:%M:%S")
    y = top
    fill = ""
    if buttonA.value == True:
        fill = "#FFFFFF"
    else:
        fill = color565(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    draw.text((x1, y), time_str, font=font, fill=fill)

    if buttonB.value == False:
        if timer == False:
            timer = True
            timer_start = time.time()
            timer_end = timer_start
        else:
            timer_end = time.time()
        timer_str = "Timer: {:.4f}".format((timer_end - timer_start))
        y += 3 * font.getsize(time_str)[1]
        draw.text((x2, y), timer_str, font=font, fill=fill)
    else:
        if timer_end - timer_start != 0:
            timer_str = "Record: {:.4f}".format((timer_end - timer_start))
            y += 3 * font.getsize(time_str)[1]
            draw.text((x2, y), timer_str, font=font, fill=fill)

        timer = False



    # Display image.
    disp.image(image, rotation)
    time.sleep(0.1)