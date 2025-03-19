import platform
import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.graphics import Color, Rectangle  # ✅ 배경색을 위해 추가

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

        # ✅ 배경을 흰색으로 설정 (Canvas 사용)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # RGB (1,1,1) = 흰색
            self.rect = Rectangle(size=self.size, pos=self.pos)
        
        self.bind(size=self.update_background, pos=self.update_background)  # ✅ 크기 변경 시 배경 유지

        # 메인 레이아웃 (세로 정렬)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # 제목 라벨 (상단)
        self.title_label = Label(
            text="운동 추천",
            font_size='26sp',
            bold=True,
            font_name=KOREAN_FONT,
            color=(0, 0, 0, 1),  # ✅ 글씨 검은색
            size_hint=(1, 0.1)  # 공간 확보 (더 위로)
        )
        self.layout.add_widget(self.title_label)

        # 운동 이름 표시
        self.exercise_label = Label(
            text="운동: ",
            font_size='22sp',
            font_name=KOREAN_FONT,
            color=(0, 0, 0, 1),  # ✅ 글씨 검은색
            size_hint=(1, 0.08)  
        )
        self.layout.add_widget(self.exercise_label)

        # ✅ 비디오 플레이어 (중앙 크고 정렬)
        self.exercise_video = Video(
            source="",
            size_hint=(1, 0.55)  
        )
        self.layout.add_widget(self.exercise_video)

        # ✅ 설명 라벨 (비디오 아래에 추가)
        self.description_label = Label(
            text="운동 설명이 여기에 표시됩니다.",
            font_size='18sp',
            font_name=KOREAN_FONT,
            color=(0, 0, 0, 1),  # ✅ 글씨 검은색
            size_hint=(1, 0.1)  
        )
        self.layout.add_widget(self.description_label)

        # 버튼 레이아웃 (가로 정렬, 버튼 작게)
        button_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.08))

        # "다음" 버튼
        self.next_button = Button(
            text="다음",
            font_name=KOREAN_FONT,
            size_hint=(0.4, 1),
            background_color=(0.8, 0.8, 0.8, 1),  # ✅ 연한 회색 배경
            color=(0, 0, 0, 1)  # ✅ 글씨 검은색
        )
        self.next_button.bind(on_press=self.show_next_exercise)
        button_layout.add_widget(self.next_button)

        # "뒤로 가기" 버튼
        self.back_button = Button(
            text="뒤로 가기",
            font_name=KOREAN_FONT,
            size_hint=(0.4, 1),
            background_color=(0.8, 0.8, 0.8, 1),  # ✅ 연한 회색 배경
            color=(0, 0, 0, 1)  # ✅ 글씨 검은색
        )
        self.back_button.bind(on_press=self.go_back)
        button_layout.add_widget(self.back_button)

        self.layout.add_widget(button_layout)  # 버튼 레이아웃 추가
        self.add_widget(self.layout)

        # ✅ 운동 데이터
        self.exercise_data = {
            "저체중": {
                "운동" : ["스쿼트", "벤치프레스", "데드리프트", "풀업", "런지"],
                "미디어" : ["images/스쿼트.mp4", "images/벤치프레스.mp4", "images/deadlift.mp4", "images/pullup.mp4", "images/lunge.mp4"],
                "설명" : ["1. 다리를 어깨너비만큼 벌리고 곧게 섭니다.\n" "2. 가슴을 편 상태로 엉덩이를 뒤로 빼며 앉습니다. \n" "3. 발바닥으로 지면을 밀고 일어나면서 시작 자세로 돌아옵니다."]
                        
            },
            "정상체중": {
                "운동": ["달리기", "사이클", "플랭크", "로잉 머신", "점프 스쿼트"],
                "미디어": ["images/running.mp4", "images/cycling.mp4", "images/plank.mp4", "images/rowing.mp4", "images/jump_squat.mp4"]
            },
            "과체중": {
                "운동": ["빠르게 걷기(트레드밀)", "줄넘기", "버피", "레그프레스", "케틀벨 스윙"],
                "미디어": ["images/fast_walk.mp4", "images/jump_rope.mp4", "images/burpee.mp4", "images/leg_press.mp4", "images/kettlebell_swing.mp4"]
            },
            "비만": {
                "운동": ["걷기", "일립티컬 머신", "스텝업", "계단오르기", "사이클"],
                "미디어": ["images/walk.mp4", "images/elliptical.mp4", "images/step_up.mp4", "images/stair_climb.mp4", "images/bike.mp4"]
            }
        }
        

        self.current_category = None
        self.current_index = 0

    def update_background(self, *args):
        """화면 크기 변경 시 배경 유지"""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def set_bmi_category(self, category):
        """BMI 카테고리에 따라 운동 추천 리스트 설정"""
        if category in self.exercise_data:
            self.current_category = category
            self.current_index = 0
            self.update_exercise_display()
        else:
            self.exercise_label.text = "운동 추천 데이터를 찾을 수 없습니다."

    def update_exercise_display(self):
        """현재 인덱스에 맞는 운동과 영상을 표시"""
        if self.current_category:
            exercises = self.exercise_data[self.current_category]["운동"]
            videos = self.exercise_data[self.current_category]["미디어"]
            descriptions = self.exercise_data[self.current_category]["설명"]

            if self.current_index < len(exercises):
                self.exercise_label.text = f"운동: {exercises[self.current_index]}"
                self.description_label.text = descriptions[self.current_index]

                video_path = os.path.abspath(videos[self.current_index])  # ✅ 절대 경로 변환

                print("비디오 경로:", video_path, "존재 여부:", os.path.exists(video_path))  # ✅ 경로 확인

                if os.path.exists(video_path):
                    self.exercise_video.source = ""  # ✅ 기존 소스 초기화 (필수)
                    self.exercise_video.source = video_path

                    if hasattr(self, "play_video"):
                        self.exercise_video.unbind(on_load=self.play_video)  # ✅ 기존 이벤트 해제
                        self.exercise_video.bind(on_load=self.play_video)  # ✅ 새 이벤트 등록
                    self.exercise_video.state = 'play'  # ✅ 자동 재생
                else:
                    print(f"⚠️ 파일 없음: {video_path}")
                    self.exercise_label.text = "⚠️ 비디오 파일을 찾을 수 없습니다."
                    self.exercise_video.source = ""
            else:
                self.exercise_label.text = "운동이 끝났습니다!"
                self.exercise_video.source = ""
                self.description_label.text = ""

    def show_next_exercise(self, instance):
        """다음 운동을 보여주는 함수"""
        if self.current_category and self.current_index < len(self.exercise_data[self.current_category]["운동"]) - 1:
            self.current_index += 1
            self.update_exercise_display()
        else:
            self.exercise_label.text = "운동이 끝났습니다!"
            self.exercise_video.source = ""
            self.description_label.text = ""

    def go_back(self, instance):
        """이전 화면으로 돌아가기"""
        self.manager.current = "height_weight_screen"
