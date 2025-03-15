from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

class ExerciseRecommendationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 전체 레이아웃 (수직 배치)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # 제목 라벨
        self.title_label = Label(text="🏋️ 운동 추천", font_size='26sp', bold=True, color=(0, 0, 0, 1))
        self.layout.add_widget(self.title_label)

        # BMI 결과별 추천 운동 데이터 (운동 리스트 + 이미지)
        self.exercise_data = {
            "저체중": {
                "운동": "🏋️ 근력 운동 추천:\n- 스쿼트: 15회 x 3세트\n- 푸쉬업: 10회 x 3세트\n- 데드리프트: 10회 x 3세트",
                "이미지": "images/squat.png"
            },
            "정상체중": {
                "운동": "🏃‍♂️ 유산소 + 근력 운동:\n- 러닝: 20~30분\n- 요가: 30분\n- 필라테스: 40분",
                "이미지": "images/running.png"
            },
            "과체중": {
                "운동": "🚴 유산소 중심 운동:\n- 빠르게 걷기: 40분\n- 자전거 타기: 30분\n- 수영: 30분",
                "이미지": "images/cycling.png"
            },
            "비만": {
                "운동": "🔥 고강도 유산소 운동:\n- 인터벌 트레이닝 (HIIT): 20분\n- 점핑 잭: 30회 x 3세트\n- 버피 테스트: 10회 x 3세트",
                "이미지": "images/hiit.png"
            }
        }

        # 운동 추천 리스트 (동적으로 업데이트될 부분)
        self.exercise_label = Label(text="", font_size='20sp', color=(0, 0, 0, 1))
        self.layout.add_widget(self.exercise_label)

        # 운동 방법 이미지 (동적으로 업데이트될 부분)
        self.exercise_image = Image(source="", size_hint=(1, 0.6))
        self.layout.add_widget(self.exercise_image)

        # 뒤로 가기 버튼
        self.back_button = Button(text="⬅ 뒤로 가기", size_hint=(1, 0.15), font_size='20sp', background_color=(0.6, 0.6, 0.6, 1))
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        # 레이아웃 추가
        self.add_widget(self.layout)

    def set_bmi_category(self, category):
        """ BMI 카테고리에 따라 운동 추천을 업데이트하는 함수 """
        if category in self.exercise_data:
            self.exercise_label.text = self.exercise_data[category]["운동"]
            self.exercise_image.source = self.exercise_data[category]["이미지"]
        else:
            self.exercise_label.text = "운동 추천 데이터를 찾을 수 없습니다."
            self.exercise_image.source = ""

    def go_back(self, instance):
        """ 이전 화면으로 돌아가기 """
        self.manager.current = "bmi_screen"
