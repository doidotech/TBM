#-------------------------------------------------------------------------------
# This script displays five screens :
#    1. First screen displays the logo.
#    2. Second screen has bitcoin price and satoshis per unit of the currency.
#    3. Third screen has Mempool information.
#    4. Fourth screen has the current Bitcoin block height.
#    5. Fifth screen has the current date and time
#-------------------------------------------------------------------------------

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
import datetime

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

# Currency as a global variable
currency = sys.argv[1]

# User screen options
userScreenChoices = sys.argv[2]

# Define a function to calculate an inverted x co-ordinate.
def get_inverted_x(currentX, objectSize):
    invertedX = WIDTH - (currentX + objectSize)
    return invertedX

# Define a function to calculate an x position that is
# corrected for smaller font sizes to re-center the text
# vertically inside the original bigger font space
def get_corrected_x_position(ideal_font_height,smaller_font_height,ideal_x_position):
    try:
        smaller_font_x_correction = int((ideal_font_height - smaller_font_height)/2)
        smaller_font_x_position = smaller_font_x_correction + ideal_x_position
        return smaller_font_x_position     
    except Exception as e:
        print("Error while calculating corrected x position; ",str(e))
        return ideal_x_position
    
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
    
# Define a function to get the number of unconfirmed transactions
def get_unconfirmed_txs():
    try:
        url = "https://mempool.space/api/mempool"
        json_response = urlreq.urlopen(url, context=ssl.create_default_context(cafile=certifi.where())).read()
        unconfirmed_dict = json.loads(json_response)
        #print("unconfirmed_dict: ",unconfirmed_dict)
        unconfirmed_txs = str(unconfirmed_dict['count'])
        #print("unconfirmed_txs: ",unconfirmed_txs)
        return unconfirmed_txs     
    except Exception as e:
        print("Error while getting unconfirmed txs; ",str(e))
        return ""

# Define a function to auto fit price text
def display_price_text(currency):
    try:
        # Display background
        display_background_image('Screen1@288x.png')
        # Display bitcoin icon
        display_icon(disp.buffer, images_path+'bitcoin_seeklogo.png', (80,2),27)
        # Display satoshi icon
        display_icon(disp.buffer, images_path+'Satoshi_regular_elipse.png', (27,2),27)
        # Get the price
        price = get_btc_price(currency)
        #price = 53836
        newPrice = str(price)
        # Calculate a font size
        number_of_chars = len(newPrice)
        # Check for divide by zero
        if (number_of_chars != 0):
            font_size = int(195/number_of_chars)
        else:
            font_size = 12
        #font_size = 39
        
        # Display the price
        ideal_font_height = 39
        smaller_font_height = font_size
        ideal_x_position = 79
        font_x_position =  get_corrected_x_position(ideal_font_height,smaller_font_height,ideal_x_position)
        price_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", font_size)
        draw_left_justified_text(disp.buffer, newPrice, font_x_position,30, 270, price_font, fill=(255,255,255))
        
        # Display currency
        currency_font_size = 12
        currency_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", currency_font_size)
        draw_right_justified_text(disp.buffer, currency, get_inverted_x(1,currency_font_size),4, 270, currency_font, fill=(255,255,255))
        
        # display SAT / USD string
        sat_font_size = 14
        sats_msg = "SATS / "+currency
        sat_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", sat_font_size)
        draw_left_justified_text(disp.buffer, sats_msg, get_inverted_x(111,sat_font_size),39, 270, sat_font, fill=(255,255,255))
        
        # Calculate and display SAT/USD value
        if price != 0:
            sat_per_usd_int = int(100000000/price)
        else:
            sat_per_usd_int = 0
        #sat_per_usd_int = 1679
        sat_per_usd_str = str(sat_per_usd_int)
        # Calculate a font size
        number_of_chars = len(sat_per_usd_str)
        # Check for divide by zero
        if (number_of_chars > 4):
            sat_font_size = int(200/number_of_chars)
        else:
            sat_font_size = 50
        #sat_font_size = 50
        sat_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", sat_font_size)
        ideal_font_height = 50
        smaller_font_height = sat_font_size
        ideal_x_position = 24
        font_x_position =  get_corrected_x_position(ideal_font_height,smaller_font_height,ideal_x_position)
        draw_left_justified_text(disp.buffer, sat_per_usd_str, font_x_position,30, 270, sat_font, fill=(255,255,255))
    except Exception as e:
        print("Error while creating price text; ",str(e))
        
