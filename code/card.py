import pygame
import requests
import time
import threading
from pathlib import Path
from settings import IMAGES, SECONDS

class Card(pygame.sprite.Sprite):
    def __init__(self, card_dict, *groups):
        super().__init__(*groups)

        self.dict = card_dict
        self.name = self.dict['name']
        self.id = self.dict['id']

        self.dual_faced = False

        self.image_path = IMAGES / f'{self.id}.png'
        self.image = pygame.image.load('images/missing.png').convert_alpha()
        self.rect = self.image.get_rect()

        if 'card_faces' in self.dict:
            self.dual_faced = True
            self.second_image_path = SECONDS / f'{self.id}.png'
            self.second_image = pygame.image.load('images/missing.png').convert_alpha()

        threading.Thread(target=self.import_assets).start()


    def import_assets(self):
        while True:
            if self.dual_faced and self.image_path.is_file():
                self.second_image = pygame.image.load(self.second_image_path).convert_alpha()

            if self.image_path.is_file():
                self.image = pygame.image.load(self.image_path).convert_alpha()

                self.images = [self.image]
                if self.dual_faced:
                    self.images.append(self.second_image)

                break
            else:
                self.download_image()

            time.sleep(0.1)

    def download_image(self):
        if not self.dual_faced:
            self.image_url = self.dict['image_uris']['png']
        else:
            self.image_url = self.dict['card_faces'][0]['image_uris']['png']
            self.second_image_url = self.dict['card_faces'][1]['image_uris']['png']
        r = requests.get(self.image_url)

        if r.status_code == 200:
            with open(self.image_path, 'wb') as f:
                f.write(r.content)
            print(f'download successful: {self.name}')

        if self.dual_faced:
            r = requests.get(self.second_image_url)
            if r.status_code == 200:
                with open(self.second_image_path, 'wb') as f:
                    f.write(r.content)
                print(f'download successful: back face')

    def update(self):
        pass
