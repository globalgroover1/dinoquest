
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

class DinoQuestApp(App):
    def build(self):
        # This forces the background to be DARK GRAY instead of white
        Window.clearcolor = (0.2, 0.2, 0.2, 1) 
        
        layout = BoxLayout(orientation='vertical')
        
        # This big label will tell us if the app is working
        label = Label(
            text="[b]DINO QUEST IS ALIVE![/b]\n\nIf you see this, the app works.\nWaiting for Dinosaur...",
            markup=True,
            font_size='24sp',
            halign='center'
        )
        
        layout.add_widget(label)
        return layout

if __name__ == '__main__':
    DinoQuestApp().run()
