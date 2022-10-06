#-------------------------------------------------------------------------------
#   Copyright (c) 2022 DOIDO Technologies
#   Version  : 2.0.1
#   Location : github
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
# This script displays eight screens on your Umbrel Node:
#    1. First screen displays the umbrel logo.
#    2. Second screen has bitcoin price and satoshis per unit of
#       the currency used.
#    3. Third screen has information about the next bitcoin block.
#    4. Fourth screen has the current Bitcoin block height.
#    5. Fifth screen has the current date and time.
#    6. Sixth screen has the bitcoin network information.
#    7. Seventh screen has the payment channels information.
#    8. Eighth screen has the Node disk storage information.
#    9. First screen is displayed once for 60 seconds.
#   10. The second to eighth screens are displayed in a loop; second screen 
#       is displayed for 60 seconds, third to eighth screens for 30 seconds 
#       each.   
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
from connections import test_tor, tor_request
import os
basedir = os.path.abspath(os.path.dirname(__file__))
import configparser
import requests

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
    port=SPI_PORT,
    cs=SPI_DEVICE,
    dc=DC,
    rst=RST,
    rotation=0,
    spi_speed_hz=SPEED_HZ,
    rgb=False,
    invert=False 
)

# The display buffer
disp.buffer = Image.new('RGB', (WIDTH, HEIGHT))

# Shape drawing object
draw = ImageDraw.Draw(disp.buffer)

# Initialize display.
disp.begin()

# Get directory of the executing script
filePath=str(pathlib.Path(__file__).parent.absolute())

# customizable images path
images_path = filePath+'/images/'

# Customizable fonts path
poppins_fonts_path = filePath+'/poppins/'

# Currency as a global variable
currency = sys.argv[1]
#currency = "USD"

# User screen options
userScreenChoices = sys.argv[2]
#userScreenChoices = "Screen1,Screen2,Screen3,Screen4,Screen5,Screen6,Screen7"

# Initial mempool url
mempool_url = "https://mempool.space"

# Mainnet or testnet settings
blockchain_type = "mainnet"

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
    """Gets current block height in the longest chain."""
        
    try:
        url = "https://blockchain.info/q/getblockcount"
        currentBlock = tor_request(url)
        currentBlockString = currentBlock.text
        #print("Current block: " + currentBlockString)
        return currentBlockString
    except Exception as err:
        print("Error while getting current block: "+ str(err))
        return ""
    
# Define a function to get bitcoin price
def get_btc_price(currency):
    """Gets bitcoin price."""
        
    try:
        # Currency is passed as an argument when running the file   
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies="+currency
        currentPrice = tor_request(url)
        coin_prices_dict = json.loads(currentPrice.text)
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
    """Gets the the recommended fees."""
        
    try:
        #url = "https://mempool.space/api/v1/fees/recommended"
        url = mempool_url + "/api/v1/fees/recommended"
        #print("get_recommended_fees(mempool_url)",url)
        json_response = tor_request(url)
        fees_dict = json.loads(json_response.text)
        #print("fees_dict: ",fees_dict)
        return fees_dict      
    except Exception as e:
        print("Error while getting recommended fees; ",str(e))
        return ""
    
# Define a function get the the next block info
def get_next_block_info():
    """Gets the the next block info."""
        
    try:
        #url = "https://mempool.space/api/v1/fees/mempool-blocks"
        url = mempool_url + "/api/v1/fees/mempool-blocks"
        #print("get_next_block_info(mempool_url)",url)
        json_response = tor_request(url)
        blocks_dict = json.loads(json_response.text)
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
    """Gets the number of unconfirmed transactions."""
        
    try:
        #url = "https://mempool.space/api/mempool"
        url = mempool_url + "/api/mempool"
        #print("get_unconfirmed_txs(mempool_url)",url)
        json_response = tor_request(url)
        unconfirmed_dict = json.loads(json_response.text)
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
        price_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", font_size)
        draw_left_justified_text(disp.buffer, newPrice, font_x_position,30, 270, price_font, fill=(255,255,255))
        
        # Display currency
        currency_font_size = 12
        currency_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", currency_font_size)
        draw_right_justified_text(disp.buffer, currency, get_inverted_x(1,currency_font_size),4, 270, currency_font, fill=(255,255,255))
        
        # display SAT / USD string
        sat_font_size = 14
        sats_msg = "SATS / "+currency
        sat_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", sat_font_size)
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
        sat_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", sat_font_size)
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
    temp_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", 12)
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
        block_num_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", hard_font_size)
        draw_centered_text(disp.buffer, btc_current_block, get_inverted_x(block_x_pos,hard_font_size), 270, block_num_font, fill=(255,255,255))
    except Exception as e:
        print("Error while creating block count text; ",str(e))
        
