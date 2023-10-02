from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
import cv2
import os

class VideoCaptureApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.camera = Camera()
        
        self.start_button = Button(text='Start Recording')
        self.start_button.bind(on_press=self.start_recording)
        self.layout.add_widget(self.start_button)
        
        self.stop_button = Button(text='Stop Recording')
        self.stop_button.bind(on_press=self.stop_recording)
        self.layout.add_widget(self.stop_button)

        self.layout.add_widget(self.camera)
        
        self.recording = False
        self.frame_counter = 0
        
        return self.layout
    
    def start_recording(self, instance):
        self.recording = True
        self.frame_counter = 0
        
        if not os.path.exists('frames'):
            os.makedirs('frames')
        
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        print(self.capture.get(cv2.CAP_PROP_FPS))
        
        self.start_button.disabled = True
        self.stop_button.disabled = False
        
        self.record_frames()
    
    def record_frames(self):
        if self.recording:
            ret, frame = self.capture.read()
            if ret:
                self.frame_counter += 1
                frame_filename = os.path.join('frames', f'frame_{self.frame_counter:04d}.jpg')
                cv2.imwrite(frame_filename, frame)
                self.camera.texture = self.texture_from_frame(frame)
                self.layout.after(100, self.record_frames)
    
    def stop_recording(self, instance):
        self.recording = False
        self.capture.release()
        
        self.start_button.disabled = False
        self.stop_button.disabled = True
    
    def texture_from_frame(self, frame):
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(frame.tostring(), colorfmt='rgb', bufferfmt='ubyte')
        return texture
        # buffer = frame.tostring()
        # texture = self.camera.texture
        # texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        # return texture

if __name__ == '__main__':
    VideoCaptureApp().run()