# Define a function to display temperature
def display_temperature():
    # Measure temperature
    temp_result = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
    temp_string = temp_result.stdout.decode('utf-8')
    raw_temp = temp_string.replace("temp=","")
    raw_temp = raw_temp.replace("'C","")
    raw_temp = raw_temp.strip()
    raw_temp_float = float(raw_temp)
    raw_temp = str(int(raw_temp_float))
    #print('Raw temp: '+raw_temp)
    temperature = raw_temp.strip()+"'C"
    # display temperature
    temp_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", 12)
    draw_right_justified_text(disp.buffer, temperature, 3,3, 270, temp_font, fill=(255,255,255))
        

# Define a function to auto fit block count text
def display_block_count_text():
    try:
        # Display background
        display_background_image('Block_HeightBG.png')
        block_x_pos = 72
        # Get current bitcoin block
        btc_current_block = get_block_count()
        #btc_current_block = "682450"
        # Display the current block text
        hard_font_size = 40
        block_num_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", hard_font_size)
        draw_centered_text(disp.buffer, btc_current_block, get_inverted_x(block_x_pos,hard_font_size), 270, block_num_font, fill=(255,255,255))
    except Exception as e:
        print("Error while creating block count text; ",str(e))
    
# Define a function to draw Screen1
def draw_screen1(currency):
    # Display current bitcoin price
    display_price_text(currency)
    # Display temperature
    display_temperature()
    
    
# Define a function to draw Screen2
def draw_screen2():
    # Get all the data from APIs
    fees_dict = get_recommended_fees()
    next_block_dict = get_next_block_info()
    unconfirmed_txs = get_unconfirmed_txs()
    
    # Display background
    display_background_image('TxsBG.png')
    
    # Get the low and high fees
    high = int(fees_dict['fastestFee'])
    low = int(fees_dict['hourFee'])
    
    # Calculate a font size for the low value
    low_number_of_chars = len(str(low))
    # Check for divide by zero
    font_constant = 86
    if (low_number_of_chars > 2):
        low_font_size = int(font_constant/low_number_of_chars)
    else:
        low_font_size = 43
    #low_font_size = 43
        
    # Calculate a font size for the high value
    high_number_of_chars = len(str(high))
    # Check for divide by zero
    if (high_number_of_chars > 2):
        high_font_size = int(font_constant/high_number_of_chars)
    else:
        high_font_size = 43
    #fees_font_size = 38
        
    # Set x position depending on font size
    if low_number_of_chars == 3:
        low_fee_x = 90
    else:
        low_fee_x = 85
    #low_fee_x = 85
    if high_number_of_chars == 3:
        high_fee_x = 90
    else:
        high_fee_x = 85
        
    # Display the low and high fees
    low_fees_font = ImageFont.truetype(keep_calm_fonts_path+"KeepCalm_Medium.ttf", low_font_size)
    high_fees_font = ImageFont.truetype(keep_calm_fonts_path+"KeepCalm_Medium.ttf", high_font_size)
    draw_left_justified_text(disp.buffer, str(low), low_fee_x,9, 270, low_fees_font, fill=(255,255,255))
    draw_left_justified_text(disp.buffer, str(high), high_fee_x,88, 270, high_fees_font, fill=(255,255,255))
    
    # Get the number of transactions
    transactions = int(next_block_dict['nTx'])
    # Calculate a font size
    txs_number_of_chars = len(str(transactions))
    font_constant = 112
    if (txs_number_of_chars > 4):
        txs_font_size = int(font_constant/txs_number_of_chars)
    else:
        txs_font_size = 28
    #txs_font_size = 28
        
    # Display the transactions
    txs_x = 43
    txs_font = ImageFont.truetype(keep_calm_fonts_path+"KeepCalm_Medium.ttf", txs_font_size)
    draw_left_justified_text(disp.buffer, str(transactions), txs_x,67, 270, txs_font, fill=(255,255,255))
    
    # Get the number of unconfirmed transactions
    unconfirmed_txs_number_of_chars = len(unconfirmed_txs)
    
    # Calculate a font size
    font_constant = 120
    if (unconfirmed_txs_number_of_chars > 5):
        unconfirmed_txs_font_size = int(font_constant/unconfirmed_txs_number_of_chars)
    else:
        unconfirmed_txs_font_size = 24
    #unconfirmed_txs_font_size = 20
        
    # Display the number of unconfirmed transactions
    unconfirmed_txs_x = 7
    unconfirmed_txs_font = ImageFont.truetype(keep_calm_fonts_path+"KeepCalm_Medium.ttf", unconfirmed_txs_font_size)
    draw_left_justified_text(disp.buffer, unconfirmed_txs, unconfirmed_txs_x,64, 270, unconfirmed_txs_font, fill=(255,255,255))


