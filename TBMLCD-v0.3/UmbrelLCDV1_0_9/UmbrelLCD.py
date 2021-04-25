#-------------------------------------------------------------------------------
#   Copyright (c) 2021 DOIDO Technologies
#-------------------------------------------------------------------------------

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

import urllib.request as urlreq
import certifi
import ssl
import json
import socket
import pathlib
import subprocess
import sys

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
made_tommy_fonts_path = filePath+'/made_tommy/'
keep_calm_fonts_path = filePath+'/keep_calm/'
porter_fonts_path = filePath+'/porter/'

# Currency as a global variable
currency = sys.argv[1]
# For testing
#currency = "USD"

# Define a function to calculate an inverted x co-ordinate.
def get_inverted_x(currentX, objectSize):
    invertedX = WIDTH - (currentX + objectSize)
    return invertedX
    
# Define a function to draw the lcd background image.
def display_background_image(image_name):
    # Load an image.
    image_path = images_path+image_name
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
    
# Define a function to draw an icon.
def display_icon(image, image_path, position,icon_size):
    # Load an image.
    picimage = Image.open(image_path)
    # Convert to RGBA
    picimage = picimage.convert('RGBA')
    # Resize the image
    picimage = picimage.resize((icon_size, icon_size), Image.BICUBIC)
    # Rotate image
    rotated = picimage.rotate(270, expand=1)
    # Paste the image into the screen buffer
    image.paste(rotated, position, rotated)
    
# Define a function to draw a custom icon.
def display_custom_icon(image, icon_path, position,icon_x_size,icon_y_size):
    # Load an image.
    picimage = Image.open(icon_path)
    # Convert to RGBA
    picimage = picimage.convert('RGBA')
    # Resize the image
    picimage = picimage.resize((icon_x_size, icon_y_size), Image.BICUBIC)
    # Rotate image
    rotated = picimage.rotate(270, expand=1)
    # Paste the image into the screen buffer
    image.paste(rotated, position, rotated)
    
    
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
    
# Define a function to create right justified text.
def draw_right_justified_text(image, text, xposition, yPosition, angle, font, fill=(255,255,255)):
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
    yCordinate = int((H-width)-yPosition)
    #yCordinate = yPosition
    
    image.paste(rotated, (xCordinate,yCordinate), rotated)
    
# Define a function to create centered text.
def draw_centered_text(image, text, xposition, angle, font, fill=(255,255,255)):
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
    yCordinate = int((H-width)/2)
    
    image.paste(rotated, (xCordinate,yCordinate), rotated)

# Define a function to return a comma seperated number
def place_value(number): 
    return ("{:,}".format(number))

# Define a function to get current block height in the longest chain
def get_block_count():
    try:
        url = "https://mempool.space/api/blocks/tip/height"
        currentBlock = urlreq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())).read()
        currentBlockString = currentBlock.decode('utf-8')
        #print("Current block: " + currentBlockString)
        return currentBlockString
    except Exception as err:
        print("Error while getting current block: "+ str(err))
        return ""
    
# Define a function to get bitcoin price
def get_btc_price(currency):
    try:
        # Currency is passed as an argument when running the file   
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies="+currency
        currentPrice = urlreq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())).read()
        coin_prices_dict = json.loads(currentPrice)
        #print(coin_prices_dict['bitcoin'])
        bitcoin_price_dict = coin_prices_dict['bitcoin']
        lowercase_currency = currency.lower()
        price = int(bitcoin_price_dict[lowercase_currency])   
        #print("$" + price)
        return price
    except Exception as err:
        print("Error while getting price: "+ str(err))
        return ""
    
    
# Define a function get the the recommended fees
def get_recommended_fees():
    try:
        url = "https://mempool.space/api/v1/fees/recommended"
        json_response = urlreq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())).read()
        fees_dict = json.loads(json_response)
        #print("fees_dict: ",fees_dict)
        return fees_dict      
    except Exception as e:
        print("Error while getting recommended fees; ",str(e))
        return ""
    
