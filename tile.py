import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the tile and the number on it
from point import Point
import copy as cp
from random import randint

# Class used for modeling numbered tiles as in 2048
class Tile: 
   # Class attributes shared among all Tile objects
   # ---------------------------------------------------------------------------
   # value used for the thickness of the boxes (boundaries) around the tiles
   boundary_thickness = 0.004
   # font family and size used for displaying the tile number
   font_family, font_size = "Helvetica Neue", 30

   # Constructor that creates a tile at a given position with 2 as its number
   def __init__(self, position = Point(0, 0)): # (0, 0) is the default position
      # set the number on the tile
      self.number = 2**randint(1,2)
      # set the colors of the tile
      self.foreground_color = Color(167, 153, 140)  # foreground (number) color
      self.boundary_color = Color(167, 153, 140)
      # set the poisiton of the tile
      self.position = Point(position.x, position.y)

   # set the rotation of tile
   def set_position(self, position):
      self.position = cp.copy(position)

   # get the position of the tile
   def get_position(self):
      return cp.copy(self.position)

   # use for the tile number (2, 4, 8, 16,...)
   def double(self):
      self.number *= 2

   # move the tetrominos to left, right and down
   def move_tetro(self, x, y):
      self.position.translate(x, y)

   # Method for drawing the tile
   def draw(self):
      # set the tile background and foreground color
      if (self.number == 2):
         self.background_color = Color(238, 228, 218)

      if (self.number == 4):
         self.background_color = Color(238, 225, 201)

      if (self.number == 8):
         self.background_color = Color(243, 178, 122)
         self.foreground_color = Color(248, 240, 232)

      if (self.number == 16):
         self.background_color = Color(246, 150, 100)
         self.foreground_color = Color(248, 240, 232)

      if (self.number == 32):
         self.background_color = Color(247, 124, 95)
         self.foreground_color = Color(248, 240, 232)

      if (self.number == 64):
         self.background_color = Color(246, 94, 59)
         self.foreground_color = Color(248, 240, 232)

      if (self.number == 128):
         self.background_color = Color(237, 207, 114)
         self.foreground_color = Color(248, 240, 232)

      if (self.number == 256):
         self.background_color = Color(237, 204, 97)
         self.foreground_color = Color(248, 240, 232)

      if (self.number == 512):
         self.background_color = Color(237, 200, 80)
         self.foreground_color = Color(248, 240, 232)

      if (self.number == 1024):
         self.background_color = Color(237, 197, 63)
         self.foreground_color = Color(248, 240, 232)

      if (self.number == 2048):
         self.background_color = Color(237, 194, 46)
         self.foreground_color = Color(248, 240, 232)

      # For the color of the tiles with numbers greater than 2048,
      # we created an if condition by looking at the darkening ratio
      # of the numbers above.
      if (self.number > 2048):
         self.background_color= Color((237),(194 - self.number/1365),(46 - self.number/800))
         self.foreground_color = Color(248, 240, 232)

      # create a tile with background color
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(self.position.x, self.position.y, 0.51)

      # create a frame of tile boxes
      stddraw.setPenColor(self.boundary_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(self.position.x, self.position.y, 0.51)
      stddraw.setPenRadius()

      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.text(self.position.x, self.position.y, str(self.number))