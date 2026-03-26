import os
from kivy.app import App
from kivy.uix.image import Image
from kivy.utils import platform

# --- AUTOMATIC FILE FINDER ---
# This helper finds your images even if the letters are wrong
def get_asset(filename):
    if platform == 'android':
        # On Android, we just return the name and hope the requirements fixed it
        return filename.lower()
    return filename

class DinoQuestApp(App):
    def build(self):
        # We use a simple image first to make sure it opens!
        # REPLACE 'dino.png' with your actual background or player name
        try:
            return Image(source=get_asset('dino.png'))
        except:
            from kivy.uix.label import Label
            return Label(text="Game Started! (Image Missing)")

if __name__ == '__main__':
    DinoQuestApp().run()import os
from kivy.app import App
from kivy.uix.image import Image
from kivy.utils import platform

# --- AUTOMATIC FILE FINDER ---
# This helper finds your images even if the letters are wrong
def get_asset(filename):
    if platform == 'android':
        # On Android, we just return the name and hope the requirements fixed it
        return filename.lower()
    return filename

class DinoQuestApp(App):
    def build(self):
        # We use a simple image first to make sure it opens!
        # REPLACE 'dino.png' with your actual background or player name
        try:
            return Image(source=get_asset('dino.png'))
        except:
            from kivy.uix.label import Label
            return Label(text="Game Started! (Image Missing)")

if __name__ == '__main__':
    DinoQuestApp().run()