# Define a function get the the next block info
def get_next_block_info():
    try:
        url = "https://mempool.space/api/v1/fees/mempool-blocks"
        json_response = urlreq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())).read()
        blocks_dict = json.loads(json_response)
        #print("blocks_dict: ",blocks_dict)
        # Use the first block
        next_block_dict = blocks_dict[0]
        #print(next_block_dict)
        return next_block_dict     
    except Exception as e:
        print("Error while getting next block info; ",str(e))
        return ""

# Define a function to auto fit price text
def display_price_text(currency):
    try:
        # Get the price
        price = get_btc_price(currency)
        #price = 59392
        # Generate price string
        newPrice = place_value(price)
        # Calculate a font size
        number_of_chars = len(newPrice)
        # Check for divide by zero
        if (number_of_chars != 0):
            font_size = int(290/number_of_chars)
        else:
            font_size = 12
            
        price_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", font_size)
        draw_centered_text(disp.buffer, newPrice, get_inverted_x(12,font_size), 270, price_font, fill="#FFFFFF")
        
        # Display currency
        currency_font_size = 13
        currency_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", currency_font_size)
        draw_left_justified_text(disp.buffer, currency, get_inverted_x(3,currency_font_size),5, 270, currency_font, fill=(255,255,255))
        
        # display SAT / Currency
        sat_font_size = 13
        sats_msg = "SATS / "+currency
        sat_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", sat_font_size)
        draw_centered_text(disp.buffer, sats_msg, get_inverted_x(113,sat_font_size), 270, sat_font, fill="#ff0000")
        
        # display SAT/USD value
        sat_per_usd_int = int(100000000/price)
        #sat_per_usd_int = 1679
        # Generate sat/usd string
        sat_per_usd_str = str(sat_per_usd_int)
        # Calculate a font size
        number_of_chars = len(sat_per_usd_str)
        #print("number_of_chars = len(sat_per_usd_str)",number_of_chars)
        # Check for divide by zero
        if (number_of_chars > 4):
            sat_font_size = int(265/number_of_chars)
        else:
            sat_font_size = 66
        #sat_font_size = 66
        sat_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", sat_font_size)
        draw_centered_text(disp.buffer, sat_per_usd_str, get_inverted_x(45,sat_font_size), 270, sat_font, fill="#FFFFFF")
    except Exception as e:
        print("Error while creating price text; ",str(e))
        

# Define a function to auto fit block count text
def display_block_count_text():
    try:
        block_x_pos = 70
        # Get current bitcoin block
        btc_current_block = get_block_count()
        #btc_current_block = "677171"
        hard_font_size = 42
        block_num_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", hard_font_size)
        draw_centered_text(disp.buffer, btc_current_block, get_inverted_x(block_x_pos+0,hard_font_size), 270, block_num_font, fill=(255,255,255))
        # Display the current block text
        font_size = 12
        block_num_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", font_size)
        draw_centered_text(disp.buffer, "Current Block", get_inverted_x(113,font_size), 270, block_num_font, fill="#00e3fa")
    except Exception as e:
        print("Error while creating block count text; ",str(e))
    
# Define a function to draw Screen1
def draw_screen1(currency):
    # Display current bitcoin price
    display_price_text(currency)
     

    