def get_tor_status():
    """Checks if tor is running."""
        
    try:
        tor = test_tor()
        if tor['status']:
            print("Tor Connected")
            return True
        else:
            print("Could not connect to Tor. The LCD application requires Tor to run.")
            return False    
    except Exception as e:
        print("Error while getting Tor status; ",str(e))
        return False
        
def load_config(quiet=False):
    """Loads the config file."""
        
    # Load Config
    basedir = os.path.abspath(os.path.dirname(__file__))
    config_file = os.path.join(basedir, 'config.ini')
    CONFIG = configparser.ConfigParser()
    if quiet:
        CONFIG.read(config_file)
        return (CONFIG)


    # Check that config file exists
    if os.path.isfile(config_file):
        CONFIG.read(config_file)
        return (CONFIG)
    else:
        print("LCD app requires config.ini to run")
            
def check_umbrel_and_mempool():
    """Checks for local mempool app."""
        
    #  Try to ping umbrel.local and check for installed apps
    umbrel = False
    mempool = False
    config = load_config(True)
    config_file = os.path.join(basedir, 'config.ini')
    try:
        url = config['UMBREL']['url']
    except Exception:
        url = 'http://umbrel.local/'

        # Test if this url can be reached
        try:
            result = tor_request(url)
            if not isinstance(result, requests.models.Response):
                raise Exception(f'Did not get a return from {url}')
            if not result.ok:
                raise Exception(f'Reached {url} but an error occured.')
            # Umbrel found
            umbrel = True
        except Exception as e:
            # Umbrel not found
            print("    Umbrel not found:" + str(e))

    if umbrel:
        if 'onion' in url:
            url_parsed = ['[Hidden Onion address]']
        else:
            url_parsed = url
            
        # Checking if Mempool.space app is installed"
        try:
            url = config['MEMPOOL']['url']
        except Exception:
            url = 'http://umbrel.local:3006/'
        try: 
            result = tor_request(url)
            if not isinstance(result, requests.models.Response):
                raise Exception('Did not get a return from http://umbrel.local:3006/')
            if not result.ok:
                raise Exception('Reached Mempool app but an error occured.')

            block_height = tor_request(url +'/api/blocks/tip/height').json()
            # Found mempool
            mempool = True
        except Exception as e:
            # Mempool not found
            print("Mempool not found:" + str(e))

    if mempool:
        return True
    else:
        return False
        
def get_mempool_base_url():
    """Determines the mempool base url."""
        
    mempool_status = check_umbrel_and_mempool()
    print(f"Local Mempool app status = {mempool_status}")
        
    if mempool_status:
        # return local mempool app url
        return "http://umbrel.local:3006"
    else:
        # return web app mempool url
        return "https://mempool.space"


def classify_bytes(num_of_bytes):
    """Converts number to convenient units of bytes"""

    num_of_bytes = int(num_of_bytes)
    #print(num_of_bytes)

    one_terabyte = 1000*1000*1000*1000
    one_gigabyte = 1000*1000*1000
    one_megabyte = 1000*1000
    one_kilobyte = 1000


    if num_of_bytes > one_terabyte:
        # Terabytes
        terabytes = round(num_of_bytes/one_terabyte)
        terabytes_string = "{0} TB".format(terabytes)
        return terabytes_string
    elif num_of_bytes > one_gigabyte:
        # Gigabytes
        gigabytes = round(num_of_bytes/one_gigabyte)
        gigabytes_string = "{0} GB".format(gigabytes)
        return gigabytes_string
    elif num_of_bytes > one_megabyte:
        # Megabytes
        megabytes = round(num_of_bytes/one_megabyte)
        megabytes_string = "{0} MB".format(megabytes)
        return megabytes_string
    elif num_of_bytes > one_kilobyte:
        # Kilobytes
        kilobytes = round(num_of_bytes/one_kilobyte)
        kilobytes_string = "{0} KB".format(kilobytes)
        return kilobytes_string
    else:
        # Bytes
        bytes_string = "{0} B".format(num_of_bytes)
        return bytes_string


