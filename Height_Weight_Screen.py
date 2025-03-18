import platform
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle

def get_korean_font():
    system = platform.system()
    if system == "Windows":
        return "C:/Windows/Fonts/malgun.ttf"
    elif system == "Darwin":
        return "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    return "NotoSansCJK-Regular.otf"

KOREAN_FONT = get_korean_font()

class HeightWeightScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.size_hint = (0.8, 0.7)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        title_label = Label(text="키 & 몸무게를 입력하세요", font_size='22sp', font_name=KOREAN_FONT, color=(0, 0, 0, 1), size_hint=(1, 0.15))
        self.layout.add_widget(title_label)

        stature_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.14), spacing=15)
        stature_icon = Image(source="images/키.png", size_hint=(0.25, 1))
        self.stature_input = TextInput(hint_text="키(cm)", multiline=False, size_hint=(0.85, 1), font_name=KOREAN_FONT)
        stature_layout.add_widget(stature_icon)
        stature_layout.add_widget(self.stature_input)
        self.layout.add_widget(stature_layout)

        weight_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.14), spacing=15)
        weight_icon = Image(source="images/몸무게.png", size_hint=(0.25, 1))
        self.weight_input = TextInput(hint_text="몸무게(kg)", multiline=False, size_hint=(0.85, 1), font_name=KOREAN_FONT)
        weight_layout.add_widget(weight_icon)
        weight_layout.add_widget(self.weight_input)
        self.layout.add_widget(weight_layout)

        self.calculate_button = Button(text="BMI 계산", size_hint=(1, 0.15), font_name=KOREAN_FONT, background_color=(0.5, 0.5, 0.5, 1))
        self.calculate_button.bind(on_press=self.calculate_bmi)
        self.layout.add_widget(self.calculate_button)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def calculate_bmi(self, instance):
        try:
            height = float(self.stature_input.text) / 100
            weight = float(self.weight_input.text)
            bmi = weight / (height ** 2)
            category = self.get_bmi_category(bmi)

            # 🚀 운동 추천 화면으로 이동 + BMI 카테고리 전달
            exercise_screen = self.manager.get_screen("exercise_recommendation")
            exercise_screen.set_bmi_category(category)
            self.manager.current = "exercise_recommendation"

        except ValueError:
            self.show_error_popup()

    def get_bmi_category(self, bmi):
        if bmi < 18.5:
            return "저체중"
        elif 18.5 <= bmi < 25:
            return "정상체중"
        elif 25 <= bmi < 30:
            return "과체중"
        else:
            return "비만"

    def show_error_popup(self):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        error_label = Label(text="입력 오류! 숫자만 입력하세요.", font_size='20sp', font_name=KOREAN_FONT)
        close_button = Button(text="확인", size_hint=(1, 0.2), font_name=KOREAN_FONT)
        popup_layout.add_widget(error_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title="Error", content=popup_layout, size_hint=(0.6, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()


