#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import mainthread, Clock

gui = '''
Root:
    orientation: 'vertical'

    arena: arena
    control_button: control_button

    Arena:
        id: arena

    Button
        id: control_button
        size_hint_y: None
        height: dp(50)
        text: 'move'


<Arena@FloatLayout>:
    player: player

    Button:
        id: player
        pos: 150, 300
        text: 'elf warrior\\nlevel 1'
        size_hint: None, None
        size: 100, 100
'''


class Root(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        @mainthread
        def job():
            self.control_button.bind(on_press=self._on_press)
            self.control_button.bind(on_release=self._on_release)

        job()

    def _on_press(self, button):
        self.arena.start_movement()

    def _on_release(self, button):
        self.arena.stop_movement()


class Arena(FloatLayout):

    def start_movement(self):
        Clock.schedule_interval(self._move_right, 0.01)

    def stop_movement(self):
        Clock.unschedule(self._move_right)

    def _move_right(self, dt):
        self.player.x += 1


class Test(App):

    def build(self):
        return Builder.load_string(gui)


Test().run()
