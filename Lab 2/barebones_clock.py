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



image_sun = Image.open("sun.jpg")
image_moon = Image.open("moon.jpeg")
# Scale the image to the smaller screen dimension
image_sun_ratio = image_sun.width / image_sun.height
screen_ratio = width / height
if screen_ratio < image_sun_ratio:
    scaled_width = image_sun.width * height // image_sun.height
    scaled_height = height
else:
    scaled_width = width
    scaled_height = image_sun.height * width // image_sun.width
new_width = (int(scaled_width*0.2))
new_height = (int(scaled_height*0.2))

image_sun = image_sun.resize((new_width, new_height), Image.BICUBIC)
image_moon = image_moon.resize((new_width, new_height), Image.BICUBIC)
# Crop and center the image
# x = scaled_width // 2 - width // 2
# y = scaled_height // 2 - height // 2
# x,y = 0,0
# image = image.crop((x, y,x + width, y + height))
x,y = height - new_height - 1, width - new_width - 1
offset_x = 0.5
offset_y = 1
status = 'day'
timer_start = time.time()
while True:
    # disp.image(image)
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    fill = color565(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    timer_end = time.time()
    timer_str = "{:.4f}".format((timer_end - timer_start))
    draw.text((0, -2), timer_str, font=font, fill=fill)


    if x > -new_width + 5 :
        x -= offset_x
    # else:
    #     x += 1

    if y > -new_height + 5 :
        # print(x**2)
        y -= offset_y
        # y -= int(x**2 / 1000)

    if x <= -new_width + 5 and  y <= -new_height + 5:
        if status == "day" :
            status = "night"
        else:
            status = "day"

        x, y = height - new_height - 1, width - new_width - 1


    # else:
    #     y += 2
    new_x = int(x)
    new_y = int(y)
    if status == "day":
        disp.image(image_sun, rotation,new_x,new_y)
    else:
        disp.image(image_moon, rotation, new_x, new_y)

    if buttonA.value == False:
        disp.image(image, rotation)
    time.sleep(0.001)