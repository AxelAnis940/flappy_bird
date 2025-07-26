import pygame
import sys
from jeu import jeu  # ✅ on importe la fonction depuis le fichier jeu.py
from score_manager import init_db, save_score, get_best_score

# Initialisation
pygame.init()
pygame.font.init()
init_db()

# Dimensions
WIDTH, HEIGHT = 500, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Accueil")

# Couleurs
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
DARK_BLUE = (30, 100, 200)
BLACK = (0, 0, 0)

# Polices
FONT = pygame.font.SysFont(None, 48)
BUTTON_FONT = pygame.font.SysFont(None, 36)

# Bouton
def draw_button(text, x, y, width, height, mouse_pos):
    button_rect = pygame.Rect(x, y, width, height)
    color = DARK_BLUE if button_rect.collidepoint(mouse_pos) else BLUE
    pygame.draw.rect(WINDOW, color, button_rect, border_radius=10)
    text_surf = BUTTON_FONT.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    WINDOW.blit(text_surf, text_rect)
    return button_rect

# Accueil
def accueil():
    clock = pygame.time.Clock()
    run = True

    while run:
        mouse_pos = pygame.mouse.get_pos()
        background_img = pygame.image.load("images/background.jfif").convert()
        bg_x = 0  # Position de départ
        background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
        WINDOW.blit(background_img, (bg_x, 0))


        flappy_img = pygame.image.load("images/flappy_bird.jfif").convert()
        WINDOW.blit(flappy_img, (WIDTH//3, HEIGHT //4))

        play_button = draw_button("Jouer", WIDTH // 2 - 100, HEIGHT // 2, 200, 60, mouse_pos)

        #RECORD
        best_score = get_best_score()
        best_score_text = FONT.render(f"Record : {best_score}", True, (255, 255, 255))
        WINDOW.blit(best_score_text, (20, 60))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    run = False
                    jeu(WINDOW)  # ✅ on passe la fenêtre à la fonction jeu

        pygame.display.update()
        clock.tick(60)

# Démarrage
if __name__ == "__main__":
    accueil()