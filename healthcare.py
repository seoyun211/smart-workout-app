import kivy
import platform
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen

kivy.require('2.0.0')  # Kivy 버전 확인

# 시스템에 따라 폰트 경로를 다르게 설정
def get_korean_font():
    system = platform.system()
    if system == "Windows":
        return "C:/Windows/Fonts/malgun.ttf"
    elif system == "Darwin":
        return "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    return "NotoSansCJK-Regular.otf"  # 기본적으로 사용할 폰트

# 폰트 등록
font_path = get_korean_font()
LabelBase.register(name="KoreanFont", fn_regular=font_path)

class HealthTrackingApp(App):

    def build(self):
        # 화면 관리 객체(ScreenManager) 생성
        self.screen_manager = ScreenManager()

        # 첫 번째 화면(건강 추적 화면) 추가
        self.first_screen = FirstScreen(name="first_screen")
        self.screen_manager.add_widget(self.first_screen)

        # 두 번째 화면(빈 화면) 추가
        self.empty_screen = EmptyScreen(name="empty_screen")
        self.screen_manager.add_widget(self.empty_screen)

        return self.screen_manager

class FirstScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data = {
            "steps": 0,
            "calories_burned": 0,
            "sleep_hours": 0,
            "weight": 0,
            "water_intake": 0,
            "heart_rate": 0
        }

        # 레이아웃 설정
        layout = BoxLayout(orientation='vertical')

        # 제목 레이블 (폰트 추가)
        title_label = Label(text="건강 추적", font_size=24, font_name="KoreanFont", size_hint=(1, 0.1))
        layout.add_widget(title_label)

               # 수면 추적
        sleep_label = Label(text="오늘의 수면 시간 (시간):", font_size=18, font_name="KoreanFont")
        layout.add_widget(sleep_label)
        self.sleep_slider = Slider(min=0, max=24, value=0, step=0.5)
        self.sleep_slider.bind(value=self.on_sleep_change)
        layout.add_widget(self.sleep_slider)
        
        # 수면 시간 값 표시 레이블
        self.sleep_value_label = Label(text="0시간", font_size=16, font_name="KoreanFont")
        layout.add_widget(self.sleep_value_label)

        # 수분 섭취 추적
        water_label = Label(text="오늘의 수분 섭취량 (밀리리터):", font_size=18, font_name="KoreanFont")
        layout.add_widget(water_label)
        self.water_slider = Slider(min=0, max=5000, value=0, step=0.1)
        self.water_slider.bind(value=self.on_water_change)
        layout.add_widget(self.water_slider)

        # 수분 섭취량 값 표시 레이블
        self.water_value_label = Label(text="0mL", font_size=16, font_name="KoreanFont")
        layout.add_widget(self.water_value_label)

        # 걸음 수 입력
        heart_rate_label = Label(text="걸음 수:", font_size=18, font_name="KoreanFont")
        layout.add_widget(heart_rate_label)

        # 자연수만 입력 받기 위한 TextInput
        self.heart_rate_input = TextInput(hint_text="걸음 수 입력", multiline=False, font_name="KoreanFont", input_filter="int")
        layout.add_widget(self.heart_rate_input)

        # 완료 버튼
        self.complete_button = Button(text="완료", on_press=self.show_popup, font_name="KoreanFont", size_hint=(1, 0.1))
        layout.add_widget(self.complete_button)

        self.add_widget(layout)

    def on_sleep_change(self, slider, value):
        self.data["sleep_hours"] = value
        print(f"수면 시간: {value}시간")

    def on_water_change(self, slider, value):
        self.data["water_intake"] = value
        print(f"수분 섭취량: {value}리터")

    def show_popup(self, instance):
        # 완료 버튼을 누르면 팝업창 띄우기
        content = BoxLayout(orientation='vertical')
        popup_label = Label(text="데이터 입력이 완료되었습니다!", font_size=18, font_name="KoreanFont")
        content.add_widget(popup_label)
        next_button = Button(text="다음", on_press=self.go_to_empty_screen, font_name="KoreanFont")
        content.add_widget(next_button)

        self.popup = Popup(title="완료", content=content, size_hint=(0.7, 0.3))
        self.popup.open()

    def go_to_empty_screen(self, instance):
        # '다음' 버튼을 누르면 빈 화면으로 전환
        self.popup.dismiss()  # 팝업 닫기
        # 'empty_screen' 화면으로 전환하고 데이터를 전달
        self.manager.get_screen('empty_screen').update_data(self.data) 
        self.manager.current = 'empty_screen'  # 'empty_screen' 화면으로 전환

class EmptyScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.empty_label = Label(text="", font_size=24, font_name="KoreanFont", size_hint=(1, 0.5))
        self.layout.add_widget(self.empty_label)
        self.add_widget(self.layout)

    def update_data(self, data):
        # 수면 시간, 수분 섭취량, 걸음 수 데이터로 텍스트 업데이트
        sleep_message = f"오늘 {data['sleep_hours']}시간만큼 주무셨군요!\n권장 수면시간은 8시간입니다."
        if data['sleep_hours'] > 8:
            sleep_message += "\n조금 덜 주무시는건 어떨까요?"
        elif data['sleep_hours'] < 8:
            sleep_message += "\n조금 더 주무시는건 어떨까요?"
        
        water_message = f"오늘 {data['water_intake']}mL 만큼 섭취하셨군요!\n권장 수분 섭취량은 대략 2L입니다."
        if data['water_intake'] > 2000:
            water_message += "\n조금 덜 마셔보세요!"
        elif data['water_intake'] < 2000:
            water_message += "\n조금 더 마셔보세요!"
        
        steps_message = f"오늘 {data['steps']} 만큼 걸으셨군요!\n주기적인 걸음 운동은 건강의 지름길입니다."

        # 텍스트 업데이트
        self.empty_label.text = f"{sleep_message}\n\n{water_message}\n\n{steps_message}"

if __name__ == "__main__":
    HealthTrackingApp().run() 