import pygame
import random

class Pipe:
    def __init__(self, x, gap_height=200):
        self.x = x
        self.speed = 3
        self.gap = gap_height

        self.passed = False

        # Charger les images
        self.image_top = pygame.image.load("images/pipe_haut.jpg").convert_alpha()
        self.image_bottom = pygame.image.load("images/pipe_bas.jpg").convert_alpha()

        # Largeur d’un tuyau
        self.width = self.image_top.get_width()

        # Déterminer la hauteur du tuyau supérieur
        self.height_top = random.randint(50, 400)

        # Créer les surfaces coupées selon les hauteurs
        self.top_rect = self.image_top.get_rect(topleft=(self.x, self.height_top - self.image_top.get_height()))
        self.bottom_rect = self.image_bottom.get_rect(topleft=(self.x, self.height_top + self.gap))

    def update(self):
        self.x -= self.speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, window):
        window.blit(self.image_top, self.top_rect)
        window.blit(self.image_bottom, self.bottom_rect)

    def is_off_screen(self):
        return self.x + self.width < 0

    def collide(self, bird):
        bird_rect = bird.current_image.get_rect(topleft=(bird.x, bird.y))
        return bird_rect.colliderect(self.top_rect) or bird_rect.colliderect(self.bottom_rect)