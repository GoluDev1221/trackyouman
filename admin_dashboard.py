import pandas as pd
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import matplotlib.pyplot as plt
import os

class AdminDashboard(Screen):
    def __init__(self, **kwargs):
        super(AdminDashboard, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        logo = Image(source='admin_dashboard.png', size_hint=(1, 0.2))
        layout.add_widget(logo)

        title_label = Button(
            text="Welcome to Admin Dashboard", 
            size_hint=(1, 0.1), 
            background_normal='', 
            background_color=(0.9, 0.3, 0.5, 1), 
            font_size=24
        )
        layout.add_widget(title_label)

        check_attendance_button = Button(
            text="Check Attendance", 
            size_hint=(0.5, 0.1), 
            pos_hint={"center_x": 0.5}, 
            background_normal='', 
            background_color=(0.7, 0.4, 0.6, 1) 
        )
        check_attendance_button.bind(on_release=self.check_attendance)
        layout.add_widget(check_attendance_button)

        clear_data_button = Button(
            text="Clear Attendance Data",
            size_hint=(0.5, 0.1),
            pos_hint={"center_x": 0.5},
            background_normal='',
            background_color=(0.8, 0.2, 0.4, 1)
        )
        clear_data_button.bind(on_release=self.confirm_clear_data)
        layout.add_widget(clear_data_button)

        logout_button = Button(
            text="Logout", 
            size_hint=(0.5, 0.1), 
            pos_hint={"center_x": 0.5},
            background_normal='', 
            background_color=(0.8, 0.1, 0.3, 1)
        )
        logout_button.bind(on_release=self.logout)
        layout.add_widget(logout_button)

        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height * 0.5)) 
        layout.add_widget(self.scroll_view)

        self.add_widget(layout)

    def check_attendance(self, instance):
        attendance_data = self.get_attendance_data()
        if attendance_data:
            self.create_pie_chart(attendance_data)
        else:
            self.show_no_data_popup()

    def create_pie_chart(self, attendance_data):
        total_entries = sum(attendance_data.values())
        labels = []
        sizes = []

        for username, present_days in attendance_data.items():
            attendance_percentage = (present_days / total_entries) * 100
            labels.append(f"{username} ({attendance_percentage:.1f}%)")
            sizes.append(attendance_percentage)

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        plt.savefig('attendance_pie_chart.png', format='png')
        plt.close(fig)

        for widget in self.scroll_view.children:
            if isinstance(widget, Image):
                self.scroll_view.remove_widget(widget)

        pie_chart_image = Image(source='attendance_pie_chart.png', size_hint=(1, 1))
        self.scroll_view.add_widget(pie_chart_image)

    def get_attendance_data(self):
        try:
            df = pd.read_csv('attendance_log.csv', header=None, names=['username', 'timestamp'])

            attendance_data = df.groupby('username').size()

            attendance_data = attendance_data.to_dict()

        except FileNotFoundError:
            print("Attendance log file not found.")
            return {}

        return attendance_data

    def confirm_clear_data(self, instance):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="Are you sure you want to clear all attendance data?"))
        
        confirm_button = Button(text="Yes", size_hint=(0.5, 0.2))
        confirm_button.bind(on_release=self.clear_attendance_data)
        content.add_widget(confirm_button)

        cancel_button = Button(text="Cancel", size_hint=(0.5, 0.2))
        cancel_button.bind(on_release=self.close_popup)
        content.add_widget(cancel_button)

        self.popup = Popup(title="Confirm Clear Data", content=content, size_hint=(0.6, 0.4))
        self.popup.open()

    def clear_attendance_data(self, instance):
        with open('attendance_log.csv', 'w') as f:
            f.truncate()
        print("Attendance data cleared.")

        self.close_popup(instance)

    def show_no_data_popup(self):
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text="No attendance data available for the selected period."))
        
        close_button = Button(text="Close", size_hint=(0.5, 0.2))
        content.add_widget(close_button)
        close_button.bind(on_release=self.close_popup)

        self.popup = Popup(title="No Data", content=content, size_hint=(0.5, 0.3))
        self.popup.open()

    def close_popup(self, instance):
        if hasattr(self, 'popup'):
            self.popup.dismiss()

    def logout(self, instance):
        self.manager.current = 'home_screen' 
