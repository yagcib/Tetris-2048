from tile import Tile  # used for modeling each tile on the tetromino
from point import Point  # used for tile positions
import copy as cp  # the copy module is used for copying tiles and positions
import random  # module for generating random values/permutations
import numpy as np  # the fundamental Python module for scientific computing


# Class used for modeling tetrominoes with 3 out of 7 different types/shapes 
# as (I, O, Z, S, L, J and T)
class Tetromino:
   # The dimensions of the game grid
   grid_height, grid_width = None, None

   # Constructor to create a tetromino with a given type (shape)
   def __init__(self, type, grid_height, grid_width):
      # set the shape of the tetromino based on the given type
      self.grid_height = grid_height
      self.grid_width = grid_width
      self.type = type
      # determine the occupied (non-empty) tiles in the tile matrix
      occupied_tiles = []
      if type == 'I':
         n = 4  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino I in its initial orientation
         print("I")
         occupied_tiles.append((1, 0))  # (column_index, row_index)
         occupied_tiles.append((1, 1))
         occupied_tiles.append((1, 2))
         occupied_tiles.append((1, 3))
      elif type == 'O':
         n = 2  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino O in its initial orientation
         print("O")
         occupied_tiles.append((0, 0))
         occupied_tiles.append((1, 0))
         occupied_tiles.append((0, 1))
         occupied_tiles.append((1, 1))
      elif type == 'Z':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino Z in its initial orientation
         occupied_tiles.append((0, 0))
         occupied_tiles.append((1, 0))
         occupied_tiles.append((1, 1))
         occupied_tiles.append((2, 1))
         print("Z")
      elif type == 'S':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino S in its initial orientation
         occupied_tiles.append((0, 1))
         occupied_tiles.append((1, 0))
         occupied_tiles.append((1, 1))
         occupied_tiles.append((2, 0))
         print("S")
      elif type == 'L':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino L in its initial orientation
         occupied_tiles.append((1, 0))
         occupied_tiles.append((1, 1))
         occupied_tiles.append((1, 2))
         occupied_tiles.append((2, 2))
         print("L")
      elif type == 'J':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino J in its initial orientation
         occupied_tiles.append((1, 0))
         occupied_tiles.append((1, 1))
         occupied_tiles.append((1, 2))
         occupied_tiles.append((0, 2))
         print("J")
      elif type == 'T':
         n = 3  # n = number of rows = number of columns in the tile matrix
         # shape of the tetromino T in its initial orientation
         occupied_tiles.append((0, 1))
         occupied_tiles.append((1, 1))
         occupied_tiles.append((2, 1))
         occupied_tiles.append((1, 2))
         print("T")
      # create a matrix of numbered tiles based on the shape of the tetromino
      self.tile_matrix = np.full((n, n), None)

      # initialize the position of the tetromino (the bottom left cell in the
      # tile matrix) with a random horizontal position above the game grid
      self.bottom_left_cell = Point()
      self.bottom_left_cell.y = grid_height
      self.bottom_left_cell.x = random.randint(0, grid_width - n)

      # create the four tiles (minos) of the tetromino and place these tiles
      # into the tile matrix
      for i in range(len(occupied_tiles)):
         col_index, row_index = occupied_tiles[i][0], occupied_tiles[i][1]
         position = Point()
         # horizontal position of the tile
         position.x = self.bottom_left_cell.x + col_index
         # vertical position of the tile
         position.y = self.bottom_left_cell.y + (n - 1) - row_index
         # create a new tile at this position
         self.tile_matrix[row_index][col_index] = Tile(position)

   # Method for drawing the tetromino on the game grid
   def draw(self):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      for row in range(n):
         for col in range(n):
            # draw each occupied tile (not equal to None) on the game grid
            if self.tile_matrix[row][col] is not None:
               # get the position of the tile
               position = self.tile_matrix[row][col].get_position()
               # draw only the tiles that are inside the game grid
               if position.y < self.grid_height:
                  self.tile_matrix[row][col].draw()

   # Method for draw the next tetromino
   def draw_next_tetro(self):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      for row in range(n):
         for col in range(n):
            # draw next tetromino on the game grid
            if self.tile_matrix[row][col] is not None:
               next_tetro = Tile(Point(self.grid_width + col + 1, self.grid_height - row - 14))
               next_tetro.number = self.tile_matrix[row][col].number
               next_tetro.draw()

   # Method for moving the tetromino in a given direction by 1 on the game grid
   def move(self, direction, game_grid):
      # check if the tetromino can be moved in the given direction by using the
      # can_be_moved method defined below
      if not (self.can_be_moved(direction, game_grid)):
         return False  # tetromino cannot be moved in the given direction
      # move the tetromino by updating the position of the bottom left cell in
      # the tile matrix
      if direction == "left":
         self.bottom_left_cell.x -= 1
      elif direction == "right":
         self.bottom_left_cell.x += 1
      else:  # direction == "down"
         self.bottom_left_cell.y -= 1

      n = len(self.tile_matrix)  # n = number of rows = number of columns
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:

               if direction == "left":
                  self.tile_matrix[row][col].move_tetro(-1, 0)
               elif direction == "right":
                  self.tile_matrix[row][col].move_tetro(1, 0)
               else:  # direction == "down"
                  self.tile_matrix[row][col].move_tetro(0, -1)

      return True  # successful move in the given direction

   # Method for when users press up, tetromino will change rotation
   def rotate(self, game_grid):
      new_position = [0, 0, 0, 0]
      counter = 0
      counter_2 = 0
      n = len(self.tile_matrix)
      x = self.bottom_left_cell.x + n / 2 - 0.5
      y = self.bottom_left_cell.y + n / 2 - 0.5

      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] is not None:
               position = self.tile_matrix[row][col].get_position()
               dx = x - position.x
               dy = y - position.y
               dx_c = x - dy
               dy_c = y + dx
               new_position[counter_2] = Point(int(dx_c), int(dy_c))
               can_rotate = self.can_rotate(new_position[counter_2], game_grid)
               counter_2 = counter_2 + 1
               if can_rotate:
                  counter = counter + 1

      counter_2 = 0
      for row in range(n):
         for col in range(n):
            if self.tile_matrix[row][col] != None:
               # if all tiles can rotate
               if counter == 4:
                  # change positions
                  self.tile_matrix[row][col].set_position(new_position[counter_2])
                  counter_2 = counter_2 + 1
      # change tile matrix if all tiles can rotate
      if counter == 4:
         self.tile_matrix = np.rot90(self.tile_matrix, 3)

   def can_rotate(self, pos, game_grid):
      if pos.x < 0:
         return False
      if pos.x >= self.grid_width:
         return False
      if game_grid.is_occupied(pos.y, pos.x):
         return False
      else:
         return True

   # Method to check if the tetromino can be moved in the given direction or not
   def can_be_moved(self, dir, game_grid):
      n = len(self.tile_matrix)  # n = number of rows = number of columns
      # check for moving left or right
      if dir == "left" or dir == "right":
         for row in range(n):
            for col in range(n):
               # direction = left --> check the leftmost tile of each row
               if dir == "left" and self.tile_matrix[row][col] is not None:
                  leftmost = self.tile_matrix[row][col].get_position()
                  # tetromino cannot go left if any leftmost tile is at x = 0
                  if leftmost.x == 0:
                     return False
                  # skip each row whose leftmost tile is out of the game grid
                  # (possible for newly entered tetrominos to the game grid)
                  if leftmost.y >= self.grid_height:
                     break
                  # tetromino cannot go left if the grid cell on the left of any
                  # of its leftmost tiles is occupied
                  if game_grid.is_occupied(leftmost.y, leftmost.x - 1):
                     return False
                  break  # end the inner for loop
               # direction = right --> check the rightmost tile of each row
               elif dir == "right" and self.tile_matrix[row][n - 1 - col] != None:
                  rightmost = self.tile_matrix[row][n - 1 - col].get_position()
                  # tetromino cannot go right if any of its rightmost tiles is
                  # at x = grid_width - 1
                  if rightmost.x == self.grid_width - 1:
                     return False
                  # skip each row whose rightmost tile is out of the game grid
                  # (possible for newly entered tetrominos to the game grid)
                  if rightmost.y >= self.grid_height:
                     break
                  # tetromino cannot go right if the grid cell on the right of
                  # any of its rightmost tiles is occupied
                  if game_grid.is_occupied(rightmost.y, rightmost.x + 1):
                     return False
                  break  # end the inner for loop
      # direction = down --> check the bottommost tile of each column
      else:
         for col in range(n):
            for row in range(n - 1, 0, -1):
               if self.tile_matrix[row][col] != None:
                  bottommost = self.tile_matrix[row][col].get_position()
                  # skip each column whose bottommost tile is out of the grid
                  # (possible for newly entered tetrominos to the game grid)
                  if bottommost.y > self.grid_height:
                     break
                  # tetromino cannot go down if any bottommost tile is at y = 0
                  if bottommost.y == 0:
                     return False
                     # or the grid cell below any bottommost tile is occupied
                  if game_grid.is_occupied(bottommost.y - 1, bottommost.x):
                     return False
                  break  # end the inner for loop
      return True  # tetromino can be moved in the given direction