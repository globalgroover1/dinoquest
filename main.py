
            from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.animation import Animation

class DinoQuestApp(App):
    def build(self):
        # Sky Blue Background
        Window.clearcolor = (0.5, 0.8, 1, 1) 
        layout = FloatLayout()
        
        # An invisible button over the whole screen to detect your taps
        tap_screen = Button(background_color=(0,0,0,0), size_hint=(1, 1))
        tap_screen.bind(on_press=self.jump)
        layout.add_widget(tap_screen)

        # The "Dinosaur" - A Yellow Box that CANNOT fail to load
        self.dino = Button(
            text="[b]DINO[/b]",
            markup=True,
            color=(0, 0, 0, 1), # Black text
            background_normal='',
            background_color=(1, 0.8, 0, 1), # Bright Yellow Box
            size_hint=(0.2, 0.2), 
            pos_hint={'center_x': 0.5, 'center_y': 0.2} # Starts near the bottom
        )
        layout.add_widget(self.dino)
        
        return layout

    def jump(self, instance):
        # When you tap, the Yellow Box goes up, then comes back down
        anim = Animation(pos_hint={'center_x': 0.5, 'center_y': 0.6}, duration=0.3) + \
               Animation(pos_hint={'center_x': 0.5, 'center_y': 0.2}, duration=0.3)
        anim.start(self.dino)

if __name__ == '__main__':
    DinoQuestApp().run()
