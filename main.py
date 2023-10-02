from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from screens.home_screen import HomeScreen
from screens.about_screen import AboutScreen
from screens.camera_screen import CameraScreen

    

class MyApp(MDApp):
    def build(self):
        
        sm = MDScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(AboutScreen(name='about'))
        sm.add_widget(CameraScreen(name='camera'))
        # sm.add_widget(LoginScreen(name='login', auth_manager=auth_manager))
        # sm.add_widget(RegistrationScreen(name='register', auth_manager=auth_manager))
        return sm


if __name__ == '__main__':
    MyApp().run()
