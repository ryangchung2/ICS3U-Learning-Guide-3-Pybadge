#!/usr/bin/env python3

# Created by Ryan Chung Kam Chung
# Created in January 2021
# Making the character move


# Libraries that will enable us to render and stage assets
import ugame
import stage

# Constants file
import constants


def game_scene():
    # Main game scene

    # IMAGE BANKS
    game_image_bank = stage.Bank.from_bmp16("image_bank_1.bmp")

    # BACKGROUND
    # Sets background to the 0th image in the image bank, 10x8 grid
    game_background = stage.Grid(game_image_bank, constants.SCREEN_GRID_X,
                                 constants.SCREEN_GRID_Y)

    # Sets the floor as the 1st image in the image bank, the walls are
    # still going to be the 0th image
    for x_location in range(1, constants.SCREEN_GRID_X - 1):
        for y_location in range(1, constants.SCREEN_GRID_Y - 1):
            tile_picked = 1
            game_background.tile(x_location, y_location, tile_picked)

    # SPRITES CREATION
    # Character sprite being displayed
    character = stage.Sprite(game_image_bank, 5, 75, 66)

    # STAGE AND RENDER
    # Creates a stage for the background
    # Sets frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # Sets sprite layers and show up in order
    game.layers = ([character] + [game_background])
    # Renders all sprites, only once
    game.render_block()

    # GAME LOOP
    while True:
        # USER MOVEMENT
        keys = ugame.buttons.get_pressed()

        # Button states to fire
        if keys & ugame.K_RIGHT:
            # Move right
            character.move(character.x + 1, character.y)
            character.set_frame(5, 1)
        if keys & ugame.K_LEFT:
            # Move left
            character.move(character.x - 1, character.y)
            character.set_frame(5, 3)
        if keys & ugame.K_UP:
            # Move up
            character.move(character.x, character.y - 1)
            character.set_frame(5, 0)
        if keys & ugame.K_DOWN:
            # Move down
            character.move(character.x, character.y + 1)
            character.set_frame(5, 2)

        # RENDER AND REDRAW
        # Renders and redraws the sprites that move
        game.render_sprites([character])
        # Waits until refresh rate finishes
        game.tick()


# Makes this file run as the main file of the program, and runs menu_scene()
if __name__ == "__main__":
    game_scene()
