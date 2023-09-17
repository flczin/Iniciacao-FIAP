import cv2
import mediapipe as mp
import pyautogui
import datetime
from enum import Enum
import sys
import getopt

from cv2 import VideoCapture


# Problably is better to name it screen than games
class Games(Enum):
    main_screen = 0
    flappy = 1
    car_game = 2
    brick_game = 3


argv = sys.argv[1:]
game = ""
value = ""
try:
    options, args = getopt.getopt(argv, "g:d:", ["game =",
                                                 "dev ="])
except:
    print("No enough arguments")


for name, value in options:
    if name in ["-g", "--game"]:
        game = value
    if name in ["-d", "--dev"]:
        dev = value


def custom_print(printing):
    if dev == "true":
        print(printing)


# get the frame of the camera.
def getPositions(camera_cv2: VideoCapture, screen: Games, curr_time: datetime, screen_x_get: int, screen_y_get: int):
    # starts the camera. The number is the index of the cameras connected to your device.
    cam = camera_cv2

    # points of the mesh of the face. (cant explain it better)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

    # size of your current screen
    screen_w, screen_h = pyautogui.size()

    # variables to make it possible to use outside the scope

    downclick = False

    screen_x = 0
    screen_y = 0
    screen_x_atual = screen_x_get
    screen_x_anterior = 0
    screen_y_atual = screen_y_get
    screen_y_anterior = 0
    pos_atual = "C"
    ttl = curr_time
    x_eye_cam = 0
    y_eye_cam = 0
    x = 0
    y = 0

    _, frame = cam.read()

    # flips the camera to match (letf -> left)
    frame = cv2.flip(frame, 1)

    # turns the video to grayscale colors, so it's easier to process.
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # return the landmarks in the face detected.
    output = face_mesh.process(gray_frame)

    # return a list of all landmarks of the face
    landmark_points = output.multi_face_landmarks

    # gets resolution of the capture images
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        # pick only the landmarks of the first detected face
        landmarks = landmark_points[0].landmark

        # points in the face for both eye and the point where the camera will follow
        # prob has better way to do this and maybe it wont perform like suck
        points = landmarks[285:287] + landmarks[474:478]

        # iterate from the points in the face
        for id, landmark in enumerate(points):

            # id of landmark for the camera (it can be either 0 or 1)
            # change for what suits best for you
            if id == 0:
                x_eye_cam = int(landmark.x * frame_w)
                y_eye_cam = int(landmark.y * frame_h)

            # calculate the points of the eye in the frame of the camera (its what is most likely)
            if id in range(2, 6):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)

            # draw the landmarks around the eye
            # frame: the window where the cv2 will draw. So it's the webcam screen
            # (x, y): the coordnates of the circle where it should draw
            # 3: size of the circles in the draw
            # last one is color
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            # make another frame that will follow the eye.
            # the values is the range of the camera. [start]:[to]
            eye_frame = frame[y_eye_cam - 20:y_eye_cam + 45, x_eye_cam:x_eye_cam + 60]
            eye_frame = cv2.resize(eye_frame, (200, 200))

            # we do this if to make sure the y and x of the eye is some value in the screen
            # i dont know if this is surely the best method to do this. Maybe there is some
            # better way to do this
            if id == 3:
                # calculations to match the eye location to the current
                # screen in your computer
                # change the screen w and h to 200 more or less to make the frame to move more than it should
                # normaly. See if this is what is really happening. Because frame * x or y is the landmark
                # because up there we can see we mult the landmark by its frame. Well se if is really true. lol
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y

                # move the cursor to the calculated x and y

                # Command to move the car in the game
                # for now because of the hard code values, the best option is to be at arm's lenght from
                # the camera, and try to move your head accordingly, the same aplies you will need to be
                # at somewhat the center of the camera. (NEED TO FIX), because of my tight schedule,
                # not possible right now, and would like to see some solutions.

                # verify this ifs if they need.
                if screen == Games.main_screen:
                    # calculations to match the eye location to the current
                    # screen in your computer
                    screen_x = screen_w / frame_w * x
                    screen_y = screen_h / frame_h * y

                    # move the cursor to the calculated x and y
                    pyautogui.moveTo(screen_x, screen_y)

                if screen == Games.car_game:
                    # make a way to restart the game, and a way to leave the game to the main screen
                    screen_x_anterior = screen_x_atual
                    screen_x_atual = screen_x
                    diff = screen_x_atual - screen_x_anterior
                    duration = datetime.datetime.now() - ttl
                    if diff > 5 and duration.total_seconds() > 1.0:
                        pyautogui.press('right')
                        custom_print("right")
                        downclick = True
                        if pos_atual == "C":
                            custom_print("direita")
                            pos_atual = "D"
                        if pos_atual == "E":
                            custom_print("centro")
                            pos_atual = "C"
                        ttl = datetime.datetime.now()
                    if diff < -5 and duration.total_seconds() > 1.0:
                        pyautogui.press('left')
                        custom_print("left")
                        downclick = True
                        if pos_atual == "C":
                            custom_print("esquerda")
                            pos_atual = "E"
                        if pos_atual == "D":
                            custom_print("centro")
                            pos_atual = "C"
                        ttl = datetime.datetime.now()

                # this is the worst experience ever
                if screen == Games.flappy:
                    screen_y_anterior = screen_y_atual
                    screen_y_atual = screen_y
                    diff = screen_y_atual - screen_y_anterior
                    duration = datetime.datetime.now() - ttl
                    if diff > 3 and duration.total_seconds() > 1.0:
                        pyautogui.press('down')
                        custom_print("down")
                        downclick = True
                        if pos_atual == "C":
                            custom_print("down")
                            pos_atual = "D"
                        if pos_atual == "U":
                            custom_print("center")
                            pos_atual = "C"
                        ttl = datetime.datetime.now()
                    if diff < -3 and duration.total_seconds() > 1.0:
                        pyautogui.press('space')
                        custom_print("up")
                        downclick = True
                        if pos_atual == "C":
                            custom_print("up")
                            pos_atual = "U"
                        if pos_atual == "D":
                            custom_print("centro")
                            pos_atual = "C"
                        ttl = datetime.datetime.now()

                if screen == Games.brick_game:
                    # make a way to restart the game, and a way to leave the game to the main screen
                    middle_screen_x = 980
                    screen_x_atual = screen_x
                    diff = screen_x_atual - middle_screen_x
                    if diff > 5:
                        pyautogui.press('right')
                        custom_print("right")

                    if diff < -5:
                        pyautogui.press('left')
                        custom_print("left")

    return screen_x, screen_y, ttl


# use this here when choosing a game, maybe, and when the screen is pause mode
# when the player is gaming the commands will change.
# pyautogui.moveTo(screen_x, screen_y)

def main():
    camera = cv2.VideoCapture(0)
    time_now = datetime.datetime.now()
    pos_x = 0
    pos_y = 0

    while True:
        pos_x, pos_y, time_now = getPositions(camera, Games[game], time_now, pos_x, pos_y)

        # print("Position x: " + str(pos_x))
        # print("Position y: " + str(pos_y))

        # stops programam when 'Q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

# Make another flag so that instead of this approach, we will make the center of the screen the middle
# and then after some ammount of movement of the eye, that we have the number, the game will be able
# to input multiple times the game.
