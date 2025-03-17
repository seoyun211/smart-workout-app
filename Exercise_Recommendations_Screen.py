from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

class ExerciseRecommendationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 전체 레이아웃 (수직 배치)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # 운동 추천 제목
        self.title_label = Label(text="운동 추천", font_size='24sp', bold=True)
        self.layout.add_widget(self.title_label)

        # BMI 결과별 추천 운동 데이터 (운동 리스트 + 이미지)
        self.exercise_data = {
            "저체중": {
                "운동": "근력 운동 (스쿼트, 푸쉬업, 데드리프트)",
                "이미지": "images/weight_gain.png"  # 저체중 운동 이미지
            },
            "정상체중": {
                "운동": "유산소 + 근력 운동 (러닝, 요가, 필라테스)",
                "이미지": "images/normal.png"  # 정상체중 운동 이미지
            },
            "과체중": {
                "운동": "유산소 중심 운동 (빠르게 걷기, 사이클, 수영)",
                "이미지": "images/overweight.png"  # 과체중 운동 이미지
            },
            "비만": {
                "운동": "고강도 유산소 운동 (HIIT, 인터벌 트레이닝)",
                "이미지": "images/obesity.png"  # 비만 운동 이미지
            }
        }

        # 운동 추천 리스트 (동적으로 업데이트될 부분)
        self.exercise_label = Label(text="", font_size='20sp')
        self.layout.add_widget(self.exercise_label)

        # 운동 방법 이미지 (동적으로 업데이트될 부분)
        self.exercise_image = Image(source="", size_hint=(1, 0.5))
        self.layout.add_widget(self.exercise_image)

        # 뒤로 가기 버튼
        self.back_button = Button(text="뒤로 가기", size_hint=(1, 0.15))
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        # 레이아웃 추가
        self.add_widget(self.layout)

    def set_bmi_category(self, category):
        """ BMI 카테고리에 따라 운동 추천을 업데이트하는 함수 """
        if category in self.exercise_data:
            self.exercise_label.text = f"추천 운동: {self.exercise_data[category]['운동']}"
            self.exercise_image.source = self.exercise_data[category]['이미지']
        else:
            self.exercise_label.text = "운동 추천 데이터를 찾을 수 없습니다."
            self.exercise_image.source = ""

    def go_back(self, instance):
        """ 이전 화면(BMI 화면)으로 돌아가기 """
        self.manager.current = "bmi_screen"
