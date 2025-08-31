#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.label import Label

class TestApp(App):
    def build(self):
        return Label(text='¡DaniStore funciona!\n\nLa aplicación está lista\npara convertir a APK')

if __name__ == '__main__':
    TestApp().run()