def get_blockchain_size():
    """Gets blockchain size"""

    global blockchain_type
    try:
        # Command is basted on blockchain network type
        if blockchain_type == "test":
            command = "docker exec bitcoin_bitcoind_1 bitcoin-cli -chain=test getblockchaininfo"
        else:
            command = "docker exec bitcoin_bitcoind_1 bitcoin-cli getblockchaininfo"

        response = subprocess.run(command.split(), stdout=subprocess.PIPE)
        size_data = response.stdout.decode('utf-8')
        #print(size_data)
        size_dictionary = json.loads(size_data)
        #print(size_dictionary)

        size_on_disk = int(size_dictionary["size_on_disk"])
        #print("size_on_disk: ",size_on_disk)

        # Blockchain type; mainnet or testnet
        blockchain_type = size_dictionary["chain"]
        #print("blockchain_type: ",blockchain_type)
        size_on_disk = classify_bytes(size_on_disk)
        return size_on_disk
    except Exception as e:
        print("Error while getting blockchain size; ",str(e))
        return False

def get_connection_count():
    """Gets the number of peers"""
    try:
        # Command is basted on blockchain network type
        if blockchain_type == "test":
            command = "docker exec bitcoin_bitcoind_1 bitcoin-cli -chain=test getconnectioncount"
        else:
            command = "docker exec bitcoin_bitcoind_1 bitcoin-cli getconnectioncount"

        response = subprocess.run(command.split(), stdout=subprocess.PIPE)
        connection_count = response.stdout.decode('utf-8')
        return int(connection_count)
    except Exception as e:
        print("Error while getting number of peers; ",str(e))
        return False

def get_mempool_info():
    """Gets mempool number of bytes"""

    try:
        # Command is basted on blockchain network type
        if blockchain_type == "test":
            command = "docker exec bitcoin_bitcoind_1 bitcoin-cli -chain=test getmempoolinfo"
        else:
            command = "docker exec bitcoin_bitcoind_1 bitcoin-cli getmempoolinfo"

        response = subprocess.run(command.split(), stdout=subprocess.PIPE)
        mempool_info = response.stdout.decode('utf-8')
        #print(mempool_info)
        mempool_info_dictionary = json.loads(mempool_info)
        #print(mempool_info_dictionary)

        mempool_bytes= int(mempool_info_dictionary["bytes"])
        #print("mempool_bytes: ",mempool_bytes)

        mempool_bytes_string = classify_bytes(mempool_bytes)
        return mempool_bytes_string
    except Exception as e:
        print("Error while getting mempool bytes; ",str(e))
        return False

def get_network_hash_ps():
    """Gets the number of hetwork hashes per second"""

    one_kilo_hash = 1000
    one_mega_hash = 1000000
    one_giga_hash = 1000000000
    one_tera_hash = 1000000000000
    one_peta_hash = 1000000000000000
    one_exa_hash = 1000000000000000000
    one_zeta_hash = 1000000000000000000000
    one_yotta_hash = 1000000000000000000000000

    try:
        # Command is basted on blockchain network type
        if blockchain_type == "test":
            command = "docker exec bitcoin_bitcoind_1 bitcoin-cli -chain=test getnetworkhashps"
        else:
            command = "docker exec bitcoin_bitcoind_1 bitcoin-cli getnetworkhashps"
        
        response = subprocess.run(command.split(), stdout=subprocess.PIPE)
        hash_per_second = float(response.stdout.decode('utf-8'))
        #print(hash_per_second)

        # Classify the hashrate
        if hash_per_second > one_yotta_hash:
            # yotta hash
            yotta_hash = round(hash_per_second/one_yotta_hash)
            yotta_hash_string = "{0} YH/s".format(yotta_hash)
            return yotta_hash_string
        elif hash_per_second > one_zeta_hash:
            # zeta hash
            zeta_hash = round(hash_per_second/one_zeta_hash)
            zeta_hash_string = "{0} ZH/s".format(zeta_hash)
            return zeta_hash_string
        elif hash_per_second > one_exa_hash:
            # exa hash
            exa_hash = round(hash_per_second/one_exa_hash)
            exa_hash_string = "{0} EH/s".format(exa_hash)
            return exa_hash_string
        elif hash_per_second > one_peta_hash:
            # peta hash
            peta_hash = round(hash_per_second/one_peta_hash)
            peta_hash_string = "{0} PH/s".format(peta_hash)
            return peta_hash_string
        elif hash_per_second > one_tera_hash:
            # tera hash
            tera_hash = round(hash_per_second/one_tera_hash)
            tera_hash_string = "{0} TH/s".format(tera_hash)
            return tera_hash_string
        elif hash_per_second > one_giga_hash:
            # giga hash
            giga_hash = round(hash_per_second/one_giga_hash)
            giga_hash_string = "{0} GH/s".format(giga_hash)
            return giga_hash_string
        elif hash_per_second > one_mega_hash:
            # mega hash
            mega_hash = round(hash_per_second/one_mega_hash)
            mega_hash_string = "{0} MH/s".format(mega_hash)
            return mega_hash_string
        elif hash_per_second > one_kilo_hash:
            # kilo_hash
            kilo_hash = round(hash_per_second/one_kilo_hash)
            kilo_hash_string = "{0} kH/s".format(kilo_hash)
            return kilo_hash_string
        else:
            # hash
            hash_string = "{0} H/s".format(hash_per_second)
            return hash_string
    except Exception as e:
        print("Error while getting hash rate; ",str(e))
        return False

