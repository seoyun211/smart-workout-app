import platform
import os
from Height_Weight_Screen import HeightWeightScreen
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
            background_color=(0.6, 0.6, 0.6, 1),  # ✅ 연한 회색 배경
            color=(1, 1, 1, 1) 
        )
        self.next_button.bind(on_press=self.show_next_exercise)
        button_layout.add_widget(self.next_button)

        # "뒤로 가기" 버튼
        self.back_button = Button(
            text="뒤로 가기",
            font_name=KOREAN_FONT,
            size_hint=(0.4, 1),
            background_color=(0.6, 0.6, 0.6, 1),  # ✅ 연한 회색 배경
            color=(1, 1, 1, 1) 
        )
        self.back_button.bind(on_press=self.go_back)
        button_layout.add_widget(self.back_button)

        self.layout.add_widget(button_layout)  # 버튼 레이아웃 추가
        self.add_widget(self.layout)

        # ✅ 운동 데이터
        self.exercise_data = {
            "저체중": {
                "운동" : ["스쿼트", "벤치프레스", "데드리프트", "풀업", "런지"],
                "미디어" : ["images/스쿼트.mp4", "images/벤치프레스.mp4", "images/데드리프트.mp4", "images/풀업.mp4", "images/런지.mp4"],
                "설명" : ["1. 다리를 어깨너비만큼 벌리고 곧게 섭니다.\n" "2. 가슴을 편 상태로 엉덩이를 뒤로 빼며 앉습니다. \n" "3. 발바닥으로 지면을 밀고 일어나면서 시작 자세로 돌아옵니다.",
                        "1. 벤치에 누운 상태에서, 바벨을 넓게 잡고 들어올립니다.\n" "2. 가슴 근육의 이완을 느끼며 바벨을 가슴 방향으로 내립니다.\n" "3. 가슴 근육의 수축을 느끼며 바벨을 밀어올립니다.",
                        "1. 양발을 넓게 벌리고, 바벨도 넓게잡아 무릎과 팔이 겹치지 않도록 합니다.\n" "2. 등이 굽지않게 유지하면서, 바벨을 들어 올립니다. \n" "3. 몸을 완전히 쭉 피고 엉덩이 근육을 수축합니다.",
                        "1. 팔을 벌리고, 손바닥이 앞을 바라본 상태로 매달립니다.\n" "2. 가슴을 편 상태로 바를 구부려 준다는 느낌으로 팔을 당겨 올라갑니다.\n" "3. 상체가 흔들리지 않도록 자세를 유지하면서 내려옵니다.",
                        "1. 양발을 골반 너비만큼 벌리고 상체를 곧게 펴고 섭니다.\n" "2. 한쪽 다리를 뻗어 앞으로 나가면서 두 무릎이 90가 되게 엉덩이를 낮춰줍니다.\n" "3. 앞발의 뒤꿈치에 무게 중심을 실어서 몸을 위쪽으로 밀어주며 원래 시작 자세로 돌아옵니다."]
            },

            "정상체중":{
                "운동": ["달리기", "싸이클", "플랭크", "로잉머신", "점프스쿼트"],
                "미디어": ["images/달리기.mp4", "images/싸이클.mp4", "images/플랭크.mp4", "images/로잉머신.mp4", "images/점프스쿼트.mp4"],
                "설명" : ["1. 올바른 자세로 달립니다.\n",
                        "1. 안장을 체형에 맞게 조절합니다.\n" "2. 두 발을 페달에 넣고 굴립니다.\n" "3. 강도를 조절하며 반복합니다.",
                        "1. 손목과 팔꿈치를 바닥에 댄 상태로 바닥에 엎드립니다.\n" "2. 복부와 엉덩이에 힘을 주며 몸을 밀어 올립니다.\n" "3. 팔꿈치로 바닥을 밀며 자세를 유지합니다.",
                        "1. 핸들을 잡고 양 발을 고정시킨 후 발판을 밀어냅니다.\n" "2. 다리가 펴지면 45도로 몸을 뒤로 젖힙니다.\n" "3. 당겼던 팔을 다시 펴고 시작 자세로 되돌아갑니다.",
                        "1. 다리를 어깨너비만큼 벌리고 허리를 펴고 곧게 섭니다.\n" "2. 가슴을 편 상태로 엉덩이를 뒤로 빼며 앉습니다.\n" "3. 복근에 힘을 주고 골반을 밀어 올리면서 높이 뛰어오릅니다."]
              
            },

            "과체중": {
                "운동": ["빠르게 걷기(트레드밀)", "줄넘기", "버피", "레그프레스", "케틀벨스윙"],
                "미디어": ["images/트레드밀.mp4", "images/줄넘기.mp4", "images/버피.mp4", "images/레그프레스.mp4", "images/케틀벨스윙.mp4"],
                "설명" : ["1. 속도를 알맞게 조절하고 운동합니다.\n" "2. 경사를 알맞게 조절하고 운동합니다.\n",
                        "1. 몸에 힘을 빼고 곧게 섭니다.\n" "2. 줄넘기를 손목의 힘으로 가볍게 돌려줍니다.\n" "3. 무릎의 탄력을 이용하여 점프해 줄을 넘습니다.",
                        "1. 곧게 섰다가 스쿼트 자세를 후 팔굽혀펴기를 수행합니다. \n" "2.다리를 가슴 쪽으로 당겨 돌아옵니다.\n" "3. 일어나면서 양손을 뻗으면서 점프합니다.",
                        "1. 의자에 앉아서 두발을 발판에 올립니다.\n" "2. 무릎을 굽힙니다. 엉덩이와 허리가 뜨지않게 중량판을 내립니다.\n" "3. 복부에 힘을 주고, 중량판을 밀어 올립니다.",
                        "1. 양발을 넓게 벌리고, 양손으로 케틀벨을 잡습니다.\n" "2. 허리가 굽지 않도록, 케틀벨을 다리 사이로 보냅니다.\n" "3. 둔근을 수축하는 힘으로 케틀벨을 밀어 올립니다."]
            },
            "비만": {
                "운동": ["걷기", "일립티컬머신", "스텝업", "계단오르기", "싸이클"],
                "미디어": ["images/걷기.mp4", "images/일립티컬머신.mp4", "images/스텝업.mp4", "images/계단오르기.mp4", "images/싸이클.mp4"],
                "설명" : ["1. 바른 자세로 걷습니다.\n",
                        "1. 핸들을 잡습니다.\n" "2. 두 발과 손을 번갈아 가면서 흔듭니다.\n" "3. 강도를 조절해 반복합니다.",
                        "1. 구조물 앞에 선 후, 한 발씩 구조물로 올라갑니다. \n" "2. 구조물 위에서 몸을 피고 섭니다.\n" "3. 한 발씩 바닥으로 내려옵니다.",
                        "1. 넘어지지 않게 유의하면서 계단을 한칸씩 올라갑니다.\n" "2. 발목에 무리가지않게 반복합니다.\n",
                        "1.  안장을 체형에 맞게 조절합니다.\n" "2. 두 발을 페달에 넣고 굴립니다.\n" "3. 강도를 조절하며 반복합니다."]
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

def go_to_height_weight_screen(self, instance):
    screen_manager = self.manager

    if not screen_manager.has_screen("height_weight_screen"):
        screen_manager.add_widget(HeightWeightScreen(name="height_weight_screen"))

    screen_manager.current = "height_weight_screen"
