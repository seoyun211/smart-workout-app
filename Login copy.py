import json
import os
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
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
            self.manager.current = 'gender_selection'
        else:
            self.show_error_popup()

    def show_error_popup(self):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_label = Label(text="ID와 Password가 일치하지 않습니다.", font_size='20sp',font_name="malgun.ttf")
        close_button = Button(text="확인", size_hint=(1, 0.2), font_name="malgun.ttf")
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title="Error", content=popup_layout, size_hint=(0.6, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def on_sign_up(self, instance):
        self.manager.current = 'sign_up_screen'

class GenderSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.size_hint = (0.8, 0.8)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        #성별 이미지
        image = Image(source="images/성별.png", size_hint=(1, 0.5), pos_hint={'center_x': 0.5, 'center_y': 0.6})  
        self.layout.add_widget(image)

        def create_gender_button(text, bg_color, text_color, gender):
            btn = Button(
                text=text,
                size_hint=(1, 0.15),
                font_name="malgun.ttf",
                color=text_color,
                background_color=(0, 0, 0, 0),  # 기본 배경 투명
                background_normal=''  # Kivy 기본 스타일 제거
            )
            with btn.canvas.before:
                btn.bg_color = Color(*bg_color)
                btn.rect = Rectangle(size=btn.size, pos=btn.pos)

            # 버튼 크기와 위치 바인딩
            btn.bind(size=lambda instance, value: setattr(btn.rect, 'size', value))
            btn.bind(pos=lambda instance, value: setattr(btn.rect, 'pos', value))
            btn.bind(on_press=lambda instance: self.on_gender_select(gender))
            return btn

        # 남성 버튼: 배경색(연한 하늘색), 글씨색(진한 파란색)
        male_button = create_gender_button(
            "남성",
            bg_color=(169/255, 206/255, 229/255, 1),  # 연한 하늘색 (#A9CEE5)
            text_color=(11/255, 18/255, 142/255, 1),  # 진한 파란색 글씨
            gender="남성"
        )
        self.layout.add_widget(male_button)

        # 여성 버튼: 배경색(연한 핑크색), 글씨색(진한 빨간색)
        female_button = create_gender_button(
            "여성",
            bg_color=(244/255, 194/255, 194/255, 1),  # 연한 핑크색 (#F4C2C2)
            text_color=(200/255, 0, 0, 1),  # 진한 빨간색 글씨
            gender="여성"
        )
        self.layout.add_widget(female_button)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_gender_select(self, gender):
        # 성별 선택 후 처리 (예: 사용자 데이터에 성별 저장)
        print(f"선택된 성별: {gender}")
        self.manager.current = 'height_weight_screen' # 메인 화면으로 이동

class HeightWeightScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.size_hint = (0.8, 0.7)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        title_label = Label(text="키 & 몸무게를 입력하세요", font_size='18sp', font_name="malgun.ttf", size_hint=(1, 0.15))
        self.layout.add_widget(title_label)

        stature_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), spacing=10)
        stature_icon = Image(source="images/키.png", size_hint=(0.15, 1))
        self.stature_input = TextInput(hint_text="키(cm)", multiline=False, size_hint=(0.85, 1), font_name="malgun.ttf")
        stature_layout.add_widget(stature_icon)
        stature_layout.add_widget(self.stature_input)
        self.layout.add_widget(stature_layout)

        weight_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), spacing=10)
        weight_icon = Image(source="images/몸무게.png", size_hint=(0.15, 1))
        self.weight_input = TextInput(hint_text="몸무게(kg)", multiline=False, size_hint=(0.85, 1), font_name="malgun.ttf")
        weight_layout.add_widget(weight_icon)
        weight_layout.add_widget(self.weight_input)
        self.layout.add_widget(weight_layout)

        self.layout.add_widget(Label(size_hint=(1, 0.3)))

        submit_button = Button(text="다음", size_hint=(1,0.08),  font_name="malgun.ttf")
        submit_button.bind(on_press=self.on_submit)
        self.layout.add_widget(submit_button)

        self.add_widget(self.layout)

    def on_submit(self, instance):
        height = self.height_input.text
        weight = self.weight_input.text
        if height.isdigit() and weight.isdigit():
            self.manager.current = 'main_screen'
        else:
            self.show_error_popup()

    def show_error_popup(self):
        popup = Popup(title="Error", content=Label(text="숫자를 입력하세요."), size_hint=(0.6, 0.4),  font_name="malgun.ttf")
        popup.open()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text="메인 화면입니다!", font_size='24sp')
        layout.add_widget(label)
        self.add_widget(layout)


class HealthTrackerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(GenderSelectionScreen(name='gender_selection')) # 성별 선택 화면 추가
        sm.add_widget(HeightWeightScreen(name='height_weight_screen')) #키,몸무게 화면 추가
        sm.add_widget(MainScreen(name='main_screen'))
        return sm

if __name__ == "__main__":
    HealthTrackerApp().run() 