def remove_extra_spaces(the_string):
    """Removes extra spaces in a string"""

    # Convert string to list
    string_list = list(the_string.strip())
    # Stores previous character
    previous_char = ""

    # Loop, replacing spaces that have a right side space neighbor
    for i in range(len(string_list)):
        if i == 0:
            previous_char = string_list[i]
        else:
            if(previous_char == ' ')and(string_list[i] == ' '):
                # remove extra space
                string_list[i] = ''
            else:
                previous_char = string_list[i]

    string_from_list = "".join(string_list)

    return string_from_list

def classify_kilo_bytes(num_of_bytes):
    """Converts kilobytes to convenient units of bytes"""

    num_of_bytes = int(num_of_bytes)*1024
    #print(num_of_bytes)

    one_terabyte = 1000*1000*1000*1000
    one_gigabyte = 1000*1000*1000
    one_megabyte = 1000*1000
    one_kilobyte = 1000


    if num_of_bytes > one_terabyte:
        # Terabytes
        terabytes = num_of_bytes/one_terabyte
        terabytes_string = "{:.1f} TB".format(terabytes)
        return terabytes_string
    elif num_of_bytes > one_gigabyte:
        # Gigabytes
        gigabytes = num_of_bytes/one_gigabyte
        gigabytes_string = "{:.1f} GB".format(gigabytes)
        return gigabytes_string
    elif num_of_bytes > one_megabyte:
        # Megabytes
        megabytes = num_of_bytes/one_megabyte
        megabytes_string = "{:.1f} MB".format(megabytes)
        return megabytes_string
    elif num_of_bytes > one_kilobyte:
        # Kilobytes
        kilobytes = num_of_bytes/one_kilobyte
        kilobytes_string = "{:.1f} KB".format(kilobytes)
        return kilobytes_string
    else:
        # Bytes
        bytes_string = "{0} B".format(num_of_bytes)
        return bytes_string

def get_disk_storage_info():
    """Gets information on how the disk is used"""

    try:
        command = "df /dev/sda1"
        response = subprocess.run(command.split(), stdout=subprocess.PIPE)
        disk_info = response.stdout.decode('utf-8')
        #print("disk_info: ",disk_info)

        disk_info_array = disk_info.split('\n')
        #print("disk_info_array: ",disk_info_array)
        usage_string = disk_info_array[1]
        #print("usage_string: ",usage_string)
        cleaned_usage_string = remove_extra_spaces(usage_string)
        #print("cleaned_usage_string: ",cleaned_usage_string)
        usage_list = cleaned_usage_string.split()
        disk_capacity = classify_kilo_bytes(int(usage_list[1]))
        #print("disk_capacity: ",disk_capacity)
        used_space = classify_kilo_bytes(int(usage_list[2]))
        #print("used_space: ",used_space)
        #available_space = classify_kilo_bytes(int(usage_list[3]))
        available_space = classify_kilo_bytes(int(usage_list[1]) - int(usage_list[2]))
        #print("available_space: ",available_space)
        used_percentage = int(usage_list[4].replace("%",""))
        #print("used_percentage: ",used_percentage)

        storage_info = [disk_capacity,used_space,available_space,used_percentage]
        return storage_info
    except Exception as e:
        print("Error while getting disk information; ",str(e))
        return False

