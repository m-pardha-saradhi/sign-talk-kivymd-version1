import cv2
import RunVideo1
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivy.uix.image import Image
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.graphics.texture import Texture
from kivy.clock import Clock


class CameraScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical')

        # Create a frame for displaying video with a gap from buttons
        self.video_frame = Image(size_hint=(1, 0.8), allow_stretch=True)
        layout.add_widget(self.video_frame)

        # Create a horizontal layout for the buttons at the bottom
        button_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, None), height='60dp', size_hint_x=1)

        # Create start and stop buttons, and a back button
        self.start_button = MDRaisedButton(text='Start')
        self.stop_button = MDRaisedButton(text='Stop', disabled=True)
        self.back_button = MDRaisedButton(text='Back')

        self.start_button.size_hint_x = 1
        self.stop_button.size_hint_x = 1
        self.back_button.size_hint_x = 1

        self.start_button.bind(on_release=self.start_capture)
        self.stop_button.bind(on_release=self.stop_capture)
        self.back_button.bind(on_release=self.show_home_screen)

        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.stop_button)
        button_layout.add_widget(self.back_button)

        layout.add_widget(button_layout)

        self.add_widget(layout)

        self.result_label = None
        self.is_capturing = False
        self.show_cam = True
        self.frames = []
        self.capture = cv2.VideoCapture(0)  # open the camera

        self.roi = (40, 30, 560, 400)  # Region of Interest (x, y, width, height)

        # Display initial camera feed
        self.update(0)

        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Schedule video update

    def show_home_screen(self, instance):
        self.manager.current = 'home'

    def start_capture(self, instance):
        self.capture = cv2.VideoCapture(0)
        self.is_capturing = True
        self.start_button.disabled = True
        self.stop_button.disabled = False
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def stop_capture(self, instance):
        self.is_capturing = False
        # self.capture.release()  # Release the camera
        self.start_button.disabled = False
        self.stop_button.disabled = True
        Clock.unschedule(self.update)   # Unscheduling will not update the imshow on screen

        # Save the captured frames as a video file
        if self.frames:
            self.save_video(self.frames)
        self.frames = []
        self.capture.release()
        words_str = ''
        words = RunVideo1.runModel()   # returns a list of words
        for word in words:
            words_str = word + ' '

        if self.result_label:
            self.remove_widget(self.result_label)
            self.result_label = MDLabel(text=words_str, pos_hint={'center_x':0.5,
                                                'center_y':0.2}, theme_text_color="Secondary", font_size='30sp')
            self.add_widget(self.result_label)
        else:
            self.result_label = MDLabel(text=words_str, pos_hint={'center_x':0.5,
                                                'center_y':0.2}, theme_text_color="Secondary", font_size='30sp')
            self.add_widget(self.result_label)

    def update(self, dt):
        if self.is_capturing:
            ret, frame = self.capture.read()  # Read a frame from the camera
            self.capture.set(cv2.CAP_PROP_FPS, 30.0)
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

                # Store the frame for saving as a video (in ROI only)
                if self.roi:
                    self.frames.append(frame_rgb[y:y+h, x:x+w])

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
    
    def save_video(self, frames):
        out = cv2.VideoWriter('captured_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 30, frames[0].shape[:2][::-1])

        for frame in frames:
            # Flip the frame vertically to correct orientation
            frame = cv2.flip(frame, 0)

            # Convert frame from BGR to RGB before saving
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Remove the green border (ROI) from the frame
            if self.roi:
                x, y, w, h = self.roi
                green_border_size = 0
                roi_frame = rgb_frame[y:y+h-green_border_size, x:x+w-green_border_size]  # Extract ROI region

                # Resize ROI frame to match the dimensions of the saved frames
                target_size = (frames[0].shape[1], frames[0].shape[0])
                roi_frame_resized = cv2.resize(roi_frame, target_size, interpolation=cv2.INTER_LINEAR)

                out.write(roi_frame_resized)
            else:
                out.write(rgb_frame)  # Save the entire frame

        out.release()
