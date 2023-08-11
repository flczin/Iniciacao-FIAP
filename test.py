import math
import cv2
import mediapipe as mp
import pyautogui
from enum import Enum


# Problably is better to name it screen than games
class Games(Enum):
    main_screen = 0
    flappy = 1
    car_game = 2


# starts the camera. The number is the index of the cameras connected to your device.
cam = cv2.VideoCapture(0)

# points of the mesh of the face. (cant explain it better)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# size of your current screen
screen_w, screen_h = pyautogui.size()

# variables to make it possible to use outside the scope
x_eye_cam = 0
y_eye_cam = 0
x = 0
y = 0

downclick = False

curr_screen = Games.flappy

while True:
    # get the frame of the camera.
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
                if curr_screen == Games.main_screen:
                    # calculations to match the eye location to the current
                    # screen in your computer
                    screen_x = screen_w / frame_w * x
                    screen_y = screen_h / frame_h * y

                    # move the cursor to the calculated x and y
                    pyautogui.moveTo(screen_x, screen_y)

                if curr_screen == Games.car_game:
                    # make a way to restart the game, and a way to leave the game to the main screen
                    if screen_x > 1100 and not downclick:
                        pyautogui.press('right')
                        print("right")
                        downclick = True

                    if screen_x < 1000 and not downclick:
                        pyautogui.press('left')
                        print("left")
                        downclick = True

                    if 1000 <= screen_x <= 1100 and downclick:
                        downclick = False

                # this is the worst experience ever
                if curr_screen == Games.flappy:
                    if screen_y > 500 and not downclick:
                        pyautogui.press("space")
                        print("space")
                        downclick = True

                    if screen_y < 500 and downclick:
                        downclick = False

                # use this here when choosing a game, maybe, and when the screen is pause mode
                # when the player is gaming the commands will change.
                # pyautogui.moveTo(screen_x, screen_y)

    # stops programam when 'Q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Its here just for the start of the cam, because if we dont have this,
    # when starting it wont have any eey_frame and then it will throw a error
    # if there is no ladmarks, there will be no eye_frame
    # and if there is no verifications, it will break when starting.
    if landmark_points:
        # screen of the eye
        cv2.imshow('eye', eye_frame)

    # screen of the webcam
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)

cam.release()
cv2.destroyAllWindows()

# FIX:
# the camera following the eye, does not resize accordign to the distance of the person
# so if the person is too close to the camera, the camera is possible to not get the
# eye of the person
# Possible fix is in line 69 where the resize of the camera is happening
# Possible fix in line in line 44 where we have a concat of 2 arrays.
# right now that operation is not very good performance wise, so maybe we have a better
# way to do that?

# Mesh points
# Left eye = 469:474
# Right eye = 474: 478
# Right point from eye 285:287 // mostly for the camera