def get_lnd_info():
    """Gets the lnd connections and active channels"""

    try:
        # Command is basted on blockchain network type
        if blockchain_type == "test":
            command = "docker exec lightning_lnd_1 lncli --network=testnet getinfo"
        else:
            command = "docker exec lightning_lnd_1 lncli --network=mainnet getinfo"

        response = subprocess.run(command.split(), stdout=subprocess.PIPE)
        lnd_info = response.stdout.decode('utf-8')
        lnd_info_dictionary = json.loads(lnd_info)

        connections = int(lnd_info_dictionary['num_peers'])
        #print("connections: ",connections)
        active_channels = int(lnd_info_dictionary['num_active_channels'])
        #print("active_channels: ",active_channels)
        return connections,active_channels
    except Exception as e:
        print("Error while getting number of lnd peers and active channels; ",str(e))
        return False


def classify_satoshis(num_of_satoshis):
    """
        Converts satoshis to convenient units of
        bitcoin or satoshis
    """
    
    num_of_satoshis = int(num_of_satoshis)
    #print(num_of_satoshis)
    
    # Unit        Number of satoshis
    one_bitcoin = 100000000 # 1 bitcoin = 100,000,000 satoshis
    megaBitcoin = 1000000*one_bitcoin
    kiloBitcoin = 1000*one_bitcoin
    kiloSatoshi = 1000
    
    if num_of_satoshis >= megaBitcoin:
        # megaBitcoin
        mega_bitcoin = round(num_of_satoshis/megaBitcoin)
        mega_bitcoin_string = "{0} MBTC".format(mega_bitcoin)
        return mega_bitcoin_string
    elif num_of_satoshis >= kiloBitcoin:
        # kiloBitcoin
        kilo_bitcoin = round(num_of_satoshis/kiloBitcoin)
        kilo_bitcoin_string = "{0} kBTC".format(kilo_bitcoin)
        return kilo_bitcoin_string
    elif num_of_satoshis >= one_bitcoin:
        # Bitcoins
        num_bitcoins = round(num_of_satoshis/one_bitcoin)
        num_bitcoins_string = "{0} BTC".format(num_bitcoins)
        return num_bitcoins_string
    elif num_of_satoshis >= kiloSatoshi:
        # kiloSatoshi
        kilo_satoshi = round(num_of_satoshis/kiloSatoshi)
        kilo_satoshi_string = "{0} kSats".format(kilo_satoshi)
        return kilo_satoshi_string
    else:
        # Satoshis
        satoshi_string = "{0} Sats".format(num_of_satoshis)
        return satoshi_string


def get_lnd_channel_balance():
    """Gets the lnd wallet max send, max receive balance."""

    try:
        # Command is basted on blockchain network type
        if blockchain_type == "test":
            command = "docker exec lightning_lnd_1 lncli --network=testnet channelbalance"
        else:
            command = "docker exec lightning_lnd_1 lncli --network=mainnet channelbalance"

        response = subprocess.run(command.split(), stdout=subprocess.PIPE)
        channel_balance_info = response.stdout.decode('utf-8')
        channel_balance_dictionary = json.loads(channel_balance_info)

        # Max send
        local_balance_dict = channel_balance_dictionary['local_balance']
        max_send = classify_satoshis(int(local_balance_dict['sat']))
        #print("max_send: ",max_send)
        # Max receive
        remote_balance_dict = channel_balance_dictionary['remote_balance']
        max_receive= classify_satoshis(int(remote_balance_dict['sat']))
        #print("max_receive: ",max_receive)
        return max_send,max_receive
    except Exception as e:
        print("Error while getting lnd wallet max send and max receive balance; ",str(e))
        return False

def get_btc_network():
    """
        Get's BTC network indirectly from the docker command
        that was used with bitcoin nd
    """

    try:
        global blockchain_type
        command = ["docker","ps","--filter","name=bitcoin_bitcoind_1"]
        response = subprocess.run(command, stdout=subprocess.PIPE)
        docker_info = response.stdout.decode('utf-8')
        #print("docker_info: ",docker_info)

        if "-chain=tes" in docker_info:
            #print("We are using testnet")
            blockchain_type = "test"
        else:
            #print("We are using mainnet")
            blockchain_type = "main"
    except Exception as e:
        print("Error while getting BTC network type; ",str(e))


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
    low_fees_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", low_font_size)
    high_fees_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", high_font_size)
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
    txs_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", txs_font_size)
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
    unconfirmed_txs_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", unconfirmed_txs_font_size)
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
    time_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", time_font_size)
    draw_centered_text(disp.buffer, time_string, get_inverted_x(16,time_font_size), 270, time_font, fill=(255,255,255))
    
    # Display week day
    day_font_size = 26
    day_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", day_font_size)
    draw_centered_text(disp.buffer, day_string, get_inverted_x(59,day_font_size), 270, day_font, fill=(255,255,255))
    
    # Display the month
    month_font_size = 22
    month_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", month_font_size)
    draw_centered_text(disp.buffer, month_string, get_inverted_x(91,month_font_size), 270, month_font, fill=(255,255,255))
    
    