# Define a function to draw Screen3
def draw_screen3():
    # Display block count
    display_block_count_text()
    
    
# Define a function to draw Screen4
def draw_screen4():
    # Display background
    display_background_image('Screen1@288x.png')

    # Get current date and time
    current_date_and_time = datetime.datetime.now()
    #Convert time object to AM/PM format
    time_string = current_date_and_time.strftime('%-I:%M %p')
    # Get the day
    day_string = current_date_and_time.strftime('%A')
    # Get the month
    month_string = current_date_and_time.strftime('%B %d')
    
    # Display the time
    time_font_size = 30
    time_font = ImageFont.truetype(keep_calm_fonts_path+"keep_calm_regular.ttf", time_font_size)
    draw_centered_text(disp.buffer, time_string, get_inverted_x(16,time_font_size), 270, time_font, fill=(255,255,255))
    
    # Display week day
    day_font_size = 26
    day_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", day_font_size)
    draw_centered_text(disp.buffer, day_string, get_inverted_x(59,day_font_size), 270, day_font, fill=(255,255,255))
    
    # Display the month
    month_font_size = 22
    month_font = ImageFont.truetype(made_tommy_fonts_path+"MADE_TOMMY_Bold_PERSONAL_USE.otf", month_font_size)
    draw_centered_text(disp.buffer, month_string, get_inverted_x(91,month_font_size), 270, month_font, fill=(255,255,255))
    
    

# Start the display of images now.
print('Running MyNode LCD script Version 1.0.10')
#Display umbrel logo first for 60 seconds
display_background_image('Mynode_Bootscreen.png')
disp.display()
time.sleep(15)

# Display other screens in a loop
while True:
    try:  
        # First screen 60s
        if "Screen1" in userScreenChoices:
            disp.clear((255, 255, 255))
            draw_screen1(currency)
            disp.display()
            time.sleep(60)
        # Second screen 30s
        if "Screen2" in userScreenChoices:
            disp.clear((255, 255, 255))
            draw_screen2()
            disp.display()
            time.sleep(30)
        # Third screen 30s
        if "Screen3" in userScreenChoices:
            disp.clear((255, 255, 255))
            draw_screen3()
            disp.display()
            time.sleep(30)
        # Fourth screen 30s
        if "Screen4" in userScreenChoices:
            disp.clear((255, 255, 255))
            draw_screen4()
            disp.display()
            time.sleep(30)
    except Exception as e:
        print("Error while running main loop; ",str(e))





