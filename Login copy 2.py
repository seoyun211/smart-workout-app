from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
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
        self.manager.current = 'main_screen'  # 로그인 성공 시 'main_screen'으로 화면 전환


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 빈 화면과 4개의 버튼 추가
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # 콘텐츠를 추가할 레이아웃
        self.content_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.9))
        self.layout.add_widget(self.content_layout)

        # 4개의 버튼 추가 (하단에 배치)
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=20)

        # 운동 버튼
        exercise_button = Button(text='Exercise', size_hint=(None, 1), width=200)
        exercise_button.bind(on_press=self.on_exercise_button_pressed)
        button_layout.add_widget(exercise_button)

        # 분석 버튼
        analysis_button = Button(text='Analysis', size_hint=(None, 1), width=200)
        button_layout.add_widget(analysis_button)

        # 커뮤니티 버튼
        community_button = Button(text='Community', size_hint=(None, 1), width=200)
        button_layout.add_widget(community_button)

        # 마이페이지 버튼
        mypage_button = Button(text='MyPage', size_hint=(None, 1), width=200)
        button_layout.add_widget(mypage_button)

        # 버튼을 레이아웃에 추가
        self.layout.add_widget(button_layout)

        self.add_widget(self.layout)

    def on_exercise_button_pressed(self, instance):
        # Exercise 버튼을 눌렀을 때 새로운 화면으로 전환
        self.manager.current = 'exercise_screen'


class ExerciseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 빈 화면과 중앙에 버튼들 배치
        self.layout = BoxLayout(orientation='horizontal', padding=20, spacing=10)

        # 좌측 레이아웃 (Weight 관련)
        left_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 1), spacing=20)

        # weight for beginners 버튼
        weight_beginners_button = Button(text='Weight for Beginners', size_hint=(None, 0.2), height=50)
        left_layout.add_widget(weight_beginners_button)

        # weight for intermediate 버튼
        weight_intermediate_button = Button(text='Weight for Intermediate', size_hint=(None, 0.2), height=50)
        left_layout.add_widget(weight_intermediate_button)

        # weight for experts 버튼
        weight_experts_button = Button(text='Weight for Experts', size_hint=(None, 0.2), height=50)
        left_layout.add_widget(weight_experts_button)

        # 우측 레이아웃 (Cardio 관련)
        right_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 1), spacing=20)

        # cardio for beginners 버튼
        cardio_beginners_button = Button(text='Cardio for Beginners', size_hint=(None, 0.2), height=50)
        right_layout.add_widget(cardio_beginners_button)

        # cardio for intermediate 버튼
        cardio_intermediate_button = Button(text='Cardio for Intermediate', size_hint=(None, 0.2), height=50)
        right_layout.add_widget(cardio_intermediate_button)

        # cardio for experts 버튼
        cardio_experts_button = Button(text='Cardio for Experts', size_hint=(None, 0.2), height=50)
        right_layout.add_widget(cardio_experts_button)

        # 좌측 레이아웃과 우측 레이아웃을 메인 레이아웃에 추가
        self.layout.add_widget(left_layout)
        self.layout.add_widget(right_layout)

        # 중앙에 Need Help 버튼 추가 (위치 변경)
        need_help_button = Button(text="Need Help? (AI)", size_hint=(None, 0.1), height=50)
        need_help_button.pos_hint = {"center_x": 0.5, "center_y": 0.5}  # 버튼을 화면 중앙에 배치
        self.layout.add_widget(need_help_button)

        self.add_widget(self.layout)


class HealthTrackerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))  # 로그인 화면
        sm.add_widget(MainScreen(name='main_screen'))  # 로그인 후 메인 화면
        sm.add_widget(ExerciseScreen(name='exercise_screen'))  # Exercise 화면
        return sm


if __name__ == "__main__":
    HealthTrackerApp().run()