def draw_screen5():
    """Displays the bitcoin network information"""
    
    # Display background
    #display_background_image('network_sample.jpg')
    display_background_image('network.png')
        
    # connection count
    connection_count = get_connection_count()
    #connection_count = 999

    # Display the number of peers
    connection_count_x = 68
    connections_number_of_chars = len(str(connection_count))
    if connections_number_of_chars == 2:
        connection_count_y = 23
    elif connections_number_of_chars == 1:
        connection_count_y = 27
    else:
        connection_count_y = 19
        
    connection_count_font_size = 15
    connection_count_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", connection_count_font_size)
    draw_left_justified_text(disp.buffer, str(connection_count), connection_count_x,connection_count_y, 270, connection_count_font, fill=(255,255,255))
    
    # mempool bytes
    mempool_bytes_data = get_mempool_info()
    #mempool_bytes_data = "999 KB"
    mempool_bytes = mempool_bytes_data.split()[0]
    mempool_bytes_units = mempool_bytes_data.split()[1]
    # Display the number of mempool bytes
    mempool_bytes_x = 68
    mempool_bytes_number_of_chars = len(str(mempool_bytes))
    if mempool_bytes_number_of_chars == 2:
        mempool_bytes_y = 101
    elif mempool_bytes_number_of_chars == 1:
        mempool_bytes_y = 108
    else:
        mempool_bytes_y = 98
        
    mempool_bytes_font_size = 15
    mempool_bytes_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", mempool_bytes_font_size)
    draw_left_justified_text(disp.buffer, str(mempool_bytes), mempool_bytes_x,mempool_bytes_y, 270, mempool_bytes_font, fill=(255,255,255))
    
    # Display mempool bytes units
    mempool_units_font_size = 9
    mempool_units_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", mempool_units_font_size)
    draw_left_justified_text(disp.buffer, mempool_bytes_units, 55,105, 270, mempool_units_font, fill=(255,255,255))
    draw_left_justified_text(disp.buffer, "Peers", 55,22, 270, mempool_units_font, fill=(255,255,255))

    # Hash rate
    network_hash_rate_data = get_network_hash_ps()
    #network_hash_rate_data = "999 EH/s"
    network_hash_rate = network_hash_rate_data.split()[0]
    network_hash_rate_units = network_hash_rate_data.split()[1]
    # Display the value of network hash rate
    network_hash_rate_x = 22
    network_hash_rate_number_of_chars = len(str(network_hash_rate))
    if network_hash_rate_number_of_chars == 2:
        network_hash_rate_y = 23
    elif network_hash_rate_number_of_chars == 1:
        network_hash_rate_y = 27
    else:
        network_hash_rate_y = 19

    network_hash_rate_font_size = 15
    network_hash_rate_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", network_hash_rate_font_size)
    draw_left_justified_text(disp.buffer, str(network_hash_rate), network_hash_rate_x,network_hash_rate_y, 270, network_hash_rate_font, fill=(255,255,255))
    
    # Display network hash rate units
    network_hash_rate_units_font_size = 9
    network_hash_rate_units_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", network_hash_rate_units_font_size)
    draw_left_justified_text(disp.buffer, network_hash_rate_units, 8,22, 270, network_hash_rate_units_font, fill=(255,255,255))
    
    
    # Blockchain size
    blockchain_size_data = get_blockchain_size()
    #blockchain_size_data = "999 MB"
    blockchain_size = blockchain_size_data.split()[0]
    blockchain_size_units = blockchain_size_data.split()[1]
    # Display the value of blockchain size
    blockchain_size_x = 22
    blockchain_size_number_of_chars = len(str(blockchain_size))
    if blockchain_size_number_of_chars == 2:
        blockchain_size_y = 101
    elif blockchain_size_number_of_chars == 1:
        blockchain_size_y = 108
    else:
        blockchain_size_y = 98
        
    blockchain_size_font_size = 15
    blockchain_size_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", blockchain_size_font_size)
    draw_left_justified_text(disp.buffer, str(blockchain_size), blockchain_size_x,blockchain_size_y, 270, blockchain_size_font, fill=(255,255,255))
    
    # Display blockchain size units
    blockchain_size_units_font_size = 9
    blockchain_size_units_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", blockchain_size_units_font_size)
    draw_left_justified_text(disp.buffer, blockchain_size_units, 8,105, 270, blockchain_size_units_font, fill=(255,255,255))
    
