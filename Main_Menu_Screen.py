from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import platform
from healthcare import HealthcareScreen



def get_korean_font():
    system = platform.system()
    if system == "Windows":
        return "C:/Windows/Fonts/malgun.ttf"
    elif system == "Darwin":
        return "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    return "NotoSansCJK-Regular.otf"

KOREAN_FONT = get_korean_font()

class BackgroundWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 1)  # 흰색 배경
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundWidget())
        layout = BoxLayout(orientation='horizontal', spacing=10, padding=20, size_hint=(None, None), size=(400, 100), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        health_button = Button(text="건강 추적", font_name=KOREAN_FONT, size_hint=(0.5, 1))
        health_button.bind(on_press=self.go_to_healthcare)
        
        exercise_button = Button(text="운동 추천", font_name=KOREAN_FONT, size_hint=(0.5, 1))
        exercise_button.bind(on_press=self.go_to_exercise_recommendation)
        
        layout.add_widget(health_button)
        layout.add_widget(exercise_button)
        self.add_widget(layout)
    
    def go_to_healthcare(self, instance):
        self.manager.current = 'healthcare'
    
    def go_to_exercise_recommendation(self, instance):
        self.manager.current = 'gender_selection' 

class HealthcareScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundWidget())
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20, size_hint=(None, None), size=(300, 300), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        next_button = Button(text="다음", font_name=KOREAN_FONT, size_hint=(1, 0.1))
        next_button.bind(on_press=self.go_to_gender_selection)
        
        layout.add_widget(next_button)
        self.add_widget(layout)
    
    def go_to_gender_selection(self, instance):
        self.manager.current = 'gender_selection'

class ExerciseRecommendationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundWidget())
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20, size_hint=(None, None), size=(300, 300), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        back_button = Button(text="뒤로", font_name=KOREAN_FONT, size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        
        layout.add_widget(back_button)
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'

class GenderSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(BackgroundWidget())
        layout = BoxLayout(orientation='horizontal', spacing=10, padding=20, size_hint=(None, None), size=(300, 100), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        male_button = Button(text="남성", font_name=KOREAN_FONT, size_hint=(0.5, 1))
        female_button = Button(text="여성", font_name=KOREAN_FONT, size_hint=(0.5, 1))
        
        layout.add_widget(male_button)
        layout.add_widget(female_button)
        self.add_widget(layout)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(HealthcareScreen(name='healthcare'))
        sm.add_widget(ExerciseRecommendationScreen(name='exercise_recommendation'))
        sm.add_widget(GenderSelectionScreen(name='gender_selection'))
        sm.current = 'main_menu'
        return sm

if __name__ == "__main__":
    MyApp().run()
