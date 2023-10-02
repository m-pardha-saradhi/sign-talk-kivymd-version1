import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.6, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils  # Import the drawing utilities

# Open the video file
video_path = 'captured_video.avi'
cap = cv2.VideoCapture(video_path)

landmarks_sequence = []  # List to store sequences of landmarks

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the frame to RGB and process it with MediaPipe Hands
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Store the hand landmarks in the sequence
            landmarks_sequence.append(hand_landmarks.landmark)
        
        # Draw landmarks on the frame
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Display the frame with or without landmarks
    cv2.imshow('Hand Gestures', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()

# Convert the landmarks sequence to a numpy array
landmarks_sequence = np.array(landmarks_sequence)

# landmarks_sequence now contains the sequence of landmarks over time
# You can use this array as input to your video classification model