def draw_screen6():
    """Displays the payment channels information"""
    
    # Display background
    #display_background_image('payment_channels_sample.jpg')
    display_background_image('payment_channels.png')
    
    # lnd connections and active channels
    connections,active_channels = get_lnd_info()
    #connections,active_channels = 999,999
    
    # Connections
    connection_count = connections
    # Display the number of peers
    connection_count_x = 68
    connections_number_of_chars = len(str(connection_count))
    if connections_number_of_chars == 2:
        connection_count_y = 23
    elif connections_number_of_chars == 1:
        connection_count_y = 27
    else:
        connection_count_y = 19
        
    connection_count_font_size = 15
    connection_count_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", connection_count_font_size)
    draw_left_justified_text(disp.buffer, str(connection_count), connection_count_x,connection_count_y, 270, connection_count_font, fill=(255,255,255))
    
    # Active channels
    active_channels_x = 68
    active_channels_number_of_chars = len(str(active_channels))
    if active_channels_number_of_chars == 2:
        active_channels_y = 101
    elif active_channels_number_of_chars == 1:
        active_channels_y = 108
    else:
        active_channels_y = 98
        
    active_channels_font_size = 15
    active_channels_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", active_channels_font_size)
    draw_left_justified_text(disp.buffer, str(active_channels), active_channels_x,active_channels_y, 270, active_channels_font, fill=(255,255,255))

    # Display Connections and active channels units
    connections_units_font_size = 9
    connections_units_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", connections_units_font_size)
    draw_left_justified_text(disp.buffer, "Channels", 55,98, 270, connections_units_font, fill=(255,255,255))
    draw_left_justified_text(disp.buffer, "Peers", 55,22, 270, connections_units_font, fill=(255,255,255))
    
    # lnd wallet max send and max receive
    temp_max_send,temp_max_receive = get_lnd_channel_balance()
    #temp_max_send,temp_max_receive = classify_satoshis(10000000),classify_satoshis(10000000)
    #temp_max_send,temp_max_receive = "999999 kSats","999999 kSats"
    # ToDo :work out max receive in 1000s of units e.g Kilo satoshis
    max_send = temp_max_send.split()[0]
    max_send_units = temp_max_send.split()[1]
    max_receive = temp_max_receive.split()[0]
    max_receive_units = temp_max_receive.split()[1]
    
    # Max send
    max_send_x = 22
    max_send_number_of_chars = len(str(max_send))
    if max_send_number_of_chars == 1:
        max_send_y = 27
    elif max_send_number_of_chars == 2:
        max_send_y = 23
    elif max_send_number_of_chars == 3:
        max_send_y = 19
    elif max_send_number_of_chars == 4:
        max_send_y = 15
    elif max_send_number_of_chars == 5:
        max_send_y = 10
    else:
        max_send_y = 6
        
    max_send_font_size = 15
    max_send_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", max_send_font_size)
    draw_left_justified_text(disp.buffer, str(max_send), max_send_x,max_send_y, 270, max_send_font, fill=(255,255,255))
    
    # Max receive
    max_receive_x = 22
    max_receive_number_of_chars = len(str(max_receive))
    if max_receive_number_of_chars == 1:
        max_receive_y = 108
    elif max_receive_number_of_chars == 2:
        max_receive_y = 101
    elif max_receive_number_of_chars == 3:
        max_receive_y = 98
    elif max_receive_number_of_chars == 4:
        max_receive_y = 93
    elif max_receive_number_of_chars == 5:
        max_receive_y = 90
    else:
        max_receive_y = 90
        
    max_receive_font_size = 15
    max_receive_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", max_receive_font_size)
    draw_left_justified_text(disp.buffer, str(max_receive), max_receive_x,max_receive_y, 270, max_receive_font, fill=(255,255,255))
    
    # Display max send and max receive bitcoin units
    bitcoin_units_font_size = 10
    bitcoin_units_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", bitcoin_units_font_size)
    draw_left_justified_text(disp.buffer, max_receive_units, 8,100, 270, bitcoin_units_font, fill=(255,255,255))
    draw_left_justified_text(disp.buffer, max_send_units, 8,22, 270, bitcoin_units_font, fill=(255,255,255))
   
def draw_screen7():
    """Displays the disk storage information"""
    
    # Display background
    #display_background_image('storage_sample.jpg')
    display_background_image('storage.png')
    
    # Disk usage info
    storage_info = get_disk_storage_info()
    #storage_info = ["983.4 GB","565.2 GB","418.2 GB",67]
    
    # Display used space
    used_space = storage_info[1]
    used_space_font_size = 20
    used_space_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", used_space_font_size)
    draw_left_justified_text(disp.buffer, used_space, 59,7, 270, used_space_font, fill=(255,255,255))
    
    # Display space capacity
    disk_capacity = storage_info[0]
    disk_capacity_string = "Used out of "+ disk_capacity
    disk_capacity_font_size = 11
    disk_capacity_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", disk_capacity_font_size)
    draw_left_justified_text(disp.buffer, disk_capacity_string, 44,7, 270, disk_capacity_font, fill=(255,255,255))
    
    # Display available space
    available_space = storage_info[2]
    available_space_string = available_space+" available"
    available_space_font_size = 11
    available_space_font = ImageFont.truetype(poppins_fonts_path+"Poppins-Bold.ttf", available_space_font_size)
    #draw_left_justified_text(disp.buffer, available_space, 30,57, 270, available_space_font, fill=(255,255,255))
    draw_right_justified_text(disp.buffer, available_space_string, 13,11, 270, available_space_font, fill=(255,255,255))
    
    # Progress bar
    width = 2
    height = 140
    x = 29
    y = 7
    used_percentage = int(storage_info[3])
    inner_bar_height = int((used_percentage*height)/100)+y
    draw.rectangle((x, y, width+x, height+y), outline=(255, 255, 255), fill=(255, 255, 255))
    draw.rectangle((x, y, width+x, inner_bar_height), outline=(0, 160, 0), fill=(0, 160, 0))
    
    
         
# Start the display of images now.
print('Running Umbrel 1.8 Inch LCD script Version 2.0.1')

#Display umbrel logo first for 60 seconds
display_background_image('umbrel_logo.png')
disp.display(disp.buffer)
time.sleep(60)

# An initial check if Tor is running
tor_status = get_tor_status()

# Initial check for umbrel and mempool
mempool_status = check_umbrel_and_mempool()
print(f"Local Mempool app status = {mempool_status}")

# Display other screens in a loop
while True:
    # Get BTC network; testnet or mainnet
    get_btc_network()
    
    # First screen 60s
    try:
        # Set mempool url
        mempool_url = get_mempool_base_url()
        print(f"current_mempool_url = {mempool_url}")
                
        if "Screen1" in userScreenChoices:
            draw_screen1(currency)
            disp.display(disp.buffer)
            time.sleep(60)
    except Exception as e:
            print("Error while showing screen1; ",str(e))

    # Second screen 30s
    try:
        if "Screen2" in userScreenChoices:
            draw_screen2()
            disp.display(disp.buffer)
            time.sleep(30)
    except Exception as e:
        print("Error while showing screen2; ",str(e))

    # Third screen 30s
    try:
        if "Screen3" in userScreenChoices:
            draw_screen3()
            disp.display(disp.buffer)
            time.sleep(30)
    except Exception as e:
        print("Error while showing screen3; ",str(e))

    # Fourth screen 30s
    try: 
        if "Screen4" in userScreenChoices:
            draw_screen4()
            disp.display(disp.buffer)
            time.sleep(30)
    except Exception as e:
        print("Error while showing screen4; ",str(e))
        
    # Fifth screen 30s
    try: 
        if "Screen5" in userScreenChoices:
            draw_screen5()
            disp.display(disp.buffer)
            time.sleep(30)
    except Exception as e:
        print("Error while showing screen5; ",str(e))
        
    # Sixth screen 30s
    try: 
        if "Screen6" in userScreenChoices:
            draw_screen6()
            disp.display(disp.buffer)
            time.sleep(30)
    except Exception as e:
        print("Error while showing screen6; ",str(e))
        
    # Seventh screen 30s
    try: 
        if "Screen7" in userScreenChoices:
            draw_screen7()
            disp.display(disp.buffer)
            time.sleep(30)
    except Exception as e:
        print("Error while showing screen7; ",str(e))