# Define a function to draw Screen2
def draw_screen2():
    # Display screen heading
    heading_font_size = 11
    heading_font = ImageFont.truetype(keep_calm_fonts_path+"KeepCalm_Medium.ttf", heading_font_size)
    fees_heading1 = "Next Block Fees~"
    fees_heading2 = "Sat/vB"

    heading_x=6
    draw_left_justified_text(disp.buffer, fees_heading1, get_inverted_x(heading_x,heading_font_size),12, 270, heading_font, fill="#00e3fa")
    draw_right_justified_text(disp.buffer, fees_heading2, get_inverted_x(heading_x,heading_font_size),10, 270, heading_font, fill=(255,255,255))
    
    # Get the recommended fees
    fees_dict = get_recommended_fees()
    #print(fees_dict)
    # Get required prices
    high = int(fees_dict['fastestFee'])
    low = int(fees_dict['hourFee'])
    
    # Display the Low fee
    low_x = 95
    icon_x_size = 52
    icon_y_size = 58
    icon2_y_size = 60
    display_custom_icon(disp.buffer, images_path+'rounded_rectangle.png', (get_inverted_x(17,icon_x_size),14),icon_y_size,icon_x_size)
    display_custom_icon(disp.buffer, images_path+'rounded_rectangle.png', (get_inverted_x(17,icon_x_size),86),icon2_y_size,icon_x_size)
    
    # Calculate a font size for the low value
    low_number_of_chars = len(str(low))
    # Check for divide by zero
    font_constant = 76
    if (low_number_of_chars > 2):
        low_font_size = int(font_constant/low_number_of_chars)
    else:
        low_font_size = 38
    # Calculate a font size for the high value
    high_number_of_chars = len(str(high))
    # Check for divide by zero
    if (high_number_of_chars > 2):
        high_font_size = int(font_constant/high_number_of_chars)
    else:
        high_font_size = 38
    #fees_font_size = 38
    if low_number_of_chars == 3:
        low_fee_x = 29
    else:
        low_fee_x = 22
    if high_number_of_chars == 3:
        high_fee_x = 29
    else:
        high_fee_x = 22
    low_fees_font = ImageFont.truetype(keep_calm_fonts_path+"KeepCalm_Medium.ttf", low_font_size)
    high_fees_font = ImageFont.truetype(keep_calm_fonts_path+"KeepCalm_Medium.ttf", high_font_size)
    draw_left_justified_text(disp.buffer, str(low), get_inverted_x(low_fee_x,low_font_size),15, 270, low_fees_font, fill=(255,255,255))
    draw_right_justified_text(disp.buffer, str(high), get_inverted_x(high_fee_x,high_font_size),17, 270, high_fees_font, fill=(255,255,255))
    
    # Display tex under the low and high fees
    fees_text_font_size = 9
    fees_text_font = ImageFont.truetype(porter_fonts_path+"Porter_Bold.ttf", fees_text_font_size)
    fees_low = "LOW"
    fees_high = "HIGH"
    fees_text_x=67
    draw_left_justified_text(disp.buffer, fees_low, get_inverted_x(fees_text_x,fees_text_font_size),14, 270, fees_text_font, fill="#00e3fa")
    draw_right_justified_text(disp.buffer, fees_high, get_inverted_x(fees_text_x,fees_text_font_size),12, 270, fees_text_font, fill="#00e3fa")
    
    # Display block count
    display_block_count_text()
    

