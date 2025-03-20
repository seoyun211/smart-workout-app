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
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line

kivy.require('2.0.0')

def get_korean_font():
    system = platform.system()
    if system == "Windows":
        return "C:/Windows/Fonts/malgun.ttf"
    elif system == "Darwin":
        return "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    return "NotoSansCJK-Regular.otf"

font_path = get_korean_font()
LabelBase.register(name="KoreanFont", fn_regular=font_path)

class BorderedBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.8, 0.8, 0.8, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            Line(rectangle=(self.x, self.y, self.width, self.height), width=1.5)
        self.bind(size=self.update_rect, pos=self.update_rect)
    
    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class HealthTrackingApp(App):
    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(FirstScreen(name="first_screen"))
        self.screen_manager.add_widget(EmptyScreen(name="empty_screen"))
        return self.screen_manager

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(1, 1, 1, 1)  # 흰색 (RGBA)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.data = {"sleep_hours": 0, "water_intake": 0, "steps": 0}
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # 수면 시간 박스
        sleep_box = BorderedBox(orientation='vertical', padding=10, spacing=10)
        sleep_label = Label(text="오늘의 수면 시간 (시간):", color=(0, 0, 0, 1),font_size=16, font_name="KoreanFont")
        self.sleep_slider = Slider(min=0, max=24, value=0, step=0.5)
        self.sleep_slider.bind(value=self.on_sleep_change)
        self.sleep_value_label = Label(text="0시간", color=(0, 0, 0, 1), font_size=14, font_name="KoreanFont")
        sleep_box.add_widget(sleep_label)
        sleep_box.add_widget(self.sleep_slider)
        sleep_box.add_widget(self.sleep_value_label)
        layout.add_widget(sleep_box)

        # 수분 섭취 박스
        water_box = BorderedBox(orientation='vertical', padding=10, spacing=10)
        water_label = Label(text="오늘의 수분 섭취량 (mL):" , color=(0, 0, 0, 1), font_size=16, font_name="KoreanFont")
        self.water_slider = Slider(min=0, max=5000, value=0, step=100)
        self.water_slider.bind(value=self.on_water_change)
        self.water_value_label = Label(text="0mL", color=(0, 0, 0, 1), font_size=14, font_name="KoreanFont")
        water_box.add_widget(water_label)
        water_box.add_widget(self.water_slider)
        water_box.add_widget(self.water_value_label)
        layout.add_widget(water_box)

        # 걸음 수 박스
        steps_box = BorderedBox(orientation='vertical', padding=10, spacing=10)
        steps_label = Label(text="걸음 수:", color=(0, 0, 0, 1),font_size=16, font_name="KoreanFont")
        self.steps_input = TextInput(hint_text="걸음 수 입력", multiline=False, font_name="KoreanFont", input_filter="int")
        steps_box.add_widget(steps_label)
        steps_box.add_widget(self.steps_input)
        layout.add_widget(steps_box)
        
        # 완료 버튼
        self.complete_button = Button(text="완료", font_name="KoreanFont", size_hint=(1, 0.3), height=50)
        self.complete_button.bind(on_press=self.show_popup)
        layout.add_widget(self.complete_button)
        
        self.add_widget(layout)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_sleep_change(self, slider, value):
        self.data["sleep_hours"] = value
        self.sleep_value_label.text = f"{int(value)}시간"

    def on_water_change(self, slider, value):
        self.data["water_intake"] = value
        self.water_value_label.text = f"{int(value)}mL"

    def show_popup(self, instance):
        self.data["steps"] = int(self.steps_input.text) if self.steps_input.text.isdigit() else 0
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text="데이터 입력이 완료되었습니다!", font_size=16, font_name="KoreanFont")
        content.add_widget(popup_label)
        next_button = Button(text="다음", font_name="KoreanFont")
        next_button.bind(on_press=self.go_to_empty_screen)
        content.add_widget(next_button)
        
        self.popup = Popup(title="완료", content=content, size_hint=(0.6, 0.3))
        self.popup.open()

    def go_to_empty_screen(self, instance):
        self.popup.dismiss()
        self.manager.get_screen('empty_screen').update_data(self.data)
        self.manager.current = 'empty_screen'

class EmptyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.empty_label = Label(text="", color=(0, 0, 0, 1),font_size=20, font_name="KoreanFont")
        self.layout.add_widget(self.empty_label)
        self.add_widget(self.layout)
    
    def update_data(self, data):
        self.empty_label.text = f"오늘 {data['sleep_hours']}시간 주무셨군요!\n오늘 {data['water_intake']}mL의 물을 마셨습니다.\n오늘 {data['steps']} 걸음 걸으셨네요!"

if __name__ == "__main__":
    HealthTrackingApp().run()
