from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
import joblib

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = MDBoxLayout(orientation='vertical', spacing='10dp')

        # Create a label for the title
        title_label = MDLabel(
            text="Words Available for Translation",
            font_size=24,
            size_hint=(1, None),
            height='60dp',
            theme_text_color="Primary",
            halign="center",
        )

        
        # list of words (labels)
        label_encoder = joblib.load('label_encoder.joblib')
        word_list =  label_encoder.classes_  # ['Accident', 'Come', 'Doctor', 'Help', 'Hot', 'Lose', 'Pain', 'Thief']
        word_scrollview = MDScrollView(size_hint=(1, 1))
        word_layout = MDGridLayout(cols=1, spacing='10dp', size_hint=(1, None), adaptive_width= True, size_hint_x=1)
        
        for word in word_list:
            word_label = MDLabel(
                text=word,
                font_size=18,
                size_hint=(1, None),
                height='40dp',
                theme_text_color="Secondary",
                padding=('10dp', '5dp'),
                halign="center",
                size_hint_x=1,
            )
            word_layout.add_widget(word_label)
        
        word_scrollview.add_widget(word_layout)
        
        # Adding buttons to the bottom footer
        footer = MDBoxLayout(orientation='horizontal', size_hint=(1, None), height='50dp')
        words_button = MDIconButton(icon='w.png', 
                                    disabled=True,
                        )
        camera_button = MDIconButton(icon='camera',
                                     pos_hint={"center_x": 0.5, "center_y": 0.5},
                                     theme_text_color="Custom",
                                     icon_color= 'orange',
                        )
        profile_button = MDIconButton(icon='profile.png', theme_text_color="Custom",
                                    # background_color=[0.8, 0.2, 0.3, 1], # no attribute
                        )

        words_button.size_hint_x = 1  
        camera_button.size_hint_x = 1  
        profile_button.size_hint_x = 1  
        
        footer.add_widget(words_button)
        footer.add_widget(camera_button)
        footer.add_widget(profile_button)
        
         # Add widgets to the main layout
        main_layout.add_widget(title_label)
        main_layout.add_widget(word_scrollview)
        main_layout.add_widget(footer)

        # Event handler for the Profile button
        profile_button.bind(on_release=self.show_about_screen)
        camera_button.bind(on_release=self.camera_screen)

        self.add_widget(main_layout)
    
    def show_about_screen(self, instance):
        self.manager.current = 'about'  # Switch to the About screen
    
    def camera_screen(self, instance):
        self.manager.current = 'camera'
