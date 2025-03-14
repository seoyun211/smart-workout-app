from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.graphics import Color
from kivy.graphics import Rectangle

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # 전체 배경색 설정
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.size_hint = (0.8, 0.6)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # 이미지 추가 (중앙 큰 이미지)
        image = Image(source="images/Login.png", size_hint=(1, 0.3))
        self.layout.add_widget(image)

        # 이메일 입력
        email_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        email_icon = Image(source="images/email.png", size_hint=(0.15, 1))
        self.email_input = TextInput(hint_text="Email ID", multiline=False, size_hint=(0.85, 1))
        email_layout.add_widget(email_icon)
        email_layout.add_widget(self.email_input)
        self.layout.add_widget(email_layout)

        # 비밀번호 입력
        password_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        password_icon = Image(source="images/password.png", size_hint=(0.15, 1))
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint=(0.85, 1))
        password_layout.add_widget(password_icon)
        password_layout.add_widget(self.password_input)
        self.layout.add_widget(password_layout)

        # "Forgot Password?" 버튼
        forgot_button = Button(text="Forgot Password?", size_hint=(1, 0.1), background_color=(0, 0, 0, 0), color=(0, 0, 1, 1))
        self.layout.add_widget(forgot_button)

        # 로그인 버튼
        self.login_button = Button(text="LOGIN", size_hint=(1, 0.2), background_color=(0, 0, 0, 1))
        self.login_button.bind(on_press=self.on_login)
        self.layout.add_widget(self.login_button)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_login(self, instance):
        # 로그인 로직 (임시로 항상 성공 처리)
        self.manager.current = 'home'


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 메인 레이아웃
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # 버튼 레이아웃
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=20)

        # "맞춤 운동" 버튼
        custom_exercise_button = Button(text='a', size_hint=(None, 1), width=200)
        custom_exercise_button.bind(on_press=self.show_custom_exercise)
        button_layout.add_widget(custom_exercise_button)

        # "운동 추적" 버튼
        exercise_tracking_button = Button(text='b', size_hint=(None, 1), width=200)
        exercise_tracking_button.bind(on_press=self.show_exercise_tracking)
        button_layout.add_widget(exercise_tracking_button)

        # 버튼 레이아웃을 화면에 추가
        self.layout.add_widget(button_layout)

        # 콘텐츠를 추가할 레이아웃
        self.content_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9))
        self.layout.add_widget(self.content_layout)

        # 초기 콘텐츠
        self.show_custom_exercise(None)

        self.add_widget(self.layout)

    def show_custom_exercise(self, instance):
        # 기존 탭 대신 맞춤 운동 화면을 표시
        self.content_layout.clear_widgets()
        self.content_layout.add_widget(Label(text="맞춤 운동 화면"))

        # "aa" 버튼 추가
        aa_button = Button(text="aa", size_hint=(None, 0.1), height=50)
        aa_button.bind(on_press=self.show_aa_tab)
        self.content_layout.add_widget(aa_button)

        # "aaa" 버튼 추가
        aaa_button = Button(text="aaa", size_hint=(None, 0.1), height=50)
        aaa_button.bind(on_press=self.show_aaa_tab)
        self.content_layout.add_widget(aaa_button)

    def show_exercise_tracking(self, instance):
        # 운동 추적 화면을 표시
        self.content_layout.clear_widgets()
        self.content_layout.add_widget(Label(text="운동 추적 화면"))

    def show_aa_tab(self, instance):
        self.content_layout.clear_widgets()
        self.content_layout.add_widget(Label(text="This is the aa tab"))

    def show_aaa_tab(self, instance):
        self.content_layout.clear_widgets()
        self.content_layout.add_widget(Label(text="This is the aaa tab"))


class HealthTrackerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        return sm

if __name__ == "__main__":
    HealthTrackerApp().run()
