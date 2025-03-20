from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
import platform

def get_korean_font():
    system = platform.system()
    if system == "Windows":
        return "C:/Windows/Fonts/malgun.ttf"
    elif system == "Darwin":
        return "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    return "NotoSansCJK-Regular.otf"

KOREAN_FONT = get_korean_font()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        login_button = Button(text="로그인", font_name=KOREAN_FONT, size_hint=(1, 0.2))
        login_button.bind(on_press=self.on_login)
        layout.add_widget(login_button)
        self.add_widget(layout)

    def on_login(self, instance):
        self.manager.current = 'main_menu'

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        
        health_button = Button(text="건강 추적", font_name=KOREAN_FONT, size_hint=(1, 0.3))
        health_button.bind(on_press=self.go_to_gender_selection)
        
        exercise_button = Button(text="운동 추천", font_name=KOREAN_FONT, size_hint=(1, 0.3))
        exercise_button.bind(on_press=self.go_to_gender_selection)
        
        layout.add_widget(health_button)
        layout.add_widget(exercise_button)
        self.add_widget(layout)
    
    def go_to_gender_selection(self, instance):
        self.manager.current = 'gender_selection'

class GenderSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        male_button = Button(text="남성", font_name=KOREAN_FONT, size_hint=(1, 0.2))
        female_button = Button(text="여성", font_name=KOREAN_FONT, size_hint=(1, 0.2))
        
        layout.add_widget(male_button)
        layout.add_widget(female_button)
        self.add_widget(layout)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(GenderSelectionScreen(name='gender_selection'))
        return sm

if __name__ == "__main__":
    MyApp().run()
