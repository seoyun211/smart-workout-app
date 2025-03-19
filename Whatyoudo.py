import platform
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase

def get_korean_font():
    system = platform.system()
    if system == "Windows":
        return "C:/Windows/Fonts/malgun.ttf"  # Windows에서 기본 한글 폰트 (맑은 고딕)
    elif system == "Darwin":  # macOS
        return "/System/Library/Fonts/AppleSDGothicNeo.ttc"  # macOS 기본 한글 폰트
    return "NotoSansCJK-Regular.otf"  # 리눅스나 기타에서 사용할 폰트

KOREAN_FONT = get_korean_font()
LabelBase.register(name="Korean", fn_regular=KOREAN_FONT)

class SelectWhatYouDo(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        btn_exercise = Button(text='운동 추천', font_name="Korean", size_hint=(1, 0.2))
        btn_exercise.bind(on_press=self.go_to_gender_selection)

        btn_health = Button(text='건강 추적', font_name="Korean", size_hint=(1, 0.2))
        btn_health.bind(on_press=self.go_to_first_screen)

        layout.add_widget(btn_exercise)
        layout.add_widget(btn_health)
        self.add_widget(layout)

    def go_to_gender_selection(self, instance):
        self.manager.current = 'gender_selection'

    def go_to_first_screen(self, instance):
        self.manager.current = 'first_screen'

class GenderSelection(Screen):
    pass

class FirstScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SelectWhatYouDo(name='selectwhatyoudo'))
        sm.add_widget(GenderSelection(name='gender_selection'))
        sm.add_widget(FirstScreen(name='first_screen'))
        return sm

if __name__ == '__main__':
    MyApp().run()
