import time

import pyautogui
import pygame
from cv2 import VideoCapture
from games.flappy.fly import main_flappy
from games.car_game.car_game import main_car
import os
import cv2
from test import Games, getPositions
from threading import Thread

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

# Initialize screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Main Menu")
cam = cv2.VideoCapture(0)


class EyeTrackerThread(Thread):
    def __init__(self, camera: VideoCapture, curr_screen: Games):
        Thread.__init__(self)
        self.cam = camera
        self.screen = curr_screen
        self.running = True

    def run(self):
        while self.running:
            getPositions(self.cam, self.screen)

    def stop(self):
        self.running = False


flappy_tracker = EyeTrackerThread(cam, Games.flappy)
car_tracker = EyeTrackerThread(cam, Games.car_game)
main_screen_tracker = EyeTrackerThread(cam, Games.main_screen)


def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # main_screen_tracker.start()

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
            # main_screen_tracker.stop()
            flappy_tracker.start()
            main_flappy()  # Start game 1
            flappy_tracker.stop()

        if game2_button.collidepoint(mouse_pos) and mouse_clicked[0]:
            # main_screen_tracker.stop()
            car_tracker.start()
            main_car()  # Start game 2
            car_tracker.stop()


if __name__ == "__main__":
    main_menu()
