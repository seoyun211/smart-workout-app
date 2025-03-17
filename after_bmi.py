import platform
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label

# 운영체제에 따라 폰트 경로 설정
def get_korean_font():
    system = platform.system()
    if system == "Windows":
        return "malgun.ttf"  # 윈도우 기본 한글 폰트 (맑은 고딕)
    elif system == "Darwin":  # macOS
        return "/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc"  # macOS 기본 한글 폰트
    else:
        return "NotoSansCJK-Regular.otf"  # 프로젝트 내부 폰트 (리눅스 대비)

KOREAN_FONT = get_korean_font()

# 화면 정의
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # 화면 상단에 텍스트 추가
        label = Label(text=f'새 화면:', font_size='24sp', font_name=KOREAN_FONT)
        layout.add_widget(label)
        
        # 하단에 버튼들 추가
        button_layout = BoxLayout(size_hint_y=None, height=50)
        
        btn1 = Button(text=f'맞춤 운동', font_size='24sp', font_name=KOREAN_FONT)
        btn2 = Button(text=f'건강 추적', font_size='24sp', font_name=KOREAN_FONT)
        btn3 = Button(text=f'MYPAGE', font_size='24sp', font_name=KOREAN_FONT)
        
        button_layout.add_widget(btn1)
        button_layout.add_widget(btn2)
        button_layout.add_widget(btn3)
        
        layout.add_widget(button_layout)
        
        self.add_widget(layout)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    MyApp().run()
