import json
import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle

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

        self.login_button = Button(text="LOGIN", size_hint=(1, 0.2), background_color=(0, 0, 0, 1))
        self.login_button.bind(on_press=self.on_login)
        self.layout.add_widget(self.login_button)

        sign_up_button = Button(text="Sign Up", size_hint=(1, 0.1), background_color=(0, 0, 0, 1), color=(0, 0, 1, 1))
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
            print("로그인 성공!")
            self.manager.current = 'main_screen'
        else:
            print("로그인 실패: 잘못된 이메일 또는 비밀번호")

    def on_sign_up(self, instance):
        self.manager.current = 'sign_up_screen'


class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.size_hint = (0.8, 0.6)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        image = Image(source="images/Login.png", size_hint=(1, 0.3))
        self.layout.add_widget(image)

        self.name_input = TextInput(hint_text="Full Name", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.name_input)

        self.email_input = TextInput(hint_text="Email ID", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.email_input)

        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint=(1, 0.1))
        self.layout.add_widget(self.password_input)

        self.confirm_password_input = TextInput(hint_text="Confirm Password", multiline=False, password=True, size_hint=(1, 0.1))
        self.layout.add_widget(self.confirm_password_input)

        sign_up_button = Button(text="SIGN UP", size_hint=(1, 0.2), background_color=(0, 0, 0, 1))
        sign_up_button.bind(on_press=self.on_sign_up)
        self.layout.add_widget(sign_up_button)

        back_button = Button(text="Back to Login", size_hint=(1, 0.1), background_color=(0, 0, 0, 1))
        back_button.bind(on_press=self.on_back_to_login)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def on_sign_up(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        if email in users:
            print("이미 존재하는 이메일입니다.")
        elif password != confirm_password:
            print("비밀번호가 일치하지 않습니다.")
        else:
            users[email] = password
            save_users(users)  # JSON 파일에 저장
            print(f"{email} 회원가입 성공!")
            self.manager.current = 'login'

    def on_back_to_login(self, instance):
        self.manager.current = 'login'


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.content_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9))
        self.layout.add_widget(self.content_layout)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=20)
        exercise_button = Button(text='Exercise', size_hint=(None, 1), width=200)
        exercise_button.bind(on_press=self.on_exercise_button_pressed)
        button_layout.add_widget(exercise_button)

        self.layout.add_widget(button_layout)
        self.add_widget(self.layout)

    def on_exercise_button_pressed(self, instance):
        self.manager.current = 'exercise_screen'


class HealthTrackerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignUpScreen(name='sign_up_screen'))
        sm.add_widget(MainScreen(name='main_screen'))
        return sm


if __name__ == "__main__":
    HealthTrackerApp().run()