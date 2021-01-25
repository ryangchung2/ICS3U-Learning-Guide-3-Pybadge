#!/usr/bin/env python3

# Created by Ryan Chung Kam Chung
# Created in January 2021
# Constraining the movement of the character


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
    character = stage.Sprite(game_image_bank, 2, 75, 66)

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

        if keys & ugame.K_RIGHT:
            # Move right with constraints of the right border
            if character.x <= constants.SCREEN_X - 2 * constants.SPRITE_SIZE:
                character.move(character.x + constants.SPRITE_MOVEMENT_SPEED,
                               character.y)
            else:
                character.move(constants.SCREEN_X - 2 * constants.SPRITE_SIZE,
                               character.y)
            character.set_frame(2, 0)
        if keys & ugame.K_LEFT:
            # Move left with constraints of the left border
            if character.x >= constants.SCREEN_X - 9 * constants.SPRITE_SIZE:
                character.move(character.x - constants.SPRITE_MOVEMENT_SPEED,
                               character.y)
            else:
                character.move(constants.SPRITE_SIZE, character.y)
            character.set_frame(2, 4)
        if keys & ugame.K_UP:
            # Moves down with constraints of the ceiling
            if character.y >= constants.SPRITE_SIZE:
                character.move(character.x,
                               character.y - constants.SPRITE_MOVEMENT_SPEED)
            else:
                character.move(character.x, constants.SPRITE_SIZE)
            character.set_frame(3, 0)
        if keys & ugame.K_DOWN:
            # Moves down with constraints of the ground
            if character.y <= constants.SCREEN_Y - 2 * constants.SPRITE_SIZE:
                character.move(character.x,
                               character.y + constants.SPRITE_MOVEMENT_SPEED)
            else:
                character.move(character.x,
                               constants.SCREEN_Y - 2 * constants.SPRITE_SIZE)
            character.set_frame(4, 0)

        # RENDER AND REDRAW
        # Renders and redraws the sprites that move
        game.render_sprites([character])
        # Waits until refresh rate finishes
        game.tick()


# Makes this file run as the main file of the program, and runs menu_scene()
if __name__ == "__main__":
    game_scene()
