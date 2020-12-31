#-------------------------------------------------------------------------------
#   Copyright (c) 2020 DOIDO Technologies
#
#   Author   : Walter
#   Version  : 1.0.4
#   Location : github
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# This script displays RaspiBlitz data on an 1.8 inch ST7735 display
#-------------------------------------------------------------------------------

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

import urllib.request
import json
import socket
import subprocess
import re
import pathlib

WIDTH = 128
HEIGHT = 160
SPEED_HZ = 4000000


# Raspberry Pi configuration.
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

# Create TFT LCD display class.
disp = TFT.ST7735(
    DC,
    rst=RST,
    spi=SPI.SpiDev(
        SPI_PORT,
        SPI_DEVICE,
        max_speed_hz=SPEED_HZ))

# Initialize display.
disp.begin()


# Clear display, white background
disp.clear((255, 255, 255))
disp.display()

# Get a PIL Draw object to start drawing on the display buffer.
draw = disp.draw()

#Get directory of the executing script
filePath=str(pathlib.Path(__file__).parent.absolute())

# customizable images path
images_path = filePath+'/images/'

# Customizable fonts path
lato_fonts_path = filePath+'/lato/'

# Define a function to initialize the display.
def initialize__lcd():
    # Initialize display.
    disp.begin()

    #Clear display, white background
    disp.clear((255, 255, 255))
    
    disp.display()

# Define a function to calculate an inverted x co-ordinate.
def get_inverted_x(currentX, objectSize):
    invertedX = WIDTH - (currentX + objectSize)
    return invertedX
    
# Define a function to draw the lcd background image.
def display_background_image():
    # Load an image.
    image_path = images_path+'BG.png'
    image = disp.buffer
    position = (0,0)
    picimage = Image.open(image_path)
    # Convert to RGBA
    picimage = picimage.convert('RGBA')
    # Resize the image
    picimage = picimage.resize((160, 128), Image.BICUBIC)
    # Rotate image
    rotated = picimage.rotate(270, expand=1)
    # Paste the image into the screen buffer
    image.paste(rotated, position, rotated)

# Define a function to draw raspiblitz logo on display
def display_logo():
    # Load an image.
    image_path = images_path+'RaspiBlitz_Logo.png'
    image = disp.buffer
    W, H = (128,160)
    width = 100
    position = (get_inverted_x(5,34), -5)
    picimage = Image.open(image_path)
    # Convert to RGBA
    picimage = picimage.convert('RGBA')
    # Resize the image
    picimage = picimage.resize((100, 34), Image.BICUBIC)
    # Rotate image
    rotated = picimage.rotate(270, expand=1)
    # Paste the image into the screen buffer
    image.paste(rotated, position, rotated)

# Define a function to draw a bitcoin icon.
def display_btc_icon():
    # Load an image.
    image_path = images_path+'bitcoin.png'
    image = disp.buffer
    W, H = (128,160)
    width = 26
    position = (get_inverted_x(40,26), 16)
    picimage = Image.open(image_path)
    # Convert to RGBA
    picimage = picimage.convert('RGBA')
    # Resize the image
    picimage = picimage.resize((26, 26), Image.BICUBIC)
    # Rotate image
    rotated = picimage.rotate(270, expand=1)
    # Paste the image into the screen buffer
    image.paste(rotated, position, rotated)
   
# Define a function to create rotated text.
def draw_rotated_text(image, text, position, angle, font, fill=(255,255,255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    newX,newY = position
    altX = get_inverted_x(108,13)
    altY = HEIGHT - (width + newY)
    altPosition = (altX,altY)
    image.paste(rotated, altPosition, rotated)
    
# Define a function to create left justified text.
def draw_left_justified_text(image, text, xposition, yPosition, angle, font, fill=(255,255,255)):
    # Get rendered font width and height.
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    # Create a new image with transparent background to store the text.
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    # Render the text.
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    W, H = (128,160)
    # Rotate the text image.
    rotated = textimage.rotate(angle, expand=1)
    # Paste the text into the image, using it as a mask for transparency.
    xCordinate = xposition
    #yCordinate = int((H-width)-yPosition)
    yCordinate = yPosition
    
    image.paste(rotated, (xCordinate,yCordinate), rotated)
    
    
# Define a function to display the temperature and ip address
def display_ip_and_temperature():
    # Measure temperature
    temp_result = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    temp_string = temp_result.stdout.decode('utf-8')
    raw_temp = temp_string.replace("temp=","")
    raw_temp = raw_temp.replace("'C","")
    temperature = raw_temp.strip()+"°C"
    font13 = ImageFont.truetype(lato_fonts_path+"Lato-Bold.ttf", 13)
    draw_rotated_text(disp.buffer, temperature, (108, 5), 270, font13, fill=(200,200,200))

    # Get ip address
    ip_result = subprocess.run(['hostname', '-I'], stdout=subprocess.PIPE)
    ip_string = ip_result.stdout.decode('utf-8')
    draw_left_justified_text(disp.buffer, ip_string, -10,5, 270, font13, fill=(200,200,200))

# Define a function to draw bitcoin price
def draw_bitcoin_price():
    # Display current bitcoin price
    price_font = ImageFont.truetype(lato_fonts_path+"Lato-Bold.ttf", 26)
    try:
        url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=KES,USD"
        currentPrice = urllib.request.urlopen(url).read()
        price_dict = json.loads(currentPrice)
        price = str(int(price_dict['USD']))
        #print("$" + price)
        draw_left_justified_text(disp.buffer, "$ " + price, get_inverted_x(71,26)-3,16, 270, price_font, fill=(255,255,255))
    except:
        draw_left_justified_text(disp.buffer, "$", get_inverted_x(71,26)-3,16, 270, price_font, fill=(255,255,255))
        
# Define a function to draw the syncing text
def display_syncing_text(is_syncing):
    text_font = ImageFont.truetype(lato_fonts_path+"Lato-Bold.ttf", 20)
    if is_syncing:
        draw_left_justified_text(disp.buffer, "Syncing", get_inverted_x(41,20)-3,45, 270, text_font, fill=(255,255,255))

# Define a function to find a word using regex
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
# Define a function to return a word search result
def get_search_result(word,sentence):
    match_object = findWholeWord(word)(sentence)
    
    if match_object == None:
        return False
    else:
        return True

# Define a function to get btc sync status
# Returns true if btc is syncing
def is_btc_not_synced():
    sync_result = subprocess.run([filePath+'/get_btc_sync.sh'], stdout=subprocess.PIPE)
    sync_string = sync_result.stdout.decode('utf-8')

    sync_status = get_search_result("NOT",sync_string)
    return sync_status
        
# Draw the image on the display hardware.
print('Running LCD script Version 1.0.4')

while True:
    try:  
        disp.clear((255, 255, 255))
        display_background_image()
        display_logo()
        display_btc_icon()
        btc_syncing = is_btc_not_synced()
        display_syncing_text(btc_syncing)
        draw_bitcoin_price()
        display_ip_and_temperature()
        disp.display()
        time.sleep(60)
    except:
        print("error")





