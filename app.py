import cv2
import mediapipe as mp
import pyautogui

pyautogui.FAILSAFE = False
# Initialize MediaPipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

# Set the video resolution to a higher value
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Define finger indices
index_finger_index = 8
middle_finger_index = 12

# Define a function to get finger coordinates
def get_finger_coords(hand_landmarks, finger_index):
    landmark = hand_landmarks.landmark[finger_index]
    x = int(landmark.x * cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    y = int(landmark.y * cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return x, y

# Define a function to smooth the cursor movement
def smooth_movement(x, y, weight=0.5):
    prev_x, prev_y = pyautogui.position()
    new_x = int(prev_x * (1 - weight) + x * weight)
    new_y = int(prev_y * (1 - weight) + y * weight)
    return new_x, new_y

# Define a function to map the finger coordinates to the screen coordinates
def map_coords_to_screen(x, y, frame_width, frame_height):
    screen_width, screen_height = pyautogui.size()
    x_ratio = x / frame_width
    y_ratio = y / frame_height

    # Apply a non-linear mapping function
    mapped_x = int(screen_width * (x_ratio ** 1.2))
    mapped_y = int(screen_height * (y_ratio ** 1.2))

    return mapped_x, mapped_y

while True:
    # Capture frame from the camera
    ret, frame = cap.read()

    # Flip the frame horizontally for a better view
    frame = cv2.flip(frame, 1)

    # Get hand landmarks
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        # Get the first hand landmarks
        hand_landmarks = results.multi_hand_landmarks[0]

        # Get the coordinates of the index and middle fingers
        index_x, index_y = get_finger_coords(hand_landmarks, index_finger_index)
        middle_x, middle_y = get_finger_coords(hand_landmarks, middle_finger_index)

        # Smooth the cursor movement
        index_x, index_y = smooth_movement(index_x, index_y)

        # Map the finger coordinates to the screen coordinates
        mapped_x, mapped_y = map_coords_to_screen(index_x, index_y, cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Move the mouse cursor based on the mapped coordinates
        pyautogui.moveTo(mapped_x, mapped_y, duration=0)

        # Perform a click if the middle finger is raised
        if middle_y < index_y:
            pyautogui.click()

    # Display the frame
    cv2.imshow('Hand Tracking', frame)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close the window
cap.release()
cv2.destroyAllWindows()