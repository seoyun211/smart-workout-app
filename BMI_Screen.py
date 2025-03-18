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

        self.bmi_label = Label(text=f'당신의 BMI: {self.calculate_bmi():.2f}', font_size='24sp')
        self.result_label = Label(text=f'분류: {self.get_bmi_category()}', font_size='28sp', bold=True)
        self.layout.add_widget(self.bmi_label)
        self.layout.add_widget(self.result_label)

         # 운동 추천 화면으로 이동하는 버튼 ✅
        self.exercise_button = Button(text="운동 추천 보기", size_hint=(1, 0.15))
        self.exercise_button.bind(on_press=self.go_to_exercise_recommendation)
        self.layout.add_widget(self.exercise_button)

        # 뒤로 가기 버튼
        self.back_button = Button(text="뒤로 가기", size_hint=(1, 0.15))
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)
        
        # BMI 결과 레이블
        bmi_label = Label(text=f'당신의 BMI: {self.calculate_bmi():.2f}', font_size='24sp', font_name=KOREAN_FONT)
        result_label = Label(text=f'분류: {self.get_bmi_category()}', font_size='28sp', bold=True, font_name=KOREAN_FONT)
        
        # 뒤로 가기 버튼
        back_button = Button(text='뒤로 가기', on_press=self.go_back, font_name=KOREAN_FONT)
        
        self.layout.add_widget(bmi_label)
        self.layout.add_widget(result_label)
        self.layout.add_widget(back_button)
        self.add_widget(self.layout)

    def set_user_data(self, height, weight):
        """ 사용자의 키와 몸무게 값을 설정하고 BMI 정보를 업데이트 """
        self.height = height
        self.weight = weight
        self.update_bmi_info()

    def update_bmi_info(self):
        """ BMI 값과 분류를 업데이트 """
        if self.height > 0 and self.weight > 0:
            bmi_value = self.calculate_bmi()
            self.bmi_label.text = f'당신의 BMI: {bmi_value:.2f}'
            category = self.get_bmi_category()
            self.result_label.text = f'분류: {self.get_bmi_category()}'

            # BMI 카테고리를 ExerciseRecommendationScreen에 전달 ✅
            exercise_screen = self.manager.get_screen("exercise_screen")
            exercise_screen.set_bmi_category(category)
        else:
            self.bmi_label.text = "입력된 값이 올바르지 않습니다."
            self.result_label.text = ""

    def calculate_bmi(self):
        try:
            return round(self.weight / ((self.height / 100) ** 2), 2) if self.height > 0 else 0
        except ZeroDivisionError:
            return 0

    
    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return '저체중'
        elif 18.5 <= bmi < 25:
            return '정상체중'
        elif 25<= bmi < 30:
            return '과체중'
        else:
            return '비만'

    def go_to_exercise_recommendation(self, instance):
        """ 운동 추천 화면으로 이동하는 함수 ✅ """
        if self.manager:
            self.manager.current = "exercise_screen"

    def go_back(self, instance):
        if self.manager and self.manager.has_screen("height_weight_screen"):
            self.manager.current = "height_weight_screen"
        else:
            print("오류: 'height_weight_screen'이 존재하지 않습니다.")
