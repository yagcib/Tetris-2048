'''
Authors: Ali Büyükberber, Ataman Fedai, Bayram Yağcı
Date: 12.04.2022
Tetris 2048 Game
'''

import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.picture import Picture  # used for displaying images
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid # the class for modeling the game grid
from tetromino import Tetromino # the class for modeling the tetrominoes
import random # used for creating tetrominoes with random types/shapes

# MAIN FUNCTION OF THE PROGRAM
#-------------------------------------------------------------------------------
# Main function where this program starts execution
def start():

   # set the dimensions of the game grid in the canvas()
   global grid
   # create the game grid
   grid = GameGrid(grid_h, grid_w)
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   current_tetromino = create_tetromino(grid_h, grid_w)
   next_tetromino = create_tetromino(grid_h, grid_w)
   grid.current_tetromino = current_tetromino
   grid.next_tetromino = next_tetromino
   # it's for game over menu to start menu
   stddraw.clearKeysTyped()
   pause = False

   # main game loop (keyboard interaction for moving the tetromino)
   while True:

      # if mouse pressed at these locations, game print the how to play menu
      if stddraw.mousePressed():
         # check if these coordinates are inside the button
         if stddraw.mouseX() >= grid_w+1 and stddraw.mouseX() <= grid_w+3:
            if stddraw.mouseY() >= grid_h-2 and stddraw.mouseY()<= grid_h:
               menu(grid_h,grid_w)
               print("Stop for how to play menu.")

      # check user interactions via the keyboard
      if stddraw.hasNextKeyTyped():
         key_typed = stddraw.nextKeyTyped()

         # if user press the p key, game will stop
         if key_typed=='p':
            print("Pause")
            if pause:
               pause = False
            else:
               pause = True

         # if users didn't press the p, game will want the press rotation key from users
         elif not pause:

            # if the left arrow key has been pressed
            if key_typed == "left":
               # move the active tetromino left by one
               current_tetromino.move(key_typed, grid)
            # if the right arrow key has been pressed
            elif key_typed == "right":
               # move the tetromino right by one
               current_tetromino.move(key_typed, grid)
            # if the down arrow key has been pressed
            elif key_typed == "down":
               # move the active tetromino down by one
               # (soft drop: causes the tetromino to fall down faster)
               current_tetromino.move(key_typed*2, grid)
            # if users want the piece drop, they have to press space button
            elif key_typed =='space':
               for i in range(grid_h):
                  current_tetromino.move('down',grid)
            # it's for game speed faster
            elif key_typed=='f':
               if grid.speed > 60:
                  grid.speed -=75
            # it's for game speed slower
            elif key_typed=='s':
               if grid.speed < 500:
                  grid.speed +=75
            # if users want to rotate the tetromino, they have to press up button
            elif key_typed == 'up':
               current_tetromino.rotate(grid)

         # R for restart the game
         if key_typed=='r':
            print("Game restarted.")
            start()

         # clear the queue that stores all the keys pressed/typed
         stddraw.clearKeysTyped()

      # move the active tetromino down by one at each iteration (auto fall)
      if not pause:
         success = current_tetromino.move("down", grid)

      # place the tetromino on the game grid when it cannot go down anymore
      if not success and not pause:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles_to_place = current_tetromino.tile_matrix
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles_to_place)
         # end the main game loop if the game is over
         if game_over:
            if display_game_over(grid_h,grid_w+5):
               pause = True
               start()

         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         current_tetromino = next_tetromino
         grid.current_tetromino = current_tetromino
         # print the next tetromino at the terminal
         print("Next Tetromino:")
         next_tetromino = create_tetromino(grid_h, grid_w)
         grid.next_tetromino = next_tetromino
         next_tetromino.draw_next_tetro()

      # display the game grid and as well the current tetromino
      grid.display(pause)

   # print a message on the console when the game is over
   print("Game over")

