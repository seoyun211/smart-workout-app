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

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # 제목
        self.title_label = Label(text="운동 추천", font_size='24sp', bold=True, font_name=KOREAN_FONT)
        self.layout.add_widget(self.title_label)

        # 📝 전체 운동 리스트 보여주는 라벨
        self.summary_label = Label(text="", font_size='18sp', font_name=KOREAN_FONT)
        self.layout.add_widget(self.summary_label)

        # "운동 시작" 버튼
        self.start_button = Button(text="운동 시작", size_hint=(1, 0.15), font_name=KOREAN_FONT)
        self.start_button.bind(on_press=self.start_exercise)
        self.layout.add_widget(self.start_button)

        # 🏋️‍♂️ 개별 운동 표시 라벨
        self.exercise_label = Label(text="", font_size='20sp', font_name=KOREAN_FONT)
        self.exercise_label.opacity = 0  # 처음에는 숨김
        self.layout.add_widget(self.exercise_label)

        # ✅ MP4 영상 플레이어 (운동 영상 전용)
        self.exercise_video = Video(source="", size_hint=(1, 0.5))
        self.exercise_video.opacity = 0
        self.layout.add_widget(self.exercise_video)

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

        # ✅ 운동 데이터 (상대 경로 사용)
        self.exercise_data = {
            "저체중": {
                "운동": ["스쿼트", "벤치프레스", "데드리프트", "풀업", "런지"],
                "미디어": ["images/스쿼트.mp4", "images/벤치프레스.mp4", "images/deadlift.mp4", "images/pullup.mp4", "images/lunge.mp4"]
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
        """비디오가 로드된 후 자동 재생"""
        if self.exercise_video and self.exercise_video.loaded:
            self.exercise_video.seek(0)
            self.exercise_video.state = 'play'

    def set_bmi_category(self, category):
        """BMI 카테고리에 따라 운동 추천 리스트를 설정"""
        if category in self.exercise_data:
            self.current_category = category
            self.current_index = 0  # 처음부터 시작

            # 📝 전체 운동 리스트 표시
            exercises = self.exercise_data[category]["운동"]
            self.summary_label.text = "추천 운동 목록:\n" + "\n".join(f"• {ex}" for ex in exercises)

            # 개별 운동 관련 요소 숨김
            self.exercise_label.opacity = 0
            self.exercise_video.opacity = 0
            self.next_button.opacity = 0

            # "운동 시작" 버튼 보이기
            self.start_button.opacity = 1
        else:
            self.summary_label.text = "운동 추천 데이터를 찾을 수 없습니다."

    def start_exercise(self, instance):
        """운동 시작 버튼을 누르면 개별 운동 표시로 전환"""
        self.start_button.opacity = 0  # 시작 버튼 숨김
        self.summary_label.opacity = 0  # 운동 목록 숨김
        self.show_next_exercise(None)

        # 개별 운동 요소 보이기
        self.exercise_label.opacity = 1
        self.exercise_video.opacity = 1
        self.next_button.opacity = 1

        self.update_exercise_display()

    def update_exercise_display(self):
        """현재 인덱스에 맞는 운동과 영상을 표시"""
        if self.current_category:
            exercises = self.exercise_data[self.current_category]["운동"]
            videos = self.exercise_data[self.current_category]["미디어"]

            if self.current_index < len(exercises):
                self.exercise_label.text = f"운동: {exercises[self.current_index]}"

                # ✅ 기존 비디오 초기화 후 새로운 비디오 설정
                video_path = videos[self.current_index]

                if video_path and os.path.exists(video_path):
                    self.exercise_video.source = ""
                    self.exercise_video.source = video_path

                    # ✅ 비디오 바인딩 및 자동 재생 설정
                    self.exercise_video.unbind(on_load=self.play_video)
                    self.exercise_video.bind(on_load=self.play_video)
                    self.exercise_video.state = 'play'
                else:
                    print(f"⚠️ 오류: {video_path} 파일이 존재하지 않음.")
                    self.exercise_label.text = "⚠️ 비디오 파일을 찾을 수 없습니다."
                    self.exercise_video.source = ""

            else:
                self.exercise_label.text = "운동이 끝났습니다!"
                self.exercise_video.source = ""



    def show_next_exercise(self, instance):
        """다음 운동을 보여주는 함수"""
        if self.current_category and self.current_index < len(self.exercise_data[self.current_category]["운동"]) - 1:
            self.current_index += 1
            self.update_exercise_display()
        else:
            self.exercise_label.text = "운동이 끝났습니다!"
            self.exercise_video.source = ""

    def go_back(self, instance):
        """이전 화면(키 & 몸무게 입력)으로 돌아가기"""
        self.manager.current = "height_weight_screen"
