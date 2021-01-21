#!/usr/bin/env python3

# Created by Ryan Chung Kam Chung
# Created in January 2021
# Constants file for code.py


# Pybadge screen is 10x8 sprites (16x16)
SCREEN_GRID_X = 10
SCREEN_GRID_Y = 8
SPRITE_SIZE = 16

# Pybadge screen is 160x128 pixels
SCREEN_X = 160
SCREEN_Y = 128

# Frames per second that the game will run on
FPS = 60

# How fast the sprites move
SPRITE_MOVEMENT_SPEED = 1

# Button state
button_state = {
    "button_up": "up",
    "button_just_pressed": "just pressed",
    "button_still_pressed": "still pressed",
    "button_released": "released"
}

# Alien constants
TOTAL_NUMBER_OF_GHOSTS = 1

# Bullet constants
SWORD_SPEED = 2
TOTAL_NUMBER_OF_SWORD_HITS = 1

# When a bullet goes back to "staging"
OFF_SCREEN_X = -1 * SPRITE_SIZE
OFF_SCREEN_Y = -1 * SPRITE_SIZE
OFF_TOP_SCREEN = -1 * SPRITE_SIZE
OFF_BOTTOM_SCREEN = SCREEN_Y + SPRITE_SIZE

# Text colour palette
PALETTE = (b'\xff\xff\x00\x22\xcey\x22\xff\xff\xff\xff\xff\xff\xff\xff\xff'
           b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')
