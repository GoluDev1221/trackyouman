from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime
import os
import csv

class EmployeeDashboard(Screen):
    def __init__(self, **kwargs):
        super(EmployeeDashboard, self).__init__(**kwargs)
        self.username = None 

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        logo = Image(source='employee_dashboard.png', size_hint=(1, 0.5))
        layout.add_widget(logo)

        title_label = Button(
            text="Welcome to Employee Dashboard", 
            size_hint=(1, 0.1), 
            background_normal='', 
            background_color=(0.1, 0.3, 0.6, 1)
        )
        layout.add_widget(title_label)

        log_attendance_button = Button(
            text="Log Attendance", 
            size_hint=(0.5, 0.2), 
            pos_hint={"center_x": 0.5}, 
            background_normal='', 
            background_color=(0.3, 0.5, 0.8, 1)
        )
        log_attendance_button.bind(on_release=self.log_attendance)
        layout.add_widget(log_attendance_button)

        logout_button = Button(
            text="Logout", 
            size_hint=(0.5, 0.2), 
            pos_hint={"center_x": 0.5}, 
            background_normal='', 
            background_color=(0.2, 0.4, 0.7, 1)
        )
        logout_button.bind(on_release=self.logout)
        layout.add_widget(logout_button)

        self.add_widget(layout)

    def set_username(self, username):
        self.username = username

    def has_logged_today(self, username):
        today = datetime.now().strftime("%Y-%m-%d")
        if os.path.exists('attendance_log.csv'):
            with open('attendance_log.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == username and row[1].split(' ')[0] == today:
                        return True
        return False

    def log_attendance(self, instance):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.has_logged_today(self.username):
            self.show_popup("Error", "You have already logged attendance today.")
            return
        with open("attendance_log.csv", mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.username, current_time])
        self.show_popup("Attendance Logged", f"Attendance logged at {current_time}.")
        print(f"Attendance logged for {self.username} at {current_time}")

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message, color=(0.1, 0.3, 0.5, 1)))
        close_button = Button(
            text="Close", 
            size_hint=(1, 0.2), 
            background_normal='', 
            background_color=(0.3, 0.5, 0.8, 1)
        )
        content.add_widget(close_button)
        popup = Popup(
            title=title, 
            content=content, 
            size_hint=(0.5, 0.3),
            title_color=(0.1, 0.3, 0.6, 1)
        )
        close_button.bind(on_release=popup.dismiss)
        popup.open()

    def logout(self, instance):
        self.manager.current = "home_screen"
