#!/usr/bin/env python3

# Created by Ryan Chung Kam Chung
# Created in January 2021
# Adding progressive difficulty


# Libraries that will enable us to render and stage assets
import ugame
import stage
import random
import supervisor
import time

# Constants file
import constants


def menu_scene():
    # Menu scene

    # IMAGE BANK
    menu_image_bank = stage.Bank.from_bmp16("image_bank_1.bmp")

    # BACKGROUND
    # Sets background to the 0th image in the image bank, 10x8 grid
    menu_background = stage.Grid(menu_image_bank, constants.SCREEN_GRID_X,
                                 constants.SCREEN_GRID_Y)

    # Sets the floor as the 1st image in the image bank, the walls are
    # still going to be the 0th image
    for x_location in range(1, constants.SCREEN_GRID_X - 1):
        for y_location in range(1, constants.SCREEN_GRID_Y - 1):
            tile_picked = 1
            menu_background.tile(x_location, y_location, tile_picked)

    # TEXT
    text = []
    text1 = stage.Text(width=29, height=12, font=None,
                       palette=constants.PALETTE, buffer=None)
    text1.move(32, 10)
    text1.text("Ghost Dodge!")
    text.append(text1)

    text2 = stage.Text(width=29, height=12, font=None,
                       palette=constants.PALETTE, buffer=None)
    text2.move(35, 110)
    text2.text("PRESS START")
    text.append(text2)

    # STAGE AND RENDER
    # creates stage and sets it to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # sets the layers of all sprites, in order
    game.layers = text + [menu_background]
    # renders all sprites, only once
    game.render_block()

    while True:
        # get user input
        keys = ugame.buttons.get_pressed()

        # select start button
        if keys & ugame.K_START != 0:
            game_scene()

        # update game logic
        game.tick()


