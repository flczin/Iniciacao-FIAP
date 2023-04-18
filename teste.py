import cv2
import mediapipe as mp
import pyautogui

# Load the cascades for detecting the eyes
eye_cascade_left = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_lefteye_2splits.xml')
eye_cascade_right = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_righteye_2splits.xml')

screen_w, screen_h = pyautogui.size()

# Initialize the video capture object
cap = cv2.VideoCapture(0)

face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect the right eye
    eyes_right = eye_cascade_right.detectMultiScale(gray, 1.3, 5)

    # Draw a rectangle around the right eye and create another frame with only the right eye
    for (x, y, w, h) in eyes_right:
        eye_frame_right = frame[y:y+h, x:x+w]
        eye_frame_right = cv2.resize(eye_frame_right, (100, 100))
        gray_frame = cv2.cvtColor(eye_frame_right, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(gray_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = eye_frame_right.shape
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(eye_frame_right, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = screen_w / frame_w * x
                    screen_y = screen_h / frame_h * y
                    pyautogui.moveTo(screen_x, screen_y)

        cv2.imshow('eye', eye_frame_right)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Wait for the 'q' key to be pressed to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
