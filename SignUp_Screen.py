import bcrypt
import pickle
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

# 사용자 데이터를 저장할 파일 경로
USER_FILE = "users.pkl"

# 사용자 데이터를 파일에서 불러오는 함수
def load_users():
    try:
        with open(USER_FILE, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return {}

# 사용자 데이터를 파일에 저장하는 함수
def save_users(users):
    with open(USER_FILE, "wb") as file:
        pickle.dump(users, file)

# 비밀번호를 해싱하는 함수
def hash_password(password):
    salt = bcrypt.gensalt()  # Salt 생성
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)  # 비밀번호 해싱
    return hashed

# 회원가입 화면 클래스
class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.size_hint = (0.8, 0.6)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # 화면에 제목 추가
        title_label = Label(text="회원가입", font_size='24sp', font_name="malgun.ttf")
        self.layout.add_widget(title_label)

        # 이메일 입력 필드 추가
        self.email_input = TextInput(hint_text="Email ID", multiline=False, size_hint=(1, 0.2))
        self.layout.add_widget(self.email_input)

        # 비밀번호 입력 필드 추가
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint=(1, 0.2))
        self.layout.add_widget(self.password_input)

        # 비밀번호 확인 필드 추가
        self.confirm_password_input = TextInput(hint_text="Confirm Password", multiline=False, password=True, size_hint=(1, 0.2))
        self.layout.add_widget(self.confirm_password_input)

        # 회원가입 버튼 추가
        sign_up_button = Button(text="회원가입", size_hint=(1, 0.2), background_color=(0, 0, 1, 1), font_name="malgun.ttf")
        sign_up_button.bind(on_press=self.on_sign_up)
        self.layout.add_widget(sign_up_button)

        # 뒤로가기 버튼 추가
        back_button = Button(text="뒤로가기", size_hint=(1, 0.2), background_color=(1, 0, 0, 1), font_name="malgun.ttf")
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
            self.show_popup("Error", "모든 필드를 입력해주세요.",)
            return
        
        # 비밀번호 일치 체크
        if password != confirm_password:
            self.show_popup("Error", "비밀번호가 일치하지 않습니다.")
            return

        # 이메일이 이미 존재하는지 체크
        if email in self.users:
            self.show_popup("Error", "이미 가입된 이메일입니다.")
            return

        # 비밀번호 해싱 후 사용자 추가
        self.users[email] = hash_password(password)
        save_users(self.users)  # 사용자 데이터 파일에 저장

        # 성공 팝업 띄우기
        self.show_popup("Success", "회원가입이 완료되었습니다!")
        
        # 팝업 창이 닫히는 것과 동시에 로그인 화면으로 전환
        self.manager.current = 'login_screen'

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_label = Label(text=message, font_size='18sp', font_name="malgun.ttf")
        close_button = Button(text="확인", size_hint=(1, 0.2), font_name="malgun.ttf")
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'login_screen'  # 뒤로가기 버튼 클릭 시 로그인 화면으로 이동
