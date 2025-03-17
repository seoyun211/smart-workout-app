import platform
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App


def get_korean_font():
    system = platform.system()
    if system == "Windows":
        return "C:/Windows/Fonts/malgun.ttf"  # Windows에서 기본 한글 폰트 (맑은 고딕)
    elif system == "Darwin":  # macOS
        return "/System/Library/Fonts/AppleSDGothicNeo.ttc"  # macOS 기본 한글 폰트
    return "NotoSansCJK-Regular.otf"  # 리눅스나 기타에서 사용할 폰트


KOREAN_FONT = get_korean_font()

class MyApp(App):
    def build(self):
        login_button = Button(
            text="로그인",
            size_hint=(1, 0.2),
            background_color=(0, 0, 0, 1),
            font_name=KOREAN_FONT  # 운영체제에 맞는 폰트 적용
        )
        return login_button

if __name__ == "__main__":
    MyApp().run()




class BMIScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = 0
        self.weight = 0

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # BMI 결과 레이블
        bmi_label = Label(text=f'당신의 BMI: {self.calculate_bmi():.2f}', font_size='24sp', font_name="KoreanFont")
        result_label = Label(text=f'분류: {self.get_bmi_category()}', font_size='28sp', bold=True, font_name="KoreanFont")
        
        # 뒤로 가기 버튼
        back_button = Button(text='뒤로 가기', on_press=self.go_back, font_name="KoreanFont")
        
        self.layout.add_widget(bmi_label)
        self.layout.add_widget(result_label)
        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)

    def calculate_bmi(self):
        return self.weight / (self.height / 100) ** 2
    
    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return '저체중'
        elif 18.5 <= bmi < 25:
            return '정상체중'
        else:
            return '과체중'
    
    def go_back(self, instance):
        self.manager.current = 'height_weight_screen'
