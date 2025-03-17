import json
import os
import platform
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.text import LabelBase

# 사용자 데이터를 저장할 JSON 파일
USER_DATA_FILE = "users.json"

def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)

def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

users = load_users()

def get_korean_font():
    system = platform.system()
    if system == "Windows":
        return "C:/Windows/Fonts/malgun.ttf"  # Windows 기본 한글 폰트
    elif system == "Darwin":
        return "/System/Library/Fonts/AppleSDGothicNeo.ttc"  # macOS 기본 한글 폰트
    return "NotoSansCJK-Regular.otf"  # 리눅스 및 기타 시스템 기본 폰트

# 한글 폰트 등록
KOREAN_FONT = get_korean_font()
LabelBase.register(name='KoreanFont', fn_regular=KOREAN_FONT)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.size_hint = (0.8, 0.6)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        image = Image(source="images/Login.png", size_hint=(1, 0.3))
        self.layout.add_widget(image)

        email_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        email_icon = Image(source="images/email.png", size_hint=(0.15, 1))
        self.email_input = TextInput(hint_text="이메일 ID", multiline=False, size_hint=(0.85, 1), font_name='KoreanFont')
        email_layout.add_widget(email_icon)
        email_layout.add_widget(self.email_input)
        self.layout.add_widget(email_layout)

        password_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        password_icon = Image(source="images/password.png", size_hint=(0.15, 1))
        self.password_input = TextInput(hint_text="비밀번호", multiline=False, password=True, size_hint=(0.85, 1), font_name='KoreanFont')
        password_layout.add_widget(password_icon)
        password_layout.add_widget(self.password_input)
        self.layout.add_widget(password_layout)

        forgot_button = Button(text="비밀번호 찾기", size_hint=(1, 0.1), background_color=(0, 0, 0, 0), color=(0, 0, 1, 1), font_name='KoreanFont')
        self.layout.add_widget(forgot_button)

        self.login_button = Button(text="로그인", size_hint=(1, 0.2), background_color=(0, 0, 0, 1), font_name='KoreanFont')
        self.login_button.bind(on_press=self.on_login)
        self.layout.add_widget(self.login_button)

        sign_up_button = Button(text="회원가입", size_hint=(1, 0.1), background_color=(0, 0, 0, 1), color=(0, 0, 1, 1), font_name='KoreanFont')
        sign_up_button.bind(on_press=self.on_sign_up)
        self.layout.add_widget(sign_up_button)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_login(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        if email in users and users[email] == password:
            self.manager.current = 'gender_selection'
        else:
            self.show_error_popup()

    def show_error_popup(self):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_label = Label(text="아이디와 비밀번호가 일치하지 않습니다.", font_size='20sp', font_name='KoreanFont')
        close_button = Button(text="확인", size_hint=(1, 0.2), font_name='KoreanFont')
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title="오류", content=popup_layout, size_hint=(0.6, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def on_sign_up(self, instance):
        self.manager.current = 'sign_up_screen'


class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.size_hint = (0.8, 0.6)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # 화면에 제목 추가
        title_label = Label(text="회원가입", font_size='24sp', font_name=KOREAN_FONT)
        self.layout.add_widget(title_label)

        # 이메일 입력 필드 추가
        self.email_input = TextInput(hint_text="Email ID", multiline=False, size_hint=(1, 0.2), font_name=KOREAN_FONT)
        self.layout.add_widget(self.email_input)

        # 비밀번호 입력 필드 추가
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint=(1, 0.2), font_name=KOREAN_FONT)
        self.layout.add_widget(self.password_input)

        # 비밀번호 확인 필드 추가
        self.confirm_password_input = TextInput(hint_text="Confirm Password", multiline=False, password=True, size_hint=(1, 0.2), font_name=KOREAN_FONT)
        self.layout.add_widget(self.confirm_password_input)

        # 회원가입 버튼 추가
        sign_up_button = Button(text="회원가입", size_hint=(1, 0.2), background_color=(0, 0, 1, 1), font_name=KOREAN_FONT)
        sign_up_button.bind(on_press=self.on_sign_up)
        self.layout.add_widget(sign_up_button)

        # 뒤로가기 버튼 추가
        back_button = Button(text="뒤로가기", size_hint=(1, 0.2), background_color=(1, 0, 0, 1), font_name=KOREAN_FONT)
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

        # 기존 사용자 정보 불러오기
        self.users = load_users()

    def on_sign_up(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        confirm_password = self.confirm_password_input.text.strip()

        # 필드가 비어 있는지 체크
        if not email or not password or not confirm_password:
            self.show_popup("Error", "모든 필드를 입력해주세요.")
            return
        
        # 비밀번호 일치 체크
        if password != confirm_password:
            self.show_popup("Error", "비밀번호가 일치하지 않습니다.")
            return

        # 이메일이 이미 존재하는지 체크
        if email in self.users:
            self.show_popup("Error", "이미 가입된 이메일입니다.")
            return

        # 사용자 추가
        self.users[email] = password
        save_users(self.users)  # 사용자 데이터 파일에 저장

        # 성공 팝업 띄우기
        self.show_popup("Success", "회원가입이 완료되었습니다!")
        
        # 팝업 창이 닫히는 것과 동시에 로그인 화면으로 전환
        self.manager.current = 'login_screen'

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_label = Label(text=message, font_size='18sp', font_name=KOREAN_FONT)
        close_button = Button(text="확인", size_hint=(1, 0.2), font_name=KOREAN_FONT)
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'login_screen'  # 뒤로가기 버튼 클릭 시 로그인 화면으로 이동


class MyApp(App):
    def build(self):
        # 화면 매니저 설정
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(SignUpScreen(name='sign_up_screen'))
        return sm

if __name__ == "__main__":
    MyApp().run()
