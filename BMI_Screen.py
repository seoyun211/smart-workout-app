import json
import platform
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

# 운영체제에 따라 폰트 경로 설정
def get_korean_font():
    system = platform.system()
    if system == "Windows":
        return "malgun.ttf"  # 윈도우 기본 한글 폰트 (맑은 고딕)
    elif system == "Darwin":  # macOS
        return "/System/Library/Fonts/Supplemental/AppleSDGothicNeo.ttc"  # macOS 기본 한글 폰트
    else:
        return "NotoSansCJK-Regular.otf"  # 프로젝트 내부 폰트 (리눅스 대비)

KOREAN_FONT = get_korean_font()

class BMIScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = 0
        self.weight = 0
        self.username = "user1"  # 로그인한 사용자 이름 (예시)
        
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 키 입력 필드
        self.height_input = TextInput(hint_text='키 (cm)', multiline=False, font_size=20, font_name=KOREAN_FONT)
        self.layout.add_widget(self.height_input)
        
        # 몸무게 입력 필드
        self.weight_input = TextInput(hint_text='몸무게 (kg)', multiline=False, font_size=20, font_name=KOREAN_FONT)
        self.layout.add_widget(self.weight_input)
        
        # BMI 결과 레이블
        self.bmi_label = Label(text=f'당신의 BMI: {self.calculate_bmi():.2f}', font_size='24sp', font_name=KOREAN_FONT)
        self.result_label = Label(text=f'분류: {self.get_bmi_category()}', font_size='28sp', bold=True, font_name=KOREAN_FONT)
        
        # 뒤로 가기 버튼
        back_button = Button(text='뒤로 가기', on_press=self.go_back, font_name=KOREAN_FONT)
        
        self.layout.add_widget(self.bmi_label)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)

    def calculate_bmi(self):
        try:
            height = float(self.height_input.text)  # 텍스트 입력에서 값 가져오기
            weight = float(self.weight_input.text)
            self.height = height
            self.weight = weight
            return weight / (height / 100) ** 2  # BMI 계산
        except ValueError:
            return 0  # 텍스트 입력 값이 숫자가 아니면 0 반환
    
    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return '저체중'
        elif 18.5 <= bmi < 25:
            return '정상체중'
        else:
            return '과체중'
    
    def go_back(self, instance):
        # BMI 값을 로그인한 사용자 정보에 저장
        self.update_user_bmi()

        # 이전 화면으로 돌아가기
        self.manager.current = 'height_weight_screen'
    
    def update_user_bmi(self):
        # JSON 파일에서 사용자 데이터 읽기
        try:
            with open('users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = []  # 파일이 없으면 빈 리스트로 시작
        
        # 로그인한 사용자의 정보 찾기
        for user in users:
            if user["username"] == self.username:
                user["height"] = self.height
                user["weight"] = self.weight
                user["bmi"] = self.calculate_bmi()  # BMI 값 업데이트
                break
        else:
            # 사용자 정보가 없으면 새로 추가
            users.append({
                "username": self.username,
                "height": self.height,
                "weight": self.weight,
                "bmi": self.calculate_bmi()
            })
        
        # 수정된 데이터 다시 저장
        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
