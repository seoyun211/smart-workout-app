from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from Login_Screen import LoginScreen
from Gender_Screen import GenderSelectionScreen
from Height_Weight_Screen import HeightWeightScreen
from SignUp_Screen import SignUpScreen
from BMI_Screen import BMIScreen
from Exercise_Recommendation_Screen import ExerciseRecommendationScreen 

class HealthTrackerApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.login_screen = LoginScreen(name='login_screen')
        self.gender_selection_screen = GenderSelectionScreen(name='gender_selection')
        self.height_weight_screen = HeightWeightScreen(name='height_weight_screen')
        self.sign_up_screen = SignUpScreen(name='sign_up_screen')
        self.exercise_recommendation_screen = ExerciseRecommendationScreen(name='exercise_recommendation')  # 🚀 추가

        self.screen_manager.add_widget(self.login_screen)
        self.screen_manager.add_widget(self.gender_selection_screen)
        self.screen_manager.add_widget(self.height_weight_screen)
        self.screen_manager.add_widget(self.sign_up_screen)
        self.screen_manager.add_widget(self.exercise_recommendation_screen)  # 🚀 추가

        return self.screen_manager

if __name__ == '__main__':
    HealthTrackerApp().run()    