def game_scene():
    # Main game scene

    # SCORE
    score = 0

    score_text = stage.Text(width=29, height=14)
    score_text.clear()
    score_text.cursor(0, 0)
    score_text.move(0, 1)
    score_text.text("Score: {0}".format(score))

    # FUNCTION DEFINITION
    def show_ghost():
        numbers_x = list(range(character.x - 3 * constants.SPRITE_SIZE,
                               character.x,
                               character.x + 3 * constants.SPRITE_SIZE))
        numbers_y = list(range(character.y - 3 * constants.SPRITE_SIZE,
                               character.y,
                               character.y + 3 * constants.SPRITE_SIZE))
        random_x = random.choice([element for element in
                                 range(-1 * constants.SPRITE_SIZE,
                                       constants.SCREEN_X
                                       + constants.SPRITE_SIZE)
                                 if element != numbers_x])
        random_y = random.choice([element for element in
                                 range(-1 * constants.SPRITE_SIZE,
                                       constants.SCREEN_Y
                                       + constants.SPRITE_SIZE)
                                 if element != numbers_y])

        for ghost_number in range(len(ghosts)):
            ghosts[ghost_number].move(random_x, random_y)
            break

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

    # SOUND
    # Sound library
    # Shooting sound
    sword_swoosh_sound = open("sword_swoosh.wav", 'rb')
    # Ghosts hitting character
    character_hit_sound = open("character_hit.wav", 'rb')
    # Sword hitting ghosts
    ghost_hit_sound = open("ghost_hit.wav", 'rb')

    # Sound setup
    sound = ugame.audio
    # Stop all sound
    sound.stop()
    # Unmute
    sound.mute(False)

    # BUTTON STATES
    # Buttons with state information
    a_button = constants.button_state["button_up"]

    # SPRITES CREATION
    # Character sprite being displayed
    character = stage.Sprite(game_image_bank, 3, 75, 66)

    # Creates sword swoops
    sword_hits = []
    sword_direction = []
    for sword_number in range(constants.TOTAL_NUMBER_OF_SWORD_HITS):
        a_single_hit = stage.Sprite(game_image_bank, 5,
                                       constants.OFF_SCREEN_X,
                                       constants.OFF_SCREEN_Y)
        sword_hits.append(a_single_hit)
        # Sets bullet direction
        sword_direction.append("")
        direction = "Up"

    # Creates ghosts
    ghosts = []
    for ghost_number in range(constants.TOTAL_NUMBER_OF_GHOSTS):
        a_single_ghost = stage.Sprite(game_image_bank, 6,
                                      constants.OFF_SCREEN_X,
                                      constants.OFF_SCREEN_Y)
        ghosts.append(a_single_ghost)

    show_ghost()

    difficulty = 0.5

    # STAGE AND RENDER
    # Creates a stage for the background
    # Sets frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # Sets sprite layers and show up in order
    game.layers = ([score_text] + sword_hits + [character] + ghosts
                   + [game_background])
    # Renders all sprites, only once
    game.render_block()

    # GAME LOOP
    while True:

        # USER MOVEMENT + SHOOTING
        keys = ugame.buttons.get_pressed()

        # Button states to use sword
        if keys & ugame.K_O != 0:
            if a_button == constants.button_state["button_up"]:
                a_button = constants.button_state["button_just_pressed"]
            elif a_button == constants.button_state["button_just_pressed"]:
                a_button = constants.button_state["button_still_pressed"]
        else:
            if a_button == constants.button_state["button_still_pressed"]:
                a_button = constants.button_state["button_released"]
            else:
                a_button = constants.button_state["button_up"]
        if keys & ugame.K_RIGHT:
            # Move right with constraints of the right border
            if character.x <= constants.SCREEN_X - 2 * constants.SPRITE_SIZE:
                character.move(character.x + constants.SPRITE_MOVEMENT_SPEED,
                               character.y)
            else:
                character.move(constants.SCREEN_X - 2 * constants.SPRITE_SIZE,
                               character.y)
            character.set_frame(2, 0)
            direction = "Right"
        if keys & ugame.K_LEFT:
            # Move left with constraints of the left border
            if character.x >= constants.SCREEN_X - 9 * constants.SPRITE_SIZE:
                character.move(character.x - constants.SPRITE_MOVEMENT_SPEED,
                               character.y)
            else:
                character.move(constants.SPRITE_SIZE, character.y)
            character.set_frame(2, 4)
            direction = "Left"
        if keys & ugame.K_UP:
            # Moves down with constraints of the ceiling
            if character.y >= constants.SPRITE_SIZE:
                character.move(character.x,
                               character.y - constants.SPRITE_MOVEMENT_SPEED)
            else:
                character.move(character.x, constants.SPRITE_SIZE)
            character.set_frame(3, 0)
            direction = "Up"
        if keys & ugame.K_DOWN:
            # Moves down with constraints of the ground
            if character.y <= constants.SCREEN_Y - 2 * constants.SPRITE_SIZE:
                character.move(character.x,
                               character.y + constants.SPRITE_MOVEMENT_SPEED)
            else:
                character.move(character.x,
                               constants.SCREEN_Y - 2 * constants.SPRITE_SIZE)
            character.set_frame(4, 0)
            direction = "Down"

        # Hit with sound
        if a_button == constants.button_state["button_just_pressed"]:
            for sword_number in range(len(sword_hits)):
                if sword_hits[sword_number].x < 0:
                    sword_hits[sword_number].move(character.x, character.y)
                    sword_direction[sword_number] = direction
                    sound.play(sword_swoosh_sound)
                    break

        # SET DIFFICULTY
        ghost_speed = difficulty / 10
        if score % 10 == 0:
            difficulty += 0.025

        # SWORD SWOOSH MOVEMENT
        # When sword hits get used, check the direction for movement.
        for sword_number in range(len(sword_hits)):
            if sword_hits[sword_number].x > -1 * constants.SPRITE_SIZE:
                if sword_direction[sword_number] == "Up":
                    sword_hits[sword_number].move(sword_hits[sword_number].x,
                                                  sword_hits[sword_number].y
                                                  - constants.SWORD_SPEED)
                    sword_hits[sword_number].set_frame(5, 0)
                if sword_direction[sword_number] == "Down":
                    sword_hits[sword_number].move(sword_hits[sword_number].x,
                                                  sword_hits[sword_number].y
                                                  + constants.SWORD_SPEED)
                    sword_hits[sword_number].set_frame(5, 2)
                if sword_direction[sword_number] == "Left":
                    sword_hits[sword_number].move(sword_hits[sword_number].x
                                                  - constants.SWORD_SPEED,
                                                  sword_hits[sword_number].y)
                    sword_hits[sword_number].set_frame(5, 3)
                if sword_direction[sword_number] == "Right":
                    sword_hits[sword_number].move(sword_hits[sword_number].x
                                                  + constants.SWORD_SPEED,
                                                  sword_hits[sword_number].y)
                    sword_hits[sword_number].set_frame(5, 1)

            # Move back sword hits to "staging"
            # if they are too far from the character
            # Right
            if sword_hits[sword_number].x > (character.x
                                             + 2 * constants.SPRITE_SIZE):
                sword_hits[sword_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)
            # Right
            if sword_hits[sword_number].x < (character.x
                                             - 2 * constants.SPRITE_SIZE):
                sword_hits[sword_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)
            # Down
            if sword_hits[sword_number].y > (character.y
                                             + 2 * constants.SPRITE_SIZE):
                sword_hits[sword_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)
            # Up
            if sword_hits[sword_number].y < (character.y
                                             - 2 * constants.SPRITE_SIZE):
                sword_hits[sword_number].move(constants.OFF_SCREEN_X,
                                              constants.OFF_SCREEN_Y)

        # GHOST MOVEMENT
        # Ghost's movement towards character
        for ghost_number in range(len(ghosts)):
            if ghosts[ghost_number].x > -1 * constants.SPRITE_SIZE:
                # Right of character (horizontal)
                if ghosts[ghost_number].x > character.x:
                    ghosts[ghost_number].move(ghosts[ghost_number].x
                                              - ghost_speed,
                                              ghosts[ghost_number].y)
                    ghosts[ghost_number].set_frame(6, 0)
                # Left of character (horizontal)
                if ghosts[ghost_number].x < character.x:
                    ghosts[ghost_number].move(ghosts[ghost_number].x
                                              + ghost_speed,
                                              ghosts[ghost_number].y)
                    ghosts[ghost_number].set_frame(6, 4)
                # Under character (vertical)
                if ghosts[ghost_number].y > character.y:
                    ghosts[ghost_number].move(ghosts[ghost_number].x,
                                              ghosts[ghost_number].y
                                              - ghost_speed)
                # Over character (vertical)
                if ghosts[ghost_number].y < character.y:
                    ghosts[ghost_number].move(ghosts[ghost_number].x,
                                              ghosts[ghost_number].y
                                              + ghost_speed)
                # Stay if the same
                if ghosts[ghost_number].x == character.x:
                    ghosts[ghost_number].move(ghosts[ghost_number].x,
                                              ghosts[ghost_number].y)
                # Stay if the same
                if ghosts[ghost_number].y == character.y:
                    ghosts[ghost_number].move(ghosts[ghost_number].x,
                                              ghosts[ghost_number].y)

        # HIT COLLISION
        # Sword hitting ghosts
        for sword_number in range(len(sword_hits)):
            if sword_hits[sword_number].x > 0:
                for ghost_number in range(len(ghosts)):
                    if ghosts[ghost_number].x > 0:
                        if stage.collide(sword_hits[sword_number].x + 1,
                                         sword_hits[sword_number].y,
                                         sword_hits[sword_number].x + 15,
                                         sword_hits[sword_number].y + 9,
                                         ghosts[ghost_number].x + 3,
                                         ghosts[ghost_number].y,
                                         ghosts[ghost_number].x + 13,
                                         ghosts[ghost_number].y + 13):
                            ghosts[ghost_number].move(constants.OFF_SCREEN_X,
                                                      constants.OFF_SCREEN_Y)
                            sword_hits[sword_number].move(constants.OFF_SCREEN_X,
                                                          constants.OFF_SCREEN_Y)
                            sound.stop()
                            sound.play(ghost_hit_sound)
                            show_ghost()
                            score += 1
                            score_text.clear()
                            score_text.cursor(0, 0)
                            score_text.move(1, 1)
                            score_text.text("Score: {0}".format(score))

        # Ghosts hitting the character
        for ghost_number in range(len(ghosts)):
            if ghosts[ghost_number].x > 0:
                if stage.collide(ghosts[ghost_number].x + 3,
                                 ghosts[ghost_number].y,
                                 ghosts[ghost_number].x + 13,
                                 ghosts[ghost_number].y + 13,
                                 character.x,
                                 character.y + 1,
                                 character.x + 15,
                                 character.y + 15):
                    sound.stop()
                    sound.play(character_hit_sound)
                    time.sleep(1.0)
                    game_over_scene(score)

        # RENDER AND REDRAW
        # Renders and redraws the sprites that move
        game.render_sprites(ghosts + sword_hits + [character])
        # Waits until refresh rate finishes
        game.tick()


