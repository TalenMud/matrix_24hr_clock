import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import time
import datetime


displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

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
    bitmap = displayio.Bitmap(64, 32, 4)
    
    if hour < 18 and hour >=6:
        for y in range(32):
            for x in range(64):
                bitmap[x, y] = 2
    else:
        for y in range(32):
            for x in range(64):
                bitmap[x, y] = 3
    return bitmap

def clock():
    current_time = get_time_rn()
    
    line1 = adafruit_display_text.label.Label(
        font=terminalio.FONT,
        color= 0xFFFFFF,
        label_direction="LTR",
        scale=2,
        anchor_point=(0.5,0.5),
        anchored_position=(32,16),
        text=current_time,
    )
    
    palette = displayio.Palette(4)
    palette[0] = 0x000000
    palette[1] = 0x3b3b3b
    palette[2] = 0x00afda
    palette[3] = 0x010543

    tile_grid = displayio.TileGrid(fill_display(), pixel_shader=palette)
  
    g = displayio.Group()
    g.append(tile_grid)
    g.append(line1)
    display.root_group = g


while True:
    clock()

    display.refresh(minimum_frames_per_second=0)
    time.sleep(15)