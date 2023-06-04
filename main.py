import cv2
import mediapipe as mp
import pyautogui

# starts the camera. The number is the index of the cameras connected to your device.
cam = cv2.VideoCapture(0)

# points of the mesh of the face. (cant explain it better)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

# size of your current screen
screen_w, screen_h = pyautogui.size()

x_eye = 0
y_eye = 0
x = 0
y = 0

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

        # prob has better way to do this and maybe it wont perform like suck
        points = landmarks[285:287] + landmarks[474:478]

        # loops over landmarks 474-478 (correspond to the four landmarks around the eye
        # for id, landmark in enumerate(landmarks[474:478]):
        # two eyes gettted
        # for id, landmark in enumerate(landmarks[469:478]):
        # eye lid
        # for id, landmark in enumerate(landmarks[253:260]):
        for id, landmark in enumerate(points):

            # stores last position of the landmarks escaling to the frame size
            if id == 0:
                x_eye = int(landmark.x * frame_w)
                y_eye = int(landmark.y * frame_h)

            if id in range(3, 7):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)

            # draw the landmarks around the eye
            # frame: the window where the cv2 will draw. So it's the webcam screen
            # (x, y): the coordnates of the circle where it should draw
            # 3: size of the circles in the draw
            # last one is color
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            eye_frame = frame[y_eye - 20:y_eye + 45, x_eye:x_eye + 60]
            eye_frame = cv2.resize(eye_frame, (200, 200))

            print(eye_frame)

            # choose one of the four landmark around the eye
            if id == 8:
                # calculations to match the eye location to the current
                # screen in your computer
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y

                # move the cursor to the calculated x and y
                pyautogui.moveTo(screen_x, screen_y)

    # stops programam when 'Q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('eye', eye_frame)
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)

cam.release()
cv2.destroyAllWindows()

# instead of making the center o the screen the middle, maybe we can make the
# person look to a point than after storing the data of how she should look at 
# the middle and some extremities, we can calculate how much she moves and than
# make the movement acordiling.

# Use 2 eyes of only 1

# Prob 2 i believe

# we could make the screen with the (0,0) instead of top left, in the middle,
# so we could multiply the screen with a variable to make the cursor to move 
# more than normal.