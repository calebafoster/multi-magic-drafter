from pathlib import Path

current_card_pool = 'commander'

ROOT = Path(__file__).parent.parent
IMAGES = ROOT / 'images'
SECONDS = IMAGES / 'seconds'
CARD_POOL_JSON = ROOT / f'{current_card_pool}.json'
CARD_POOL_FOLDER = ROOT / current_card_pool

HOST = "127.0.0.1"
PORT = 55885
