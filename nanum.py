from kivy.app import App
from kivy.uix.label import Label
from kivy.core.text import LabelBase

# 한글 폰트를 등록합니다
LabelBase.register(name="NanumGothic", fn_regular="NanumGothic.ttf")