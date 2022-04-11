import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing

# Class used for modelling the game grid
class GameGrid:
   # Constructor for creating the game grid based on the given arguments
   def __init__(self, grid_h, grid_w):
      # set the dimensions of the game grid as the given arguments
      self.grid_height = grid_h
      self.grid_width = grid_w
      # create a tile matrix to store the tiles landed onto the game grid
      self.tile_matrix = np.full((grid_h, grid_w), None)
      # create the tetromino that is currently being moved on the game gri
      self.current_tetromino = None
      self.next_tetromino = None
      # the game_over flag shows whether the game is over or not
      self.game_over = False
      self.speed = 300
      # set the color used for the empty grid cells
      self.empty_cell_color = Color(205, 193, 180)
      # set the colors used for the grid lines and the grid boundaries
      self.line_color = Color(187, 173, 160)
      self.boundary_color = Color(147, 133, 120)
      # thickness values used for the grid lines and the grid boundaries
      self.line_thickness = 0.006
      self.box_thickness = 1.5 * self.line_thickness
      # sum score
      self.score = 0

   # Method used for displaying the game grid
   def display(self, pause):
      # clear the background canvas to empty_cell_color
      stddraw.clear(self.empty_cell_color)

      # draw the Your Score to the right side
      stddraw.setFontSize(38)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.text(self.grid_width + 2, self.grid_height - 2.5, "Your Score")

      # draw the score to the right side
      stddraw.setFontSize(50)
      stddraw.text(self.grid_width + 2, self.grid_height - 3.5, str(self.score))

      # draw to the How to Play? to the right side
      stddraw.setPenColor(Color(255, 255, 255))
      stddraw.rectangle(self.grid_width + 1, self.grid_height - 1.75, 2, 1)
      stddraw.setFontSize(18)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.text(self.grid_width + 2, self.grid_height - 1.25, "How to Play?")

      # draw to the Next Tetromino to the right side
      stddraw.setFontSize(24)
      stddraw.setPenColor(stddraw.WHITE)
      stddraw.text(self.grid_width + 2, self.grid_height - 13, "Next Tetromino")

      # draw the game grid
      self.next_tetromino.draw_next_tetro()
      self.draw_grid()

      # draw the current/active tetromino if it is not None (the case when the
      # game grid is updated)
      if self.current_tetromino is not None:
         self.current_tetromino.draw()
      # draw a box around the game grid
      self.draw_boundaries()

      # draw the pause screen
      if (pause):
         stddraw.setPenColor(stddraw.DARK_GRAY)
         stddraw.setFontSize(35)
         stddraw.setFontFamily("Helvetica Neue")
         stddraw.text(self.grid_width / 2, self.grid_height / 2, "Game is Paused")
         stddraw.text(self.grid_width / 2, self.grid_height / 2-1, "Press P for Resume")

      # show the resulting drawing with a pause duration
      stddraw.show(self.speed)

   # Method for drawing the cells and the lines of the grid
   def draw_grid(self):
      self.delete_tile()
      # for each cell of the game grid
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            # draw the tile if the grid cell is occupied by a tile
            if self.tile_matrix[row][col] is not None:
               self.tile_matrix[row][col].draw()
      # draw the inner lines of the grid
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      # x and y ranges for the game grid
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
         stddraw.line(start_x, y, end_x, y)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # Method for drawing the boundaries around the game grid
   def draw_boundaries(self):
      # draw a bounding box around the game grid as a rectangle
      stddraw.setPenColor(self.boundary_color)  # using boundary_color
      # set the pen radius as box_thickness (half of this thickness is visible
      # for the bounding box as its lines lie on the boundaries of the canvas)
      stddraw.setPenRadius(self.box_thickness)
      # the coordinates of the bottom left corner of the game grid
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()  # reset the pen radius to its default value

   # Method used for checking whether the grid cell with given row and column
   # indexes is occupied by a tile or empty
   def is_occupied(self, row, col):
      # considering newly entered tetrominoes to the game grid that may have
      # tiles with position.y >= grid_height
      if not self.is_inside(row, col):
         return False
      # the cell is occupied by a tile if it is not None
      return self.tile_matrix[row][col] != None

   # Method used for checking whether the cell with given row and column indexes
   # is inside the game grid or not
   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   # Method that locks the tiles of the landed tetromino on the game grid while
   # checking if the game is over due to having tiles above the topmost grid row.
   # The method returns True when the game is over and False otherwise.
   def update_grid(self, tiles_to_place):
      # necessary for the display method to stop displaying the tetromino
      self.current_tetromino = None
      # lock the tiles of the current tetromino (tiles_to_lock) on the game grid
      n_rows, n_cols = len(tiles_to_place), len(tiles_to_place[0])
      for col in range(n_cols):
         for row in range(n_rows):
            # place each occupied tile onto the game grid
            if tiles_to_place[row][col] is not None:
               # compute the position of the tile on the game grid
               pos = tiles_to_place[row][col].get_position()
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_place[row][col]
               # the game is over if any placed tile is out of the game grid
               else:
                  self.game_over = True
      # call the check_grid and merge method
      self.check_grid()
      self.merge()
      # return the game_over flag
      return self.game_over

   def check_grid(self):
      for row in range(self.grid_width):
         if None not in self.tile_matrix[row]:
            self.delete_row(row)
            self.move_row(row)
            self.check_grid()

   # Method for delete the row when row are full
   def delete_row(self, row):
      for i in range(self.grid_width):
         new_score = self.tile_matrix[row][i].number
         self.score += new_score

      self.tile_matrix = np.delete(self.tile_matrix, row, axis=0)
      self.tile_matrix = np.append(self.tile_matrix, np.reshape(np.full(self.grid_width, [None]), (-1, self.grid_width)), axis=0)

   # Method for when one row deleted, tiles will move to the down row
   def move_row(self, row):
      for row_i in range(row, self.grid_height):
         for col_i in range(self.grid_width):
            if self.tile_matrix[row_i][col_i] is not None:
               self.tile_matrix[row_i][col_i].move_tetro(0, -1)

   # Method for when one row deleted, tiles on column will move to the down row
   def move_column(self, col, row):
      for row_i in range(row, self.grid_height):
         if self.tile_matrix[row_i][col] is not None:
            self.tile_matrix[row_i][col].move_tetro(0, -1)
      # transpose the tile to the down
      transposed = self.tile_matrix.transpose()
      deleted = np.delete(transposed[col], row)
      transposed[col] = np.append(deleted, [None], axis=0)
      self.tile_matrix = transposed.transpose()

   # Method for if there are no tiles around all 4 of the tile,
   # it deletes the tile and adds the tile's score to the total score.
   def delete_tile(self):
      for row_i in range(1, self.grid_height - 1):
         for col_i in range(1, self.grid_width - 1):
            if self.tile_matrix[row_i][col_i] is not None:
               if self.tile_matrix[row_i + 1][col_i] is None and \
                       self.tile_matrix[row_i - 1][col_i] is None and \
                       self.tile_matrix[row_i][col_i + 1] is None and \
                       self.tile_matrix[row_i][col_i - 1] is None:
                  new_score = self.tile_matrix[row_i][col_i].number
                  self.score += new_score
                  self.tile_matrix[row_i][col_i] = None
                  self.delete_tile()

   # Method for If the numbers in the overlapping tiles
   # are the same, add the numbers and delete the upper
   # tile and write the total number in the lower tile.
   def merge(self):
      for row_i in range(self.grid_height - 1):
         for col_i in range(self.grid_width):
            if self.tile_matrix[row_i][col_i] is not None and self.tile_matrix[row_i + 1][col_i] is not None:
               if self.tile_matrix[row_i][col_i].number == self.tile_matrix[row_i + 1][col_i].number:
                  self.score += self.tile_matrix[row_i][col_i].number * 2
                  self.tile_matrix[row_i][col_i].double()
                  self.tile_matrix[row_i + 1][col_i] = None
                  self.move_column(col_i, row_i + 1)
                  self.merge()