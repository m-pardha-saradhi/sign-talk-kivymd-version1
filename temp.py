from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton


class MainApp(MDApp):
    def build(self):
        button = MDIconButton(
            icon="camera",
            text="Take photo",
            theme_text_color="Custom",
            text_color=(1, 0, 0, 1),
            size_hint=(0.2, 0.2),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        return button

if __name__ == "__main__":
    MainApp().run()
