from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from home_screen import HomeScreen
from employee_dashboard import EmployeeDashboard
from admin_dashboard import AdminDashboard
from about_us import AboutUs

class TrackYourMan(App):
    def build(self):
        self.icon = 'TrackYourMan.png'
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(HomeScreen(name="home_screen"))
        sm.add_widget(EmployeeDashboard(name="employee_dashboard"))
        sm.add_widget(AdminDashboard(name="admin_dashboard"))
        sm.add_widget(AboutUs(name="about_us"))
        sm.current = "home_screen"
        
        return sm

if __name__ == "__main__":
    TrackYourMan().run()
