import cv2
import mediapipe as mp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.graphics import Line
from kivy.clock import Clock
import RunFrames

class CameraApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # Create a frame for displaying video
        self.video_frame = Image(size_hint=(1, 0.8))
        self.layout.add_widget(self.video_frame)

        # Create start and stop buttons
        self.start_button = Button(text='Start', size_hint=(0.2, 0.1))
        self.stop_button = Button(text='Stop', disabled=True, size_hint=(0.2, 0.1))
        self.start_button.bind(on_press=self.start_capture)
        self.stop_button.bind(on_press=self.stop_capture)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.stop_button)

        # Create an instance of the hand detection module
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False, max_num_hands=2,
            min_detection_confidence=0.8, min_tracking_confidence=0.6
        )
        self.mp_drawing = mp.solutions.drawing_utils


        self.capture = None
        self.is_capturing = False
        self.show_cam = True
        self.frames = []
        self.capture = cv2.VideoCapture(0)  # Open the camera
        print('cam on')

        self.frame_buffer = []
        self.gesture_detected = False
        self.min_gesture_frames = 20  # Minimum number of frames to consider as a gesture

        self.roi = (40, 30, 400, 400)  # Region of Interest (x, y, width, height)

        # Display initial camera feed
        self.update(0)

        Clock.schedule_interval(self.update, 1 / 30.0)  # Schedule video update

        return self.layout

    def start_capture(self, instance):
        self.is_capturing = True
        self.start_button.disabled = True
        self.stop_button.disabled = False
        Clock.schedule_interval(self.update, 1 / 30.0)

    def stop_capture(self, instance):
        self.is_capturing = False
        self.capture.release()  # Release the camera
        self.start_button.disabled = False
        self.stop_button.disabled = True
        Clock.unschedule(self.update)
    
    def dummy(self):
        print('dummy ')
        

    def update(self, dt):
        if self.is_capturing:
            # Initialize Mediapipe hands module
            mp_hands = mp.solutions.hands
            hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.6, min_tracking_confidence=0.5)
            ret, frame = self.capture.read()  # Read a frame from the camera
            if ret:
                # Flip the frame vertically to correct orientation
                frame = cv2.flip(frame, 0)
                
                # Draw borders around ROI
                if self.roi:
                    x, y, w, h = self.roi
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Convert the frame from BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Detect hands in the frame
                results = hands.process(frame_rgb)

                # Check if hands are detected
                if results.multi_hand_landmarks:
                    self.frame_buffer.append(frame)
                    print(len(self.frame_buffer))
                else:
                    if len(self.frame_buffer) >= self.min_gesture_frames:
                        gesture_frames = self.frame_buffer.copy()  # one gesture video
                        print('gesture recognised')
                        print(len(gesture_frames))
                        # RunFrames.run_model_by_frames(gesture_frames)
                        # self.dummy()


                    self.gesture_detected = False
                    self.frame_buffer = []

                # Update the Kivy Image widget
                self.video_frame.texture = self.convert_to_kivy_texture(frame_rgb)


        elif self.show_cam:
            ret, frame = self.capture.read()  # Read a frame from the camera
            if ret:
                # Flip the frame vertically to correct orientation
                frame = cv2.flip(frame, 0)
                
                # Draw borders around ROI
                if self.roi:
                    x, y, w, h = self.roi
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Convert the frame from BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Update the Kivy Image widget
                self.video_frame.texture = self.convert_to_kivy_texture(frame_rgb)
    

    def convert_to_kivy_texture(self, cv2_frame):
        texture = Texture.create(size=(cv2_frame.shape[1], cv2_frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(cv2_frame.tostring(), colorfmt='rgb', bufferfmt='ubyte')
        return texture


if __name__ == '__main__':
    CameraApp().run()
