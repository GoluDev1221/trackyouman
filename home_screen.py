from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import csv

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        logo = Image(source='TrackYourMan.png', size_hint=(1, 0.4))
        layout.add_widget(logo)

        scroll_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        scroll_layout.bind(minimum_height=scroll_layout.setter('height'))

        self.username_input = TextInput(hint_text="Enter Username", multiline=False, size_hint=(0.8, 0.1), pos_hint={"center_x": 0.5}, font_size=18)
        self.username_input.background_color = (1, 1, 1, 0.8)
        self.username_input.foreground_color = (0, 0, 0, 1)
        self.username_input.height = 40
        scroll_layout.add_widget(self.username_input)

        self.password_input = TextInput(password=True, hint_text="Enter Password", multiline=False, size_hint=(0.8, 0.1), pos_hint={"center_x": 0.5}, font_size=18)
        self.password_input.background_color = (1, 1, 1, 0.8)
        self.password_input.foreground_color = (0, 0, 0, 1)
        self.password_input.height = 40
        scroll_layout.add_widget(self.password_input)

        layout.add_widget(scroll_layout)

        login_button = Button(text="Login", size_hint=(0.8, 0.2), pos_hint={"center_x": 0.5}, background_normal='', background_color=(0.2, 0.4, 0.8, 1), font_size=24)
        login_button.bind(on_release=self.verify_login)
        layout.add_widget(login_button)

        about_button = Button(text="About Us", size_hint=(0.8, 0.2), pos_hint={"center_x": 0.5}, background_normal='', background_color=(0.2, 0.4, 0.8, 1), font_size=24)
        about_button.bind(on_release=self.go_to_about)
        layout.add_widget(about_button)

        self.add_widget(layout)

    def verify_login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if not username or not password:
            self.show_error_popup("Error", "Please fill in both username and password.")
            return

        if username == "admin" and password == "TheRealAdmin":
            self.manager.current = "admin_dashboard"
        else:
            if self.verify_employee_login(username, password):
                employee_dashboard = self.manager.get_screen('employee_dashboard')
                employee_dashboard.set_username(username)
                self.manager.current = "employee_dashboard"
            else:
                self.show_error_popup("Login Error", "Invalid username or password. Please try again.")

    def verify_employee_login(self, username, password):
        try:
            with open('employee_details.csv', 'r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) < 3:
                        continue

                    emp_username = row[1]
                    emp_password = row[2]

                    if username == emp_username and password == emp_password:
                        return True
        except FileNotFoundError:
            self.show_error_popup("File Error", "Employee details file not found.")
            return False
        return False 

    def show_error_popup(self, title, message):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_content.add_widget(Label(text=message))

        close_button = Button(text="Close", size_hint=(1, 0.2), background_color=(0.2, 0.4, 0.8, 1))
        close_button.bind(on_release=self.close_popup)
        popup_content.add_widget(close_button)

        self.error_popup = Popup(title=title,
                                  content=popup_content,
                                  size_hint=(0.5, 0.5),
                                  background_color=(0.2, 0.4, 0.8, 1))
        self.error_popup.open()

    def close_popup(self, instance):
        self.error_popup.dismiss()

    def go_to_about(self, instance):
        self.manager.current = "about_us"