# Define a function to draw Screen3
def draw_screen3():
    # Get next block info
    next_block_dict = get_next_block_info()
    #print(next_block_dict)
    # Get required values
    m_fee = int(next_block_dict['medianFee'])
    transactions = int(next_block_dict['nTx'])
    raw_size = int(next_block_dict['blockSize'])

    # Convert size from bytes to Megabytes
    float_size = raw_size/1000000
    size = round(float_size,2) 
    # Display heading
    heading_font_size = 10
    heading_font = ImageFont.truetype(keep_calm_fonts_path+"KeepCalm_Medium.ttf", heading_font_size)
    fees_heading = "Next Block"
    heading_x=5
    draw_left_justified_text(disp.buffer, fees_heading, get_inverted_x(heading_x,heading_font_size),6, 270, heading_font, fill="#1bcee0")
    
    # Display m-fee text
    m_fee_font_size = 15
    m_fee_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", m_fee_font_size)
    m_fee_x=30
    draw_left_justified_text(disp.buffer, "M-Fee~", get_inverted_x(m_fee_x,m_fee_font_size),7, 270, m_fee_font, fill=(255,255,255))
    
    # Display m-fee box
    icon_x_size = 55
    icon_y_size = 54
    display_custom_icon(disp.buffer, images_path+'rounded_rectangle.png', (get_inverted_x(13,icon_x_size),64),icon_y_size,icon_x_size)
    
    # Display m-fee value
    # Calculate a font size
    m_fee_number_of_chars = len(str(m_fee))
    
    # Check for divide by zero
    font_constant = 60
    if (m_fee_number_of_chars > 2):
        m_fee_font_size = int(font_constant/m_fee_number_of_chars)
    else:
        m_fee_font_size = 30
    #m_fee_font_size = 30
    if m_fee_number_of_chars == 3:
        m_fee_x = 29
    else:
        m_fee_x = 22
    m_fee_font = ImageFont.truetype(keep_calm_fonts_path+"KeepCalm_Medium.ttf", m_fee_font_size)
    draw_left_justified_text(disp.buffer, str(m_fee), get_inverted_x(m_fee_x,m_fee_font_size),69, 270, m_fee_font, fill=(255,255,255))
    
    # Display sat/vb text
    sat_vb_font_size = 11
    sat_vb_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", sat_vb_font_size)
    sat_vb_x=35
    draw_right_justified_text(disp.buffer, "Sat/vB", get_inverted_x(sat_vb_x,sat_vb_font_size),2, 270, sat_vb_font, fill=(255,255,255))
    
    # Display TXs Text
    tx_text_font_size = 17
    tx_text_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", tx_text_font_size)
    tx_text_x=76
    draw_left_justified_text(disp.buffer, "TXs", get_inverted_x(tx_text_x,tx_text_font_size),7, 270, tx_text_font, fill=(255,255,255))
    
    # Draw the txs box
    icon_x_size = 46
    icon_y_size = 103
    display_custom_icon(disp.buffer, images_path+'rounded_rectangle.png', (get_inverted_x(62,icon_x_size),42),icon_y_size,icon_x_size)
    
    # Display txs value
    # Calculate a font size
    txs_number_of_chars = len(str(transactions))
    
    # Check for divide by zero
    font_constant = 120
    if (txs_number_of_chars > 4):
        txs_font_size = int(font_constant/txs_number_of_chars)
    else:
        txs_font_size = 30
    #txs_font_size = 30
    txs_x = 68
    txs_font = ImageFont.truetype(keep_calm_fonts_path+"KeepCalm_Medium.ttf", txs_font_size)
    draw_left_justified_text(disp.buffer, str(transactions), get_inverted_x(txs_x,txs_font_size),50, 270, txs_font, fill=(255,255,255))
    
    # Display sat/vb text
    sat_vb_font_size = 11
    sat_vb_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", sat_vb_font_size)
    sat_vb_x=35
    draw_right_justified_text(disp.buffer, "Sat/vB", get_inverted_x(sat_vb_x,sat_vb_font_size),2, 270, sat_vb_font, fill=(255,255,255))
    
    # Display size Text
    size_text_font_size = 15
    size_text_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", size_text_font_size)
    size_text_x=106
    draw_left_justified_text(disp.buffer, "Size", get_inverted_x(size_text_x,size_text_font_size),7, 270, size_text_font, fill=(255,255,255))
    
    # Display size box
    icon_x_size = 22
    icon_y_size = 83
    display_custom_icon(disp.buffer, images_path+'rounded_rectangle.png', (get_inverted_x(104,icon_x_size),52),icon_y_size,icon_x_size)
    
    # Display the size value
    # Calculate a font size
    size_text = str(size)+ " MB"
    size_value_number_of_chars = len(size_text)
    #print("size_value_number_of_chars", size_value_number_of_chars)
    
    # Check for divide by zero
    font_constant = 112
    if (size_value_number_of_chars > 7):
        size_value_font_size = int(font_constant/size_value_number_of_chars)
    else:
        size_value_font_size = 16
    #size_value_font_size = 16
    size_value_x = 107
    size_value_font = ImageFont.truetype(keep_calm_fonts_path+"KeepCalm_Medium.ttf", size_value_font_size)
    draw_left_justified_text(disp.buffer, size_text, get_inverted_x(size_value_x,size_value_font_size),61, 270, size_value_font, fill="#f7f7f7")

# Start the display of images now.
print('Running Umbrel LCD script Version 1.0.9')
#Display umbrel logo first for 60 seconds
display_background_image('umbrel_logo.jpg')
disp.display()
time.sleep(60)

while True:
    try:  
        # First screen 60s
        disp.clear((30, 30, 49))
        draw_screen1(currency)
        disp.display()
        time.sleep(60)
        # Second screen 30s
        disp.clear((30, 30, 49))
        draw_screen2()
        disp.display()
        time.sleep(15)
        # Third screen 30s
        disp.clear((30, 30, 49))
        draw_screen3()
        disp.display()
        time.sleep(15)
    except Exception as e:
        print("Error while running main loop; ",str(e))





