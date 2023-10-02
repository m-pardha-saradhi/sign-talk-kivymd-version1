import cv2
import RunVideo1
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.clock import Clock
# from jnius import autoclass, cast

# Import the OpenCV Java class
# JavaCameraView = autoclass('org.opencv.android.JavaCameraView')

class CameraScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        
        # Create a frame for displaying video
        self.video_frame = Image(size_hint=(1, 0.8))
        layout.add_widget(self.video_frame)

        # Create start and stop buttons
        self.start_button = Button(text='Start', size_hint=(0.2, 0.1))
        self.stop_button = Button(text='Stop', disabled=True, size_hint=(0.2, 0.1))
        self.cancel_button = Button(text='cancel', size_hint=(0.2, 0.1))
        self.start_button.bind(on_press=self.start_capture)
        self.stop_button.bind(on_press=self.stop_capture)
        self.cancel_button.bind(on_press=self.show_home_screen)
        layout.add_widget(self.start_button)
        layout.add_widget(self.stop_button)

        self.add_widget(layout)


        self.is_capturing = False
        self.show_cam = True
        self.frames = []
        self.capture = None  # Open the camera
        print('cam on')

        self.roi = (40, 30, 560, 400)  # Region of Interest (x, y, width, height)

        # Display initial camera feed
        self.update(0)

        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Schedule video update

        # Event handler for the Profile button
        # self.stop_button.bind(on_release=self.show_about_screen)

        # return self.layout

    def show_about_screen(self, instance):
        self.manager.current = 'about'  
    
    def show_home_screen(self, instance):
        self.manager.current = 'home'  
    

    def start_capture(self, instance):
        self.capture = cv2.VideoCapture(0)
        # self.capture = JavaCameraView(cast('android.content.Context', App.get_running_app().activity), 0)
        # self.capture.enableView()
        self.is_capturing = True
        self.start_button.disabled = True
        self.stop_button.disabled = False
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def stop_capture(self, instance):
        self.is_capturing = False
        self.capture.release()  # Release the camera
        self.start_button.disabled = False
        self.stop_button.disabled = True
        Clock.unschedule(self.update)   # Unscheduling will not update the imshow on screen

        # Save the captured frames as a video file
        if self.frames:
            self.save_video(self.frames)
        self.frames = []
	
        # Release the camera
        # if self.capture:
        #     self.capture.disableView()

        words_str = ''
        words = RunVideo1.runModel()   # returns a list of words
        for word in words:
            words_str = word + ' '
        lbl = Label(text=words_str, pos_hint={'center_x':0.4,
                                                'center_y':0.3}, color=(0.5, 0, 0.5, 1))
        self.add_widget(lbl)



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