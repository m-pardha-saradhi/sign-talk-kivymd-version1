from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout

import webview 

# Google OAuth Configuration
CLIENT_ID = "912530491605-jh5beg1pjlv2hbbqlml8a52da6up3lke.apps.googleusercontent.com"
REDIRECT_URI = "https://www.google.com/"
AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        self.add_widget(Label(text="Username"))
        self.username = TextInput()
        self.add_widget(self.username)

        self.add_widget(Label(text="Password"))
        self.password = TextInput(password=True)
        self.add_widget(self.password)

        self.login_button = Button(text="Login with Google")
        self.login_button.bind(on_press=self.login_with_google)
        self.add_widget(self.login_button)

    def login_with_google(self, instance):
        auth_url = (
            f"{AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=email"
        )

        # Open a webview to handle the OAuth flow
        try:
            webview.create_window("Google OAuth Login", REDIRECT_URI)
            print('login pressed')
        except:
            print('exception ')

class RegisterScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Implement the registration screen UI here

class MyApp(App):
    def build(self):
        self.login_screen = LoginScreen()
        self.register_screen = RegisterScreen()
        return self.login_screen

if __name__ == "__main__":
    MyApp().run()
