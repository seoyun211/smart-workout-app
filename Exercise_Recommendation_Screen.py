import platform
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image

# ✅ 한글 폰트 설정
def get_korean_font():
    system = platform.system() 
    if system == "Windows":
        return "C:/Windows/Fonts/malgun.ttf"
    elif system == "Darwin":
        return "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    return "NotoSansCJK-Regular.otf"

KOREAN_FONT = get_korean_font()

class ExerciseRecommendationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # 제목
        self.title_label = Label(text="운동 추천", font_size='24sp', bold=True, font_name=KOREAN_FONT)
        self.layout.add_widget(self.title_label)

        # 📝 1️⃣ 전체 운동 리스트 보여주는 라벨
        self.summary_label = Label(text="", font_size='18sp', font_name=KOREAN_FONT)
        self.layout.add_widget(self.summary_label)

        # "운동 시작" 버튼
        self.start_button = Button(text="운동 시작", size_hint=(1, 0.15), font_name=KOREAN_FONT)
        self.start_button.bind(on_press=self.start_exercise)
        self.layout.add_widget(self.start_button)

        # 🏋️‍♂️ 2️⃣ 개별 운동 표시 라벨 & 이미지
        self.exercise_label = Label(text="", font_size='20sp', font_name=KOREAN_FONT)
        self.exercise_label.opacity = 0  # 처음에는 숨김
        self.layout.add_widget(self.exercise_label)

        self.exercise_image = Image(source="", size_hint=(1, 0.5))
        self.exercise_image.opacity = 0  # 처음에는 숨김
        self.layout.add_widget(self.exercise_image)

        # "다음" 버튼 (운동 넘기기)
        self.next_button = Button(text="다음", size_hint=(1, 0.15), font_name=KOREAN_FONT)
        self.next_button.bind(on_press=self.show_next_exercise)
        self.next_button.opacity = 0  # 처음에는 숨김
        self.layout.add_widget(self.next_button)

        # "뒤로 가기" 버튼
        self.back_button = Button(text="뒤로 가기", size_hint=(1, 0.15), font_name=KOREAN_FONT)
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

        # 운동 데이터
        self.exercise_data = {
            "저체중": {
                "운동": ["스쿼트", "푸쉬업", "데드리프트"],
                "이미지": ["images/squat.png", "images/pushup.png", "images/deadlift.png"]
            },
            "정상체중": {
                "운동": ["러닝", "요가", "필라테스"],
                "이미지": ["images/running.png", "images/yoga.png", "images/pilates.png"]
            },
            "과체중": {
                "운동": ["빠르게 걷기", "사이클", "수영"],
                "이미지": ["images/walk.png", "images/cycle.png", "images/swim.png"]
            },
            "비만": {
                "운동": ["HIIT", "인터벌 트레이닝"],
                "이미지": ["images/hiit.png", "images/interval.png"]
            }
        }

        self.current_category = None  # 현재 BMI 카테고리
        self.current_index = 0  # 현재 표시 중인 운동 인덱스

    def set_bmi_category(self, category):
        """BMI 카테고리에 따라 운동 추천 리스트를 설정"""
        if category in self.exercise_data:
            self.current_category = category
            self.current_index = 0  # 처음부터 시작

            # 📝 1️⃣ 전체 운동 리스트 표시
            exercises = self.exercise_data[category]["운동"]
            self.summary_label.text = "추천 운동 목록:\n" + "\n".join(f"• {ex}" for ex in exercises)

            # 개별 운동 관련 요소 숨김
            self.exercise_label.opacity = 0
            self.exercise_image.opacity = 0
            self.next_button.opacity = 0

            # "운동 시작" 버튼 보이기
            self.start_button.opacity = 1
        else:
            self.summary_label.text = "운동 추천 데이터를 찾을 수 없습니다."

    def start_exercise(self, instance):
        """운동 시작 버튼을 누르면 개별 운동 표시로 전환"""
        self.start_button.opacity = 0  # 시작 버튼 숨김
        self.summary_label.opacity = 0  # 운동 목록 숨김

        # 개별 운동 요소 보이기
        self.exercise_label.opacity = 1
        self.exercise_image.opacity = 1
        self.next_button.opacity = 1

        self.update_exercise_display()

    def update_exercise_display(self):
        """현재 인덱스에 맞는 운동과 이미지를 표시"""
        if self.current_category:
            exercises = self.exercise_data[self.current_category]["운동"]
            images = self.exercise_data[self.current_category]["이미지"]

            if self.current_index < len(exercises):
                self.exercise_label.text = f"운동: {exercises[self.current_index]}"
                self.exercise_image.source = images[self.current_index]
            else:
                self.exercise_label.text = "운동이 끝났습니다!"
                self.exercise_image.source = ""

    def show_next_exercise(self, instance):
        """다음 운동을 보여주는 함수"""
        if self.current_category:
            if self.current_index < len(self.exercise_data[self.current_category]["운동"]) - 1:
                self.current_index += 1
                self.update_exercise_display()
            else:
                self.exercise_label.text = "운동이 끝났습니다!"
                self.exercise_image.source = ""

    def go_back(self, instance):
        """이전 화면(키 & 몸무게 입력)으로 돌아가기"""
        self.manager.current = "height_weight_screen"
