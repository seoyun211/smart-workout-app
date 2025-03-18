from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

class BMIScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = 0
        self.weight = 0

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        bmi_label = Label(text=f'당신의 BMI: {self.calculate_bmi():.2f}', font_size='24sp')
        result_label = Label(text=f'분류: {self.get_bmi_category()}', font_size='28sp', bold=True)
        
        back_button = Button(text='뒤로 가기', on_press=self.go_back)
        
        self.layout.add_widget(bmi_label)
        self.layout.add_widget(result_label)
        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)

    def calculate_bmi(self):
        if self.hight > 0:
            return self.weight / (self.height / 100) ** 2
    
    def get_bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return '저체중'
        elif 18.5 <= bmi < 25:
            return '정상체중'
        elif 25<= bmi < 30:
            return '과체중'
        else:
            return '비만'
    def go_to_exercise_recommendation(self, instance):
        """ 운동 추천 화면으로 이동하는 함수 ✅ """
        if self.manager:
            self.manager.current = "exercise_screen"

    def go_back(self, instance):
        self.manager.current = 'height_weight_screen'