def game_over_scene(final_score):
    # Game over scene

    # SOUND
    sound = ugame.audio
    sound.stop()

    # IMAGE_BANK
    over_image_bank = stage.Bank.from_bmp16("splash_over_image_bank.bmp")

    # BACKGROUND
    # sets the background to image 0 in the image Bank
    over_background = stage.Grid(over_image_bank, constants.SCREEN_GRID_X,
                                 constants.SCREEN_GRID_Y)

    # TEXT
    text = []
    text1 = stage.Text(width=29, height=12, font=None,
                       palette=constants.PALETTE, buffer=None)
    text1.move(22, 20)
    text1.text("Final Score: {:0>2d}".format(final_score))
    text.append(text1)

    text2 = stage.Text(width=29, height=14, font=None,
                       palette=constants.PALETTE, buffer=None)
    text2.move(43, 60)
    text2.text("GAME OVER")
    text.append(text2)

    text3 = stage.Text(width=29, height=14, font=None,
                       palette=constants.PALETTE, buffer=None)
    text3.move(35, 110)
    text3.text("PRESS START")
    text.append(text3)

    # STAGE AND RENDER
    # Creates a stage for the background
    # Sets frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # Sets sprite layers and show up in order
    game.layers = text + [over_background]
    # Renders all sprites, only once
    game.render_block()

    while True:
        # get user input
        keys = ugame.buttons.get_pressed()

        # Start button pressed
        if keys & ugame.K_START != 0:
            supervisor.reload()

        # update game logic
        game.tick()


# Makes this file run as the main file of the program, and runs game_scene()
if __name__ == "__main__":
    menu_scene()
