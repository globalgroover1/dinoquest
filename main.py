from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window

class DinoQuestApp(App):
    def build(self):
        # Sky Blue Background
        Window.clearcolor = (0.5, 0.8, 1, 1) 
        
        layout = FloatLayout()
        
        try:
            # This looks for your file named 'dino.png'
            dino = Image(
                source='dino.png', 
                size_hint=(0.5, 0.5), 
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            layout.add_widget(dino)
        except:
            # If the image fails, it shows this text instead of crashing
            layout.add_widget(Label(text="App works, but dino.png not found!"))
            
        return layout

if __name__ == '__main__':
    DinoQuestApp().run()
