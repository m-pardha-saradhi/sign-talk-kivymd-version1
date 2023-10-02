import cv2
import mediapipe as mp
import numpy as np
from keras.models import load_model
import joblib


def run_model_by_frames(frames):

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.6, min_tracking_confidence=0.5)
    mp_drawing = mp.solutions.drawing_utils  # Import the drawing utilities
    
    # Load the trained LSTM model
    model = load_model('gesture_classification.keras')

    landmarks_sequence = []  # List to store sequences of landmarks

    for frame in frames:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            print('hands ')
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks_numeric = np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks.landmark])
                landmarks_sequence.append(landmarks_numeric)
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        else:
            print('hands not detected')
        
        # Display the frame with landmarks
        cv2.imshow('Hand Gestures', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
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
        print(landmarks_sequence)
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