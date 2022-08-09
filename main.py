import kivy
from kivy.app import App
from kivy.uix.label import Label

import requests
import pdfplumber






class MyApp(App):
    def build(self):
        return Label(text="Hello World")

if __name__ == "__main__":
   MyApp().run()
