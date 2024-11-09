from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image

class AboutUs(Screen):
    def __init__(self, **kwargs):
        super(AboutUs, self).__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        about_us_image = Image(source='about_us.png', size_hint=(1, 0.5))
        layout.add_widget(about_us_image)

        credit_image = Image(source='Credits.png', size_hint=(1, 0.5))
        layout.add_widget(credit_image)

        back_button = Button(text="Back to Home", size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5}, background_normal='', background_color=(0.2, 0.4, 0.8, 1), font_size=24)
        back_button.bind(on_release=self.go_to_home)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def go_to_home(self, instance):
        self.manager.current = "home_screen"
