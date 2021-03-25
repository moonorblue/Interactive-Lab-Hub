import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
import random
from adafruit_rgb_display.rgb import color565
from subprocess import Popen, call


import datetime
import json
import time
import hmac
from requests import Request, Session



API = "NtLHXKDodrJP6koKOZobYLDAD957uqO7wWzSaONF"
API_secret = "OpL8zZ6L0wJviNBMnAwbW3wKhdFPsx0X6W-lV6dL"
sub_account = "t"
ftx_domain = "https://ftx.com/api"
tol = 0.9

def callAPI(string, params, type, is_sub):
    ts = int(time.time() * 1000)

    path = ftx_domain+string

    if type == "GET":
        request = Request(type, path, params=params)
    elif type == "POST":
        request = Request(type, path, json=params)

    prepared = request.prepare()

    signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
    if prepared.body:
        signature_payload += prepared.body

    signature_payload = signature_payload
    signature = hmac.new(API_secret.encode(),
                         signature_payload, 'sha256').hexdigest()

    prepared.headers['FTX-KEY'] = API
    prepared.headers['FTX-SIGN'] = signature
    prepared.headers['FTX-TS'] = str(ts)
    if is_sub:
        prepared.headers['FTX-SUBACCOUNT'] = sub_account
    session = Session()
    resp = session.send(prepared)
    json_data = json.loads(resp.text)
    return json_data

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
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.

x = 0

count = 0




def handel_speak(val):
    call(f"espeak '{val}'", shell=True)

def getPrice(market):
    query = "/markets/{}".format(market)
    get_market_data = callAPI(query, {}, 'GET', True)['result']
    price = get_market_data["last"]
    return price

price = getPrice("BTC/USD")

def showMarket(market):
    price = getPrice("BTC/USD")
    return "{}: ${}".format(market,price)

previousA = 0
previousB = 0
previousC = 0
pA = True
speed = 2
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    marketA = "BTC/USD"
    priceA = getPrice("BTC-PERP")
    s1 = "{}: ${}".format(marketA,priceA)

    marketB = "ETH/USD"
    priceB = getPrice("ETH-PERP")
    s2 = "{}: ${}".format(marketB, priceB)

    marketC = "LTC/USD"
    priceC = getPrice("LTC-PERP")
    s3 = "{}: ${}".format(marketC, priceC)

    if priceA > previousA:
        colorA = "#6beb34"
    else:
        colorA = "#eb4334"
    previousA = priceA

    if priceB > previousB:
        colorB = "#6beb34"
    else:
        colorB = "#eb4334"
    previousB = priceB

    if priceC > previousC:
        colorC = "#6beb34"
    else:
        colorC = "#eb4334"
    previousC = priceC
    y = top
    draw.text((x, y), s1, font=font, fill=colorA)
    y += font.getsize(s1)[1]
    if count > 0:
        draw.text((x, y), s2, font=font, fill=colorB)
        y += font.getsize(s2)[1]
    if count > 1:
        draw.text((x, y), s3, font=font, fill=colorC)
        y += font.getsize(s3)[1]



    if buttonA.value == False and pA == True :
        count += 1
        pA = False

    pA = buttonA.value

    if buttonB.value == False:
        speed = 0.1



    # Display image.
    disp.image(image, rotation)
    time.sleep(speed)