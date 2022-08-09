import kivy
from kivy.app import App
from kivy.uix.label import Label

import os
import requests
import pdfplumber
import re





class MyApp(App):
    def build(self):
        return Label(text="Hello World")

if __name__ == "__main__":
   MyApp().run()
