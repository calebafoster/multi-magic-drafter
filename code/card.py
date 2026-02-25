import pygame
import requests
import time
import threading
from settings import IMAGES, SECONDS, CARD_DIMENSIONS, CARD_SCALE_PRIME

class Card(pygame.sprite.Sprite):
    def __init__(self, card_dict, *groups):
        super().__init__(*groups)

        self.dict = card_dict
        self.name = self.dict['name']
        self.id = self.dict['id']

        self.dual_faced = False

        self.scaled_index = 0
        self.second_bool = False
        self.scaled_images = []
        self.scaled_rects = []

        self.source_images = []
        self.image_path = IMAGES / f'{self.id}.png'
        self.image = pygame.image.load('../images/missing.png').convert_alpha()
        self.source_images.append(self.image)
        self.rect = self.image.get_rect()

        if 'card_faces' in self.dict:
            self.dual_faced = True
            self.second_image_path = SECONDS / f'{self.id}.png'
            self.second_image = pygame.image.load('../images/missing.png').convert_alpha()
            self.source_images.append(self.second_image)

        threading.Thread(target=self.import_assets).start()

    def import_assets(self):
        images = []
        while True:
            if self.dual_faced and self.image_path.is_file():
                self.second_image = pygame.image.load(self.second_image_path).convert_alpha()

            if self.image_path.is_file():
                images.append(pygame.image.load(self.image_path).convert_alpha())

                if self.dual_faced:
                    images.append(self.second_image)

                self.source_images = images
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
        else:
            print("failed to download")

        if self.dual_faced:
            r = requests.get(self.second_image_url)
            if r.status_code == 200:
                with open(self.second_image_path, 'wb') as f:
                    f.write(r.content)
                print(f'download successful: back face')

    def scale_images(self):
        self.scaled_images = []
        self.scaled_rects = []
        for i in range(self.scaled_index + 1):
            print(i)
            scalar = 0.0
            if i == 0:
                scalar = CARD_SCALE_PRIME / (i + 1)
            else:
                scalar = CARD_SCALE_PRIME / (i + 0.5)
            images = []
            for surf in self.source_images:
                scaled_image = pygame.transform.scale_by(surf, scalar)
                images.append(scaled_image)
            self.scaled_rects.append(images[0].get_rect())
            self.scaled_images.append(images)

    def image_logic(self):
        images = []
        self.scale_images()
        images = self.scaled_images[self.scaled_index]

        self.image = images[self.second_bool]
        self.rect = self.scaled_rects[self.scaled_index]

    def set_scale_index(self, relative_index):
        self.scaled_index = abs(relative_index)

    def update(self, dt):
        self.image_logic()
