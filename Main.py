from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Login_Screen import LoginScreen
from Gender_Screen import GenderSelectionScreen
from Height_Weight_Screen import HeightWeightScreen
from SignUp_Screen import SignUpScreen

class HealthTrackerApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.login_screen = LoginScreen(name='login_screen')
        self.gender_selection_screen = GenderSelectionScreen(name='gender_selection')
        self.height_weight_screen = HeightWeightScreen(name='height_weight_screen')
        self.sign_up_screen = SignUpScreen(name='sign_up_screen')

        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.gender_selection_screen)
        self.screen_manager.add_widget(self.height_weight_screen)
        self.screen_manager.add_widget(self.sign_up_screen)


        return self.screen_manager

if __name__ == '__main__':
    HealthTrackerApp().run()
