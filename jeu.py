import pygame
import sys
from bird import Bird
from pipe import Pipe
from score_manager import init_db, save_score, get_best_score


# Dimensions (doivent correspondre à main.py)
WIDTH, HEIGHT = 500, 700

# Police globale (facultatif, on peut l'initialiser ici aussi)
pygame.font.init()
FONT = pygame.font.SysFont(None, 48)
BUTTON_FONT = pygame.font.SysFont(None, 36)



# Couleurs
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
DARK_BLUE = (30, 100, 200)
BLACK = (0, 0, 0)
RED = (255,0,0)

# Bouton
def draw_button(text, x, y, width, height, mouse_pos,window):
    button_rect = pygame.Rect(x, y, width, height)
    color = DARK_BLUE if button_rect.collidepoint(mouse_pos) else BLUE
    pygame.draw.rect(window, color, button_rect, border_radius=10)
    text_surf = BUTTON_FONT.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    window.blit(text_surf, text_rect)
    return button_rect


def jeu(window):
    clock = pygame.time.Clock()
    bird = Bird(200,350)
    pipes = []  # Liste des tuyaux
    pipe_timer = 0  # Compteur de frames
    running = True
    font = pygame.font.SysFont(None, 64)
    score = 0

    background_img = pygame.image.load("images/background.jfif").convert()
    bg_x = 0  # Position de départ
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    bg_width = WIDTH
    bg_height = HEIGHT

    while running:
        # Défilement du fond
        bg_x -= 2  # Vitesse de défilement (augmente pour aller plus vite)

        # Réinitialiser quand l'image est complètement partie à gauche
        if bg_x <= -bg_width:
            bg_x = 0

        # Afficher l'image deux fois pour créer un effet de boucle
        window.blit(background_img, (bg_x, 0))
        window.blit(background_img, (bg_x + bg_width, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        bird.update()
        bird.draw(window)

        # Génération automatique de tuyaux
        pipe_timer += 1
        if pipe_timer >= 90:  # toutes les 1.5 secondes environ (60 FPS)
            pipes.append(Pipe(WIDTH))
            pipe_timer = 0

        # Mise à jour et affichage des tuyaux
        for pipe in pipes[:]:  # on copie la liste pour pouvoir la modifier pendant la boucle
            pipe.update()
            pipe.draw(window)

            # Collision avec bird
            if pipe.collide(bird):
                text = font.render("GAME OVER", True, (255, 0, 0))
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
                window.blit(text, text_rect)

                 # SCORE
                score_text = font.render(f"Score : {score}", True, (255, 0, 0))
                score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 60))
                window.blit(score_text, score_rect)
                save_score(score)

                #RECORD
                best_score = get_best_score()
                best_score_text = FONT.render(f"Record : {best_score}", True, (255, 255, 255))
                window.blit(best_score_text, (20, 60))


                pygame.display.update()
                pygame.time.wait(5000)
                accueil(window)
                running = False

            # Supprimer les tuyaux hors écran
            if pipe.is_off_screen():
                pipes.remove(pipe)

            if not pipe.passed and pipe.x + pipe.image_top.get_width() < bird.getX():
                pipe.passed = True
                score += 1


        if(bird.getY()<0 or bird.getY() + bird.current_image.get_height() > HEIGHT ):
            bird.setY(bird.getY())
            # Texte "GAME OVER"
            text = font.render("GAME OVER", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            window.blit(text, text_rect)

            # SCORE
            score_text = font.render(f"Score : {score}", True, (255, 0, 0))
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 60))
            window.blit(score_text, score_rect)
            save_score(score)
            
            #RECORD
            best_score = get_best_score()
            best_score_text = FONT.render(f"Record : {best_score}", True, (255, 255, 255))
            window.blit(best_score_text, (20, 60))

            pygame.display.update()
            pygame.time.wait(8000)
            accueil(window)
            running = False
            
        # Affichage du score
        score_text = FONT.render(f"Score : {score}", True, (255, 255, 255))
        window.blit(score_text, (20, 20))
        pygame.display.update()
        clock.tick(60)


# Accueil
def accueil(window):
    clock = pygame.time.Clock()
    run = True

    while run:
        mouse_pos = pygame.mouse.get_pos()
        background_img = pygame.image.load("images/background.jfif").convert()
        bg_x = 0  # Position de départ
        background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
        window.blit(background_img, (bg_x, 0))

        flappy_img = pygame.image.load("images/flappy_bird.jfif").convert()
        window.blit(flappy_img, (WIDTH//3, HEIGHT //5))

        title_text = FONT.render("GAME OVER", True, RED)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        window.blit(title_text, title_rect)

        #RECORD
        best_score = get_best_score()
        best_score_text = FONT.render(f"Record : {best_score}", True, (255, 255, 255))
        window.blit(best_score_text, (20, 60))

        replay_button = draw_button("ReJouer", WIDTH // 2 - 100, HEIGHT // 2, 200, 60, mouse_pos,window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    run = False
                    jeu(window)  # ✅ on passe la fenêtre à la fonction jeu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False
                    jeu(window)
        pygame.display.update()
        clock.tick(60)
