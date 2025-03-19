import platform
import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.video import Video

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

        # 메인 레이아웃 (세로 정렬)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # 제목 라벨 (상단)
        self.title_label = Label(
            text="운동 추천",
            font_size='26sp',
            bold=True,
            font_name=KOREAN_FONT,
            size_hint=(1, 0.1)  # 공간 확보 (더 위로)
        )
        self.layout.add_widget(self.title_label)

        # 운동 이름 표시 (더 위로 조정)
        self.exercise_label = Label(
            text="운동: ",
            font_size='22sp',  # 조금 더 크게
            font_name=KOREAN_FONT,
            size_hint=(1, 0.08)  # 크기 줄여서 위로 올림
        )
        self.layout.add_widget(self.exercise_label)

        # ✅ 비디오 플레이어 (중앙 크고 정렬)
        self.exercise_video = Video(
            source="",
            size_hint=(1, 0.55)  # 비디오 크기 조정
        )
        self.layout.add_widget(self.exercise_video)

        # ✅ 설명 라벨 (비디오 아래에 추가)
        self.description_label = Label(
            text="운동 설명이 여기에 표시됩니다.",
            font_size='18sp',
            font_name=KOREAN_FONT,
            size_hint=(1, 0.1)  # 설명 공간 추가
        )
        self.layout.add_widget(self.description_label)

        # 버튼 레이아웃 (가로 정렬, 버튼 작게)
        button_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint=(1, 0.08))

        # "다음" 버튼 (작게 조정)
        self.next_button = Button(
            text="다음",
            font_name=KOREAN_FONT,
            size_hint=(0.4, 1)  # 버튼 크기 축소
        )
        self.next_button.bind(on_press=self.show_next_exercise)
        button_layout.add_widget(self.next_button)

        # "뒤로 가기" 버튼 (작게 조정)
        self.back_button = Button(
            text="뒤로 가기",
            font_name=KOREAN_FONT,
            size_hint=(0.4, 1)  # 버튼 크기 축소
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
                         ["데드리프트 하는법"]
                         ["풀업"]
                         ["런지"]
                         ["벤치프레스스"]
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

        self.current_category = None  # 현재 BMI 카테고리
        self.current_index = 0  # 현재 표시 중인 운동 인덱스

    def play_video(self, *args):
        """비디오 로드 후 자동 재생"""
        if self.exercise_video and self.exercise_video.loaded:
            self.exercise_video.seek(0)
            self.exercise_video.state = 'play'

    def set_bmi_category(self, category):
        """BMI 카테고리에 따라 운동 추천 리스트 설정"""
        if category in self.exercise_data:
            self.current_category = category
            self.current_index = 0  # 처음부터 시작
            self.update_exercise_display()
        else:
            self.exercise_label.text = "운동 추천 데이터를 찾을 수 없습니다."

    def update_exercise_display(self):
        """현재 인덱스에 맞는 운동과 영상을 표시"""
        if self.current_category:
            exercises = self.exercise_data[self.current_category]["운동"]
            videos = self.exercise_data[self.current_category]["미디어"]
            descriptions = self.exercise_data[self.current_category].get("설명", [])  # 설명이 없을 수도 있음
        
            if self.current_index < len(exercises):
                self.exercise_label.text = f"운동: {exercises[self.current_index]}"

                # ✅ 설명이 있으면 표시, 없으면 기본값 설정
                if self.current_index < len(descriptions):
                    self.description_label.text = descriptions[self.current_index]
                else:
                    self.description_label.text = "운동 설명이 없습니다."

                # ✅ 기존 비디오 초기화 후 새로운 비디오 설정
                video_path = videos[self.current_index]
                if video_path and os.path.exists(video_path):
                    self.exercise_video.source = ""
                    self.exercise_video.source = video_path
                    self.exercise_video.state = 'play'
                else:
                    print(f"⚠️ 오류: {video_path} 파일이 존재하지 않음.")
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
        """이전 화면(키 & 몸무게 입력)으로 돌아가기"""
        self.manager.current = "height_weight_screen"
