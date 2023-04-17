import cv2
import mediapipe as mp
import pyautogui

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):

            # this make the points around the eyes
            # ex: so if you change the numbers to fixed amound
            # it will make green fixed dots in the camera image 
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

            # circle around the retina
            # frame: the window where the cv2 will draw. So its the webcam screen
            # (x, y): the coordnates of the circle where it should draw
            # 3: size of the circles in the draw
            # last one is color
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            if id == 1:

                # calculations to match the eye location to the current 
                # screen in your computer
                # calc: cv2 camera height or width * landmark(???)
                screen_x = screen_w * landmark.x
                screen_y = screen_h * landmark.y

                # move the cursor to the calculated x and y
                pyautogui.moveTo(screen_x, screen_y)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
    

# instead of making the center o the screen the middle, maybe we can make the
# person look to a point than after storing the data of how she should look at 
# the middle and some extremities, we can calculate how much she moves and than
# make the movement acordiling.

# Use 2 eyes of only 1

# Prob 2 i believe

# we could make the screen with the (0,0) instead of top left, in the middle,
# so we could multiply the screen with a variable to make the cursor to move 
# more than normal.