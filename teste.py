import cv2
import mediapipe as mp
import pyautogui

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
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y

                # move the cursor to the calculated x and y
                pyautogui.moveTo(screen_x, screen_y)

    # stops programam when 'Q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # screen of the eye
    cv2.imshow('eye', eye_frame)

    # screen of the webcam        
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)

cam.release()
cv2.destroyAllWindows()

# Mesh points
# Left eye = 469:474
# Right eye = 474: 478
# Right point from eye 285:287 // mostly for the camera
