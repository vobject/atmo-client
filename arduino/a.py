import os
import sys
import curses
import serial
import traceback

# global variables
class gb:
  scrn = None # Curses window object
  ser = None # serial connection object
  channels = 0
  sum_R    = 0
  sum_G    = 0
  sum_B    = 0
  left_R   = 0
  left_G   = 0
  left_B   = 0
  right_R  = 0
  right_G  = 0
  right_B  = 0
  top_R    = 0
  top_G    = 0
  top_B    = 0
  bottom_R = 0
  bottom_G = 0
  bottom_B = 0

def print_vline(y, x, text, n, attr):
  for i in range(n):
    gb.scrn.addch(y + i, x, text, attr | curses.A_BOLD)
    gb.scrn.addch(y + i, x + 1, text, attr | curses.A_BOLD)
    gb.scrn.addch(y + i, x + 2, text, attr | curses.A_BOLD)
    gb.scrn.addch(y + i, x + 3, text, attr | curses.A_BOLD)
    gb.scrn.addch(y + i, x + 4, text, attr | curses.A_BOLD)

def get_channel_data():
  # read from serial and populate gb.*_channel
  data = gb.ser.read(19)
  data_ord = [ord(x) for x in data]
  # populate the channel variables
  gb.channels = int(data_ord[ 3])
  gb.sum_R    = int(data_ord[ 4])
  gb.sum_G    = int(data_ord[ 5])
  gb.sum_B    = int(data_ord[ 6])
  gb.left_R   = int(data_ord[ 7])
  gb.left_G   = int(data_ord[ 8])
  gb.left_B   = int(data_ord[ 9])
  gb.right_R  = int(data_ord[10])
  gb.right_G  = int(data_ord[11])
  gb.right_B  = int(data_ord[12])
  gb.top_R    = int(data_ord[13])
  gb.top_G    = int(data_ord[14])
  gb.top_B    = int(data_ord[15])
  gb.bottom_R = int(data_ord[16])
  gb.bottom_G = int(data_ord[17])
  gb.bottom_B = int(data_ord[18])

def print_channel_data():
  # print gb.*_channel
  col_stepwith = curses.COLS / 5
  line_start = curses.LINES - 3
  sum_R_start = line_start - (gb.sum_R / 5)
  sum_G_start = line_start - (gb.sum_G / 5)
  sum_B_start = line_start - (gb.sum_B / 5)
  left_R_start = line_start - (gb.left_R / 5)
  left_G_start = line_start - (gb.left_G / 5)
  left_B_start = line_start - (gb.left_B / 5)
  right_R_start = line_start - (gb.right_R / 5)
  right_G_start = line_start - (gb.right_G / 5)
  right_B_start = line_start - (gb.right_B / 5)
  top_R_start = line_start - (gb.top_R / 5)
  top_G_start = line_start - (gb.top_G / 5)
  top_B_start = line_start - (gb.top_B / 5)
  bottom_R_start = line_start - (gb.bottom_R / 5)
  bottom_G_start = line_start - (gb.bottom_G / 5)
  bottom_B_start = line_start - (gb.bottom_B / 5)
  print_vline(sum_R_start, col_stepwith * 0 +  1, "*", gb.sum_R / 5, curses.color_pair(1))
  print_vline(sum_G_start, col_stepwith * 0 +  6, "*", gb.sum_G / 5, curses.color_pair(2))
  print_vline(sum_B_start, col_stepwith * 0 + 11, "*", gb.sum_B / 5, curses.color_pair(3))
  print_vline(left_R_start, col_stepwith * 1 +  1, "*", gb.left_R / 5, curses.color_pair(1))
  print_vline(left_G_start, col_stepwith * 1 +  6, "*", gb.left_G / 5, curses.color_pair(2))
  print_vline(left_B_start, col_stepwith * 1 + 11, "*", gb.left_B / 5, curses.color_pair(3))
  print_vline(right_R_start, col_stepwith * 2 +  1, "*", gb.right_R / 5, curses.color_pair(1))
  print_vline(right_G_start, col_stepwith * 2 +  6, "*", gb.right_G / 5, curses.color_pair(2))
  print_vline(right_B_start, col_stepwith * 2 + 11, "*", gb.right_B / 5, curses.color_pair(3))
  print_vline(top_R_start, col_stepwith * 3 +  1, "*", gb.top_R / 5, curses.color_pair(1))
  print_vline(top_G_start, col_stepwith * 3 +  6, "*", gb.top_G / 5, curses.color_pair(2))
  print_vline(top_B_start, col_stepwith * 3 + 11, "*", gb.top_B / 5, curses.color_pair(3))
  print_vline(bottom_R_start, col_stepwith * 4 +  1, "*", gb.bottom_R / 5, curses.color_pair(1))
  print_vline(bottom_G_start, col_stepwith * 4 +  6, "*", gb.bottom_G / 5, curses.color_pair(2))
  print_vline(bottom_B_start, col_stepwith * 4 + 11, "*", gb.bottom_B / 5, curses.color_pair(3))

def print_legend():
  # show legend at the bottom line
  col_stepwith = curses.COLS / 5
  sum_str    = "SUM: (%.3d, %.3d, %.3d)" % (gb.sum_R, gb.sum_G, gb.sum_B)
  left_str   = "LEFT: (%.3d, %.3d, %.3d)" % (gb.left_R, gb.left_G, gb.left_B)
  right_str  = "RIGHT: (%.3d, %.3d, %.3d)" % (gb.right_R, gb.right_G, gb.right_B)
  top_str    = "TOP: (%.3d, %.3d, %.3d)" % (gb.top_R, gb.top_G, gb.top_B)
  bottom_str = "BOTTOM: (%.3d, %.3d, %.3d)" % (gb.bottom_R, gb.bottom_G, gb.bottom_B)
  gb.scrn.addstr(curses.LINES - 1, col_stepwith * 0, sum_str, curses.A_BOLD)
  gb.scrn.addstr(curses.LINES - 1, col_stepwith * 1, left_str, curses.A_BOLD)
  gb.scrn.addstr(curses.LINES - 1, col_stepwith * 2, right_str, curses.A_BOLD)
  gb.scrn.addstr(curses.LINES - 1, col_stepwith * 3, top_str, curses.A_BOLD)
  gb.scrn.addstr(curses.LINES - 1, col_stepwith * 4, bottom_str, curses.A_BOLD)

def refresh():
  get_channel_data()
  gb.scrn.clear()
  print_channel_data()
  print_legend()
  gb.scrn.refresh()

def main(stdscr):
  gb.scrn = stdscr
  wnd_setup()
  # print the legend
  print_channel_data()
  # make sure serial connection is established
  serial_setup()
  # main loop - processes serial input and user input
  while True:
    try:
      refresh()
    except KeyboardInterrupt:
      gb.ser.close()
      break
  restorescreen()

def wnd_setup():
  curses.start_color()
  curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
  curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
  curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
  curses.curs_set(0)
  print_legend()
  gb.scrn.refresh()

def serial_setup():
  gb.ser = serial.Serial(port=sys.argv[1],
                         baudrate=38400,
                         parity=serial.PARITY_NONE,
                         bytesize=serial.EIGHTBITS,
                         stopbits=serial.STOPBITS_ONE)
  return gb.ser.isOpen()


if __name__ == "__main__":
  try:
    curses.wrapper(main)
  except:
    # print error message re exception
    traceback.print_exc()


  
