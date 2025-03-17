import json
import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
import platform

# 사용자 데이터를 저장할 JSON 파일
USER_DATA_FILE = "users.json"

# 사용자 데이터 저장 함수
def save_users(users):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(users, f)

# 사용자 데이터 불러오기 함수
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as f:
            return json.load(f)
    return {}

# 기존 사용자 데이터 불러오기
users = load_users()

from kivy.uix.button import Button
from kivy.app import App

def get_korean_font():
    system = platform.system()
    # DejaVuSans는 대부분의 시스템에 기본적으로 제공되는 폰트입니다.
    return "DejaVuSans.ttf"  # macOS와 리눅스에서 공통적으로 사용할 수 있는 폰트

KOREAN_FONT = get_korean_font()

class MyApp(App):
    def build(self):
        # DejaVuSans 폰트를 적용한 버튼을 생성합니다.
        login_button = Button(
            text="LOGIN", 
            size_hint=(1, 0.2), 
            background_color=(0, 0, 0, 1), 
            font_name=KOREAN_FONT
        )
        return login_button

if __name__ == "__main__":
    MyApp().run()

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
        self.email_input = TextInput(hint_text="Email ID", multiline=False, size_hint=(0.85, 1))
        email_layout.add_widget(email_icon)
        email_layout.add_widget(self.email_input)
        self.layout.add_widget(email_layout)

        password_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        password_icon = Image(source="images/password.png", size_hint=(0.15, 1))
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint=(0.85, 1))
        password_layout.add_widget(password_icon)
        password_layout.add_widget(self.password_input)
        self.layout.add_widget(password_layout)

        forgot_button = Button(text="Forgot Password?", size_hint=(1, 0.1), background_color=(0, 0, 0, 0), color=(0, 0, 1, 1))
        self.layout.add_widget(forgot_button)

        self.login_button = Button(text="LOGIN", size_hint=(1, 0.2), background_color=(0, 0, 0, 1), font_name=KOREAN_FONT)
        self.login_button.bind(on_press=self.on_login)
        self.layout.add_widget(self.login_button)

        sign_up_button = Button(text="Sign Up", size_hint=(1, 0.1), background_color=(0, 0, 0, 1), color=(0, 0, 1, 1), font_name=KOREAN_FONT)
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
        popup_label = Label(text="ID와 Password가 일치하지 않습니다.", font_size='20sp', font_name=KOREAN_FONT)
        close_button = Button(text="확인", size_hint=(1, 0.2), font_name=KOREAN_FONT)
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title="Error", content=popup_layout, size_hint=(0.6, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def on_sign_up(self, instance):
        self.manager.current = 'sign_up_screen'
