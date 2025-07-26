import pygame

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.gravity = 0.5
        self.jump_strength = -10
        self.velocity = 0

        # Chargement des images
        self.img_normal = pygame.image.load("images/flappy_normal.jfif").convert_alpha()
        self.img_jump = pygame.image.load("images/flappy_saut.jfif").convert_alpha()

        # Redimensionnement facultatif
        self.img_normal = pygame.transform.scale(self.img_normal, (50, 50))
        self.img_jump = pygame.transform.scale(self.img_jump, (50, 50))

        self.current_image = self.img_normal

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        # Choisir l’image selon la vitesse
        if self.velocity < 0:
            self.current_image = self.img_jump
        else:
            self.current_image = self.img_normal

    def jump(self):
        self.velocity = self.jump_strength

    def draw(self, window):
        window.blit(self.current_image, (int(self.x), int(self.y)))

    def getY(self):
        return self.y
    
    def getX(self):
        return self.x
    
    def setY(self,y):
        self.y=y
