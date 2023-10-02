from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.button import MDFloatingActionButtonSpeedDial


class AboutScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', spacing='10dp')
        loggedin = True
        email = 'pardhu@gmail.com'
        name = 'pardhu'

        if loggedin:
            user_label = MDLabel(text=f"Email: {email}\n"
                                       f"Name: {name}",
                                    font_size=20,
                                    size_hint=(1, None),
                                    height='20dp',
                                    theme_text_color="Primary",
                                    halign="center",
                                )
            layout.add_widget(user_label)
            settings_button = MDFloatingActionButtonSpeedDial(icon='w.png',
                                                            id="speed_dial",
                                                            hint_animation=True,
                                                            root_button_anim=True,
                                                            pos_hint={"center_x": 0.5, "center_y": 0.5},
                                                            size_hint=(1, None),
                                                            size_hint_x=1,
                                                        )
            layout.add_widget(settings_button)
        else:
            login_button = MDRaisedButton(text='Login')
            register_button = MDRaisedButton(text='Register')

            login_button.bind(on_release=self.show_login_screen)
            register_button.bind(on_release=self.show_registration_screen)

            layout.add_widget(login_button)
            layout.add_widget(register_button)

        self.add_widget(layout)

        # Adding buttons to the bottom footer
        footer = MDBoxLayout(orientation='horizontal', size_hint=(1, None), height='50dp', size_hint_x=1)
        words_button = MDIconButton(icon='w.png', 
                                    
                        )
        camera_button = MDIconButton(icon='camera',
                                     pos_hint={"center_x": 0.5, "center_y": 0.5},
                                     theme_text_color="Custom",
                                     icon_color= 'orange',
                        )
        profile_button = MDIconButton(icon='profile.png', theme_text_color="Custom",
                                      disabled=True,
                        )

        words_button.size_hint_x=1
        camera_button.size_hint_x = 1
        profile_button.size_hint_x = 1

        footer.add_widget(words_button)
        footer.add_widget(camera_button)
        footer.add_widget(profile_button)

        self.add_widget(footer)

        # Event handler for the buttons
        words_button.bind(on_release=self.show_words_screen)
        camera_button.bind(on_release=self.show_camera_screen)

    def show_login_screen(self, instance):
        self.manager.current = 'login'

    def show_registration_screen(self, instance):
        self.manager.current = 'register'

    def show_words_screen(self, instance):
        self.manager.current = 'home'

    def show_camera_screen(self, instance):
        self.manager.current = 'camera'
