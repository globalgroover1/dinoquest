
import os
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.utils import platform

class DinoQuestApp(App):
    def build(self):
        layout = FloatLayout()
        
        # This is the "Safety Net"
        # It tries to load your image, but won't crash if it fails
        try:
            # IMPORTANT: Ensure your file is named 'dino.png' (all lowercase) in GitHub
            img = Image(source='dino.png', allow_stretch=True, keep_ratio=True)
            layout.add_widget(img)
        except Exception as e:
            # If the image fails, this shows text so the app stays open
            error_label = Label(text="Dino Quest Started!\n(Check image filenames)", halign="center")
            layout.add_widget(error_label)
            
        return layout

if __name__ == '__main__':
    DinoQuestApp().run()
