from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color
from kivy.graphics import Rectangle

# User data storage (this can be replaced with a more permanent solution)
users = {}

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Set background color
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.size_hint = (0.8, 0.6)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Add image (central large image)
        image = Image(source="images/Login.png", size_hint=(1, 0.3))
        self.layout.add_widget(image)

        # Email input
        email_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        email_icon = Image(source="images/email.png", size_hint=(0.15, 1))
        self.email_input = TextInput(hint_text="Email ID", multiline=False, size_hint=(0.85, 1))
        email_layout.add_widget(email_icon)
        email_layout.add_widget(self.email_input)
        self.layout.add_widget(email_layout)

        # Password input
        password_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        password_icon = Image(source="images/password.png", size_hint=(0.15, 1))
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint=(0.85, 1))
        password_layout.add_widget(password_icon)
        password_layout.add_widget(self.password_input)
        self.layout.add_widget(password_layout)

        # "Forgot Password?" button
        forgot_button = Button(text="Forgot Password?", size_hint=(1, 0.1), background_color=(0, 0, 0, 0), color=(0, 0, 1, 1))
        self.layout.add_widget(forgot_button)

        # Login button
        self.login_button = Button(text="LOGIN", size_hint=(1, 0.2), background_color=(0, 0, 0, 1))
        self.login_button.bind(on_press=self.on_login)
        self.layout.add_widget(self.login_button)

        # Sign Up button
        sign_up_button = Button(text="Sign Up", size_hint=(1, 0.1), background_color=(0, 0, 0, 1), color=(0, 0, 1, 1))
        sign_up_button.bind(on_press=self.on_sign_up)
        self.layout.add_widget(sign_up_button)

        self.add_widget(self.layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_login(self, instance):
        # Login logic (simple check if the user exists)
        email = self.email_input.text
        password = self.password_input.text
        if email in users and users[email] == password:
            self.manager.current = 'main_screen'  # Success, go to main screen
        else:
            print("Invalid login credentials")

    def on_sign_up(self, instance):
        # Switch to the SignUpScreen
        self.manager.current = 'sign_up_screen'


class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.layout.size_hint = (0.8, 0.6)
        self.layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Add image
        image = Image(source="images/Login.png", size_hint=(1, 0.3))
        self.layout.add_widget(image)

        # Name input
        self.name_input = TextInput(hint_text="Full Name", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.name_input)

        # Email input
        self.email_input = TextInput(hint_text="Email ID", multiline=False, size_hint=(1, 0.1))
        self.layout.add_widget(self.email_input)

        # Password input
        self.password_input = TextInput(hint_text="Password", multiline=False, password=True, size_hint=(1, 0.1))
        self.layout.add_widget(self.password_input)

        # Confirm password input
        self.confirm_password_input = TextInput(hint_text="Confirm Password", multiline=False, password=True, size_hint=(1, 0.1))
        self.layout.add_widget(self.confirm_password_input)

        # Sign Up button
        sign_up_button = Button(text="SIGN UP", size_hint=(1, 0.2), background_color=(0, 0, 0, 1))
        sign_up_button.bind(on_press=self.on_sign_up)
        self.layout.add_widget(sign_up_button)

        # Back to Login button
        back_button = Button(text="Back to Login", size_hint=(1, 0.1), background_color=(0, 0, 0, 1))
        back_button.bind(on_press=self.on_back_to_login)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def on_sign_up(self, instance):
        # Sign up logic (check if passwords match and email is unique)
        email = self.email_input.text
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text

        if email in users:
            print("Email already exists")
        elif password != confirm_password:
            print("Passwords do not match")
        else:
            # Save user data
            users[email] = password
            print(f"User {email} registered successfully!")
            self.manager.current = 'login'  # Switch back to login screen

    def on_back_to_login(self, instance):
        # Go back to the login screen
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


class ExerciseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='horizontal', padding=20, spacing=10)
        left_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 1), spacing=20)

        weight_beginners_button = Button(text='Weight for Beginners', size_hint=(None, 0.2), height=50)
        left_layout.add_widget(weight_beginners_button)

        right_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 1), spacing=20)
        cardio_beginners_button = Button(text='Cardio for Beginners', size_hint=(None, 0.2), height=50)
        right_layout.add_widget(cardio_beginners_button)

        self.layout.add_widget(left_layout)
        self.layout.add_widget(right_layout)

        need_help_button = Button(text="Need Help? (AI)", size_hint=(None, 0.1), height=50)
        need_help_button.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.layout.add_widget(need_help_button)

        self.add_widget(self.layout)


class HealthTrackerApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(SignUpScreen(name='sign_up_screen'))  # Add the SignUpScreen
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(ExerciseScreen(name='exercise_screen'))
        return sm


if __name__ == "__main__":
    HealthTrackerApp().run()
#코드끝끝