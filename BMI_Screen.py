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
        
        self.bmi_label = Label(text=f'당신의 BMI: {self.calculate_bmi():.2f}', font_size='24sp')
        self.result_label = Label(text=f'분류: {self.get_bmi_category()}', font_size='28sp', bold=True)
        
        back_button = Button(text='뒤로 가기', on_press=self.go_back)
        
        self.layout.add_widget(self.bmi_label)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(back_button)
        
        self.add_widget(self.layout)

    def set_user_data(self, height, weight):
        """ 사용자의 키와 몸무게 값을 설정하고 BMI 정보를 업데이트 """
        self.height = height
        self.weight = weight
        self.update_bmi_info()

    def update_bmi_info(self):
        """ BMI 값과 분류를 업데이트 """
        if self.height > 0 and self.weight > 0:
            self.bmi_label.text = f'당신의 BMI: {self.calculate_bmi():.2f}'
            self.result_label.text = f'분류: {self.get_bmi_category()}'
        else:
            self.bmi_label.text = "입력된 값이 올바르지 않습니다."
            self.result_label.text = ""

    def calculate_bmi(self):
        if self.height > 0:
            return self.weight / (self.height / 100) ** 2
        return 0  # 잘못된 값이 들어왔을 경우 0 반환
    
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
    
    def go_back(self, instance):
        self.manager.current = 'height_weight_screen'

