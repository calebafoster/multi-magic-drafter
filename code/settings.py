from pathlib import Path
from pygame.math import Vector2 as vector

current_card_pool = 'commander'

ROOT = Path(__file__).parent.parent
IMAGES = ROOT / 'images'
SECONDS = IMAGES / 'seconds'
CARD_POOL_JSON = ROOT / f'{current_card_pool}.json'
CARD_POOL_FOLDER = ROOT / current_card_pool

CARD_DIMENSIONS = vector(745, 1040)
CARD_SCALE_PRIME = 0.6
SURFACE_DIMENSIONS = vector(1280, 720)
SURFACE_CENTER = vector(SURFACE_DIMENSIONS.x / 2, SURFACE_DIMENSIONS.y / 2)

HOST = "127.0.0.1"
PORT = 55885
