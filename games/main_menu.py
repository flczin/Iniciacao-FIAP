import pygame
from games.flappy.fly import main_flappy
from games.car_game.car_game import main_car

pygame.init()

# Initialize screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Main Menu")


def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill((255, 255, 255))

        # Draw buttons for game selection
        font = pygame.font.Font(None, 36)
        game1_button = pygame.Rect(200, 200, 400, 50)
        game2_button = pygame.Rect(200, 300, 400, 50)
        pygame.draw.rect(screen, (0, 128, 255), game1_button)
        pygame.draw.rect(screen, (0, 128, 255), game2_button)

        game1_text = font.render("Flappy Bird", True, (255, 255, 255))
        game2_text = font.render("Car Game", True, (255, 255, 255))
        screen.blit(game1_text, (320, 210))
        screen.blit(game2_text, (320, 310))

        pygame.display.flip()

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()

        if game1_button.collidepoint(mouse_pos) and mouse_clicked[0]:
            main_flappy()  # Start game 1

        if game2_button.collidepoint(mouse_pos) and mouse_clicked[0]:
            main_car()  # Start game 2


if __name__ == "__main__":
    main_menu()