# Method for the how to play menu on the right side of grid
def menu(grid_height, grid_width):
   stddraw.setPenColor(Color(147, 123, 110))
   stddraw.filledRectangle(grid_width-0.35 , grid_width - 5, 4.75,6)
   stddraw.setPenColor(Color(243, 178, 122))
   stddraw.filledRectangle(grid_width + 3.40, grid_width , 1, 1)
   stddraw.setPenRadius(0.002)
   stddraw.setPenColor(Color(100,100,100))
   stddraw.rectangle(grid_width + 3.40, grid_width, 1, 1)
   stddraw.setFontSize(45)
   stddraw.setPenColor(stddraw.WHITE)
   stddraw.text(grid_width + 3.9, grid_width+0.45, "X")
   stddraw.setFontSize(24)
   stddraw.setPenColor(stddraw.WHITE)
   stddraw.text(grid_width + 2, grid_height - 6.5, "Press P for Pause")
   stddraw.text(grid_width + 2, grid_height - 7.5, "Press R for Restart")
   stddraw.text(grid_width + 2, grid_height - 8.5, "Press Space for Drop")
   stddraw.text(grid_width + 2, grid_height - 9.5, "Press F for Speed Up")
   stddraw.text(grid_width + 2, grid_height - 10.5, "Press S for Speed Down")

   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the button
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has
         # most recently been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= grid_width+3.4  and mouse_x <= grid_width+4.5:
            if mouse_y >= grid_height-6 and mouse_y <= grid_height-5:
               break # break the loop to return game

# Function for creating random shaped tetrominoes to enter the game grid
def create_tetromino(grid_height, grid_width):
   # type (shape) of the tetromino is determined randomly
   tetromino_types = [ "S", "T","J",'L','O','Z','I']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type, grid_height, grid_width)
   return tetromino

# Function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   # colors used for the menu
   background_color = Color(0, 0, 0)
   button_color = Color(194, 24, 27)
   text_color = Color(255, 255, 255)
   # clear the background canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   directory = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = directory + "/images/space.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 9
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # get the directory in which this python code file is placed
   directoryy = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = directoryy + "/images/HowToPlay.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 20
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = grid_width - 1.5, 2
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Helvetica Neue")
   stddraw.setFontSize(35)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)
   # menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has
         # most recently been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break # break the loop to end the method and start the game

# Method for the display a game over menu with grid height and grid width
def display_game_over(grid_height, grid_width):
   # colors used for the game over screen
   button_color = Color(194, 24, 27)
   text_color = Color(255, 255, 255)
   # get the directory in which this python code file is placed
   directory = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = directory + "/images/space.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 9
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # center coordinates to display the image
   img_center_x, img_center_y = (grid_width - 1) / 2, grid_height - 7
   # image is represented using the Picture class
   image_to_display = Picture(img_file)
   # display the image
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # dimensions of the start game button
   button_w, button_h = grid_width - 1.5, 2
   # coordinates of the bottom left corner of the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # display the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # display the text on the start game button
   stddraw.setFontFamily("Helvetica Neue")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Game Over"
   stddraw.text(img_center_x, 5.6, text_to_display)
   stddraw.text(img_center_x, 5.1, "Score : " + str(grid.score))
   stddraw.text(img_center_x, 4.4, "Click Here to Main Menu")
   # game over menu interaction loop
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked
      if stddraw.mousePressed():
         # get the x and y coordinates of the location at which the mouse has
         # most recently been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               display_game_menu(grid_height,grid_width)
               start() # break the loop to end the method and start the game

# Method for create a canvas for game
def canvas():
   # set the dimensions of the game grid
   global grid_h, grid_w
   grid_h, grid_w = 18, 12
   # set the size of the drawing canvas
   canvas_h, canvas_w = 40 * grid_h, 60 * grid_w
   stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system
   stddraw.setXscale(-0.5, grid_w + 4.5)
   stddraw.setYscale(-0.5, grid_h - 0.5)
   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(grid_h, grid_w + 5)

# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__== '__main__':
   canvas()
   start()