import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import time
import datetime
import random


displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
g = displayio.Group()
display.root_group = g

def get_text_color():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        return 0xFFA500  
    elif hour < 18:
        return 0x00FF00
    else:
        return 0xFF1493

def get_time_rn():
    hr = datetime.datetime.now().hour
    min = str(datetime.datetime.now().minute)    
    if int(min) < 10:
        min = '0' + min
    return str(hr) + ':' + min

def fill_display():
    curr_time = get_time_rn()
    hour, minute = curr_time.split(":")
    hour = int(hour)
    bitmap = displayio.Bitmap(64, 32, 6)
    cloud_positions = [(random.randint(0, 64), random.randint(0, 8)) for _ in range(6)]
   
    if hour < 18 and hour >=6:
        for y in range(32):
            for x in range(64):
                bitmap[x, y] = 2
# CLOUDS
        for (x, y) in cloud_positions: 
            for dx in range(-2, 3):
                for dy in range(-1, 2):
                    if (0 <= x+dx < 64 and 0 <= y+dy < 32 and 
                    not (54 <= x+dx <= 63 and 0 <= y+dy <= 9)):
                        bitmap[x+dx, y+dy] = 5  # Light Gray for clouds

    else:
        for y in range(32):
            for x in range(64):
                bitmap[x, y] = 3
# STARS
                if random.randint(0, 30) == 1:  # 1 in 30 chance of a star
                    bitmap[x, y] = 4
               
    bg_palette = displayio.Palette(6)
    bg_palette[0] = 0x000000
    bg_palette[1] = 0x3b3b3b
    bg_palette[2] = 0x00afda
    bg_palette[3] = 0x1B003B
    bg_palette[4] = 0xADD8E6
    bg_palette[5] = 0xF0F8FF

    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bg_palette)

    g.append(tile_grid)

def get_icon():
    hour = datetime.datetime.now().hour
    shape_bitmap = displayio.Bitmap(9, 9, 3)  # 9x9 grid, 3 colors (0 = background, 1 = shape)
    
    # Define the yellow parts (value = 1)
    sun_pixels = [
        (4, 0), (4, 8), (0, 4), (8, 4),  # Cross center
        (2, 2), (2, 6), (6, 2), (6, 6),  # Outer corners
        (4, 2), (4, 6), (2, 4), (6, 4),  # Mid arms
        (3, 3), (3, 5), (5, 3), (5, 5),  # Inner corners
        (3, 4), (4, 3), (4, 4), (4, 5), (5, 4)  # Filling the middle
    ]

    moon_pixels = [
    (3, 1), (4, 1), (5, 1),
    (2, 2), (3, 2), (4, 2), (5, 2), (6, 2),
    (2, 3), (3, 3), (4, 3), (5, 3), (6, 3),
    (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4),
    (2, 5), (3, 5), (4, 5), (5, 5), (6, 5),
    (2, 6), (3, 6), (4, 6), (5, 6), (6, 6),
    (3, 7), (4, 7), (5, 7)
]

    shape_p = displayio.Palette(4)

    shape_p[0] = 0x00afda #day sky
    shape_p[1] = 0xffb400 #sun
    shape_p[2] = 0xC0C0C0 #moon
    shape_p[3] = 0x1B003B #night sky
 #SUN -------------------------------------------------------------------------------------------------------------------------------------------------   
    if 6 <= hour < 18:
        for x in range(9):
            for y in range(9):
                if (x, y) in sun_pixels:
                    shape_bitmap[x, y] = 1
                else:
                    shape_bitmap[x, y] = 0
    
# MOON -------------------------------------------------------------------------------------------------------------------------------------------------
    else:
        for x in range(9):
            for y in range(9):
                if (x, y) in moon_pixels:
                    shape_bitmap[x,y] = 2
                else:
                    shape_bitmap[x,y] = 3

                
    g.append(displayio.TileGrid(bitmap=shape_bitmap, pixel_shader=shape_p,
            width=1,height=1,
            tile_width=9,tile_height=9,
            default_tile=0,
            x= display.width - 10,
            y=1))
   

def clock():
   
    current_time = get_time_rn()
   
    line1 = adafruit_display_text.label.Label(
        font=terminalio.FONT,
        color= get_text_color(),
        label_direction="LTR",
        scale=2,
        anchor_point=(0.5,0.5),
        anchored_position=(32,22),
        text=current_time,
    )
   
    g.append(line1)




while True:
    fill_display()
    clock()
    get_icon()
    display.refresh(minimum_frames_per_second=0)
    if 6<= datetime.datetime.now().hour < 18 :
        time.sleep(5)
    else:
        time.sleep(1)
