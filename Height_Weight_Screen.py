import platform
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle  # Color와 Rectangle을 추가합니다.
from kivy.uix.button import Button
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
        # 영어와 한글을 모두 지원하는 버튼 생성
        login_button = Button(
            text="로그인",  # 한글 텍스트
            size_hint=(1, 0.2),
            background_color=(0, 0, 0, 1),
            font_name=KOREAN_FONT  # 시스템에 맞는 한글 폰트 적용
        )
        return login_button

if __name__ == "__main__":
    MyApp().run()


class HeightWeightScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 배경색 설정
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # 연한 회색 배경
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # 레이아웃 설정
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.size_hint = (0.8, 0.7)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # 타이틀 레이블
        title_label = Label(text="키 & 몸무게를 입력하세요", font_size='22sp', font_name=KOREAN_FONT, color=(0, 0, 0, 1), size_hint=(1, 0.15))
        self.layout.add_widget(title_label)

        # 키 입력 필드
        stature_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.14), spacing=15)
        stature_icon = Image(source="images/키.png", size_hint=(0.25, 1))
        self.stature_input = TextInput(hint_text="키(cm)", multiline=False, size_hint=(0.85, 1), font_name=KOREAN_FONT)
        stature_layout.add_widget(stature_icon)
        stature_layout.add_widget(self.stature_input)
        self.layout.add_widget(stature_layout)

        # 몸무게 입력 필드
        weight_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.14), spacing=15)
        weight_icon = Image(source="images/몸무게.png", size_hint=(0.25, 1))
        self.weight_input = TextInput(hint_text="몸무게(kg)", multiline=False, size_hint=(0.85, 1), font_name=KOREAN_FONT)
        weight_layout.add_widget(weight_icon)
        weight_layout.add_widget(self.weight_input)
        self.layout.add_widget(weight_layout)

        # BMI 계산 버튼
        self.calculate_button = Button(text="BMI 계산", size_hint=(1, 0.15), font_name=KOREAN_FONT, background_color=(0.5, 0.5, 0.5, 1))
        self.calculate_button.bind(on_press=self.calculate_bmi)
        self.layout.add_widget(self.calculate_button)

        self.add_widget(self.layout)

    # 배경색이 화면 크기에 맞게 조정되도록 업데이트
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    # BMI 계산 로직
    def calculate_bmi(self, instance):
        try:
            height = float(self.stature_input.text) / 100  # 키를 미터로 변환
            weight = float(self.weight_input.text)
            bmi = weight / (height ** 2)
            bmi_result = f"BMI: {bmi:.2f}"
            self.show_bmi_result_popup(bmi_result)
        except ValueError:
            self.show_error_popup()

    # BMI 결과를 보여주는 팝업
    def show_bmi_result_popup(self, bmi_result):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        result_label = Label(text=bmi_result, font_size='20sp', font_name=KOREAN_FONT)
        close_button = Button(text="확인", size_hint=(1, 0.2), font_name=KOREAN_FONT)
        popup_layout.add_widget(result_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title="BMI 계산 결과", content=popup_layout, size_hint=(0.6, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    # 입력 오류 팝업
    def show_error_popup(self):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        error_label = Label(text="입력 오류! 숫자만 입력하세요.", font_size='20sp', font_name=KOREAN_FONT)
        close_button = Button(text="확인", size_hint=(1, 0.2), font_name=KOREAN_FONT)
        popup_layout.add_widget(error_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title="Error", content=popup_layout, size_hint=(0.6, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

