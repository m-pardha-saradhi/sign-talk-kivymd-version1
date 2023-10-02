import cv2
import mediapipe as mp
import numpy as np
from keras.models import load_model
import joblib
import os
import shutil

Words_predicted = []

def run_model_by_video(video_path):

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.6, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils  # Import the drawing utilities

    # Load the trained LSTM model
    model = load_model('gesture_classification.keras')  # Replace with the path to your trained model

    # Open the video file
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
                # Convert the NormalizedLandmark objects to numerical representation
                landmarks_numeric = np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks.landmark])

                # Store the hand landmarks in the sequence
                landmarks_sequence.append(landmarks_numeric)

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


    # Assuming max_sequence_length is the desired sequence length
    max_sequence_length = 50  # Change this to your desired value - no of frames

    # Preprocess the landmarks sequences to have a consistent length
    num_landmarks = 21

    # Truncate or pad the sequence to match max_sequence_length
    if len(landmarks_sequence) >= max_sequence_length:
        landmarks_sequence = landmarks_sequence[:max_sequence_length]
    else:
        num_landmarks = 21
        num_coordinates = 3
        padding = np.zeros((max_sequence_length - len(landmarks_sequence), num_landmarks, num_coordinates))
        landmarks_sequence = np.concatenate((landmarks_sequence, padding), axis=0)

    # Convert the landmarks sequence to a numpy array
    landmarks_sequence = np.array(landmarks_sequence)

    print(landmarks_sequence.shape)

    # Assuming all_landmarks_sequences has shape (num_samples, sequence_length, num_landmarks, num_coordinates)
    # You need to reshape it to (num_samples, sequence_length, num_landmarks * num_coordinates)
    landmarks_sequence = landmarks_sequence.reshape(
        1,
        landmarks_sequence.shape[0],
        landmarks_sequence.shape[1] * landmarks_sequence.shape[2]
    )
    # landmarks_sequence.shape[0] = frame size
    # landmarks_sequence.shape[1] = 21 (no of landmarks of hands)
    # landmarks_sequence.shape[2] = x, y, z co-ordinates

    # Use the trained model to predict
    # Ensure that you preprocess the landmarks_sequence similarly to how you preprocessed during training
    # predicted_probs = model.predict(np.expand_dims(landmarks_sequence, axis=0))

    print(landmarks_sequence.shape)

    predicted_probs = model.predict(landmarks_sequence)
    print(predicted_probs)

    # Get the class with the highest probability as the predicted gesture
    predicted_class = np.argmax(predicted_probs)

    label_encoder = joblib.load('label_encoder.joblib')

    # Decode the numeric label back to the original class label
    predicted_label = label_encoder.inverse_transform([predicted_class])[0]

    print("Predicted Gesture:", predicted_label)

    return predicted_label



# Concurrent threads for video writting and frames extraction

# Run time - 60 sec

# Process gesture frames concurrently
def process_gesture(gesture_frames, output_path):
    height, width, _ = gesture_frames[0].shape
    output_video_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), 30, (width, height))
    for gesture_frame in gesture_frames:
        output_video_writer.write(gesture_frame)
    output_video_writer.release()


def runModel():
    # Initialize Mediapipe hands module
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.6, min_tracking_confidence=0.5)

    # Load the input video
    video_path = 'captured_video.avi'
    cap = cv2.VideoCapture(video_path)

    # Create a folder for saving gesture videos
    output_folder = 'gestures'

    if os.path.exists(output_folder):
        try:
            shutil.rmtree(output_folder)
            print(f"Contents of '{output_folder}' removed successfully.")
            os.makedirs(output_folder)
        except Exception as e:
            print(f"Error removing contents of '{output_folder}': {e}")
    else:
        print(f"'{output_folder}' does not exist.")
        os.makedirs(output_folder)

    # Initialize variables for gesture segmentation
    gesture_frame_count = 0
    gesture_frames = []
    gesture_num = 1
    min_gesture_frames = 30  # Minimum number of frames to consider as a gesture

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the BGR frame to RGB for Mediapipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Detect hands in the frame
        results = hands.process(rgb_frame)

        # Check if hands are detected
        if results.multi_hand_landmarks:
            gesture_frame_count += 1
            gesture_frames.append(frame)
        else:
            if(gesture_frame_count != 0): print(gesture_frame_count)
            if gesture_frame_count >= min_gesture_frames:
                output_path = os.path.join(output_folder, f'gesture_{gesture_num}.avi')
                process_gesture(gesture_frames, output_path)
                gesture_num += 1

            gesture_frame_count = 0
            gesture_frames = []


    # Release resources
    cap.release()
    cv2.destroyAllWindows()


    video_paths = os.listdir('gestures')
    # print(len(video_paths), ' gestures recognised ')
    for video in video_paths:
        # print(video)
        res = run_model_by_video('gestures/'+video)
        Words_predicted.append(res)
    
    return Words_predicted

