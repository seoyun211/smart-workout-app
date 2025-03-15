class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.size_hint = (0.8, 0.6)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.layout.add_widget(Label(text="회원가입", font_size='24sp'))

        self.email_input = TextInput(hint_text="Email ID", multiline=False, size_hint=(1, 0.2))
        self.layout.add_widget(self.email_input)

        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint=(1, 0.2))
        self.layout.add_widget(self.password_input)

        self.confirm_password_input = TextInput(hint_text="Confirm Password", multiline=False, password=True, size_hint=(1, 0.2))
        self.layout.add_widget(self.confirm_password_input)

        self.sign_up_button = Button(text="회원가입", size_hint=(1, 0.2), background_color=(0, 0, 1, 1))
        self.sign_up_button.bind(on_press=self.on_sign_up)
        self.layout.add_widget(self.sign_up_button)

        self.back_button = Button(text="뒤로가기", size_hint=(1, 0.2), background_color=(1, 0, 0, 1))
        self.back_button.bind(on_press=self.go_back)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def on_sign_up(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        confirm_password = self.confirm_password_input.text.strip()

        if not email or not password or not confirm_password:
            self.show_popup("Error", "모든 필드를 입력해주세요.")
            return
        
        if password != confirm_password:
            self.show_popup("Error", "비밀번호가 일치하지 않습니다.")
            return

        if email in users:
            self.show_popup("Error", "이미 가입된 이메일입니다.")
            return

        # 비밀번호 해싱 후 저장
        users[email] = hash_password(password)
        save_users(users)

        self.show_popup("Success", "회원가입이 완료되었습니다!")
        self.manager.current = 'login_screen'

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        popup_label = Label(text=message, font_size='18sp')
        close_button = Button(text="확인", size_hint=(1, 0.2))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'login_screen'
