import time
import pygame
from games.flappy.fly import main_flappy
from games.car_game.car_game import main_car
from games.brick_game.brick_main import brick_main_start
import os
import subprocess


class Tracker:
    _init_already = False

    def __init__(self, cmd):
        if not self._init_already:
            self.process = subprocess.Popen(cmd, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            self._init_already = True

    def kill(self):
        if self._init_already:
            subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.process.pid)])
            self._init_already = False


os.environ['SDL_VIDEO_CENTERED'] = '1'


def init_pygame():
    pygame.init()

    # Initialize screen
    screen_game = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Main Menu")
    return screen_game


screen = init_pygame()

dev = True

if dev is True:
    main_screen_cmd = "python ./../testCLI.py -g main_screen -d true"
    flappy_cmd = "python ./../testCLI.py -g flappy -d true"
    car_game_cmd = "python ./../testCLI.py -g car_game -d true"
    brick_game_cmd = "python ./../testCLI.py -g brick_game -d true"
else:
    main_screen_cmd = "python ./../testCLI.py -g main_screen -d false"
    flappy_cmd = "python ./../testCLI.py -g flappy -d false"
    car_game_cmd = "python ./../testCLI.py -g car_game -d false"
    brick_game_cmd = "python ./../testCLI.py -g brick_game -d false"

main_screen = None


def main_menu():
    global main_screen, screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if main_screen is None:
            main_screen = Tracker(main_screen_cmd)

        screen.fill((255, 255, 255))

        # Draw buttons for game selection
        font = pygame.font.Font(None, 36)
        game1_button = pygame.Rect(200, 200, 400, 50)
        game2_button = pygame.Rect(200, 300, 400, 50)
        game3_button = pygame.Rect(200, 400, 400, 50)
        pygame.draw.rect(screen, (0, 128, 255), game1_button)
        pygame.draw.rect(screen, (0, 128, 255), game2_button)
        pygame.draw.rect(screen, (0, 128, 255), game3_button)

        game1_text = font.render("Flappy Bird", True, (255, 255, 255))
        game2_text = font.render("Car Game", True, (255, 255, 255))
        game3_text = font.render("Brick Game", True, (255, 255, 255))
        screen.blit(game1_text, (320, 210))
        screen.blit(game2_text, (320, 310))
        screen.blit(game3_text, (320, 410))

        pygame.display.flip()

        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()

        if game1_button.collidepoint(mouse_pos) and mouse_clicked[0]:
            main_screen.kill()
            main_screen = None
            flappy = Tracker(flappy_cmd)
            time.sleep(5)  # loading to have the time of the tracker to start
            main_flappy()  # Start game 1
            flappy.kill()

        if game2_button.collidepoint(mouse_pos) and mouse_clicked[0]:
            main_screen.kill()
            main_screen = None
            car_game = Tracker(car_game_cmd)
            time.sleep(5)  # loading to have the time of the tracker to start
            main_car()  # Start game 2
            car_game.kill()
            screen = init_pygame()

        if game3_button.collidepoint(mouse_pos) and mouse_clicked[0]:
            main_screen.kill()
            main_screen = None
            brick_game = Tracker(brick_game_cmd)
            time.sleep(5)  # loading to have the time of the tracker to start
            brick_main_start()  # Start game 3
            brick_game.kill()


if __name__ == "__main__":
    main_menu()
