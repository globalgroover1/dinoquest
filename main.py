from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
import random

class DinoQuestGame(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_active = False
        self.score = 0
        self.speed = 10
        
        # 1. Background / Sky
        Window.clearcolor = (0.5, 0.8, 1, 1)
        
        # 2. The Dino (Image Support)
        # Fallback: If dino.png isn't there, Kivy shows a white box, 
        # but our code won't crash.
        self.dino = Image(
            source='dino.png',
            size_hint=(0.2, 0.2),
            pos_hint={'center_x': 0.2, 'center_y': 0.2}
        )
        self.add_widget(self.dino)
        
        # 3. UI Labels
        self.info_label = Label(
            text="[b]DINO QUEST[/b]\nTap to Start",
            markup=True, font_size='40sp', color=(1,1,1,1),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        self.add_widget(self.info_label)
        
        self.score_label = Label(
            text="Score: 0", font_size='25sp',
            pos_hint={'center_x': 0.5, 'center_y': 0.9}, opacity=0
        )
        self.add_widget(self.score_label)

        # Game State Variables
        self.velocity = 0
        self.gravity = -0.9
        self.jump_height = 18
        self.obstacles = []
        
        # Game Loop
        Clock.schedule_interval(self.update, 1.0/60.0)

    def on_touch_down(self, touch):
        if not self.game_active:
            self.start_game()
        else:
            # Only jump if we are near the ground
            if self.dino.pos_hint['center_y'] < 0.25:
                self.velocity = self.jump_height

    def start_game(self):
        self.game_active = True
        self.score = 0
        self.speed = 10
        self.info_label.opacity = 0
        self.score_label.opacity = 1
        self.score_label.text = "Score: 0"
        self.dino.pos_hint = {'center_x': 0.2, 'center_y': 0.2}
        self.velocity = 0

    def update(self, dt):
        if not self.game_active:
            return

        # Dino Physics (Gravity)
        self.velocity += self.gravity
        new_y = self.dino.pos_hint['center_y'] + (self.velocity / Window.height)
        
        if new_y <= 0.2:
            new_y = 0.2
            self.velocity = 0
        self.dino.pos_hint['center_y'] = new_y

        # Obstacle Management
        if random.random() < 0.015: # Random chance to spawn cactus
            self.spawn_obstacle()

        for obs in self.obstacles[:]:
            obs.pos_hint['center_x'] -= (self.speed / Window.width)
            
            # Check Collision
            if self.dino.collide_widget(obs):
                self.game_over()

            # Cleanup and Scoring
            if obs.pos_hint['center_x'] < -0.1:
                self.remove_widget(obs)
                self.obstacles.remove(obs)
                self.score += 1
                self.score_label.text = f"Score: {self.score}"
                # Increase speed as score goes up
                if self.score % 5 == 0:
                    self.speed += 0.5

    def spawn_obstacle(self):
        # We use a Label as a 'Cactus' placeholder so it never fails to load
        obs = Label(
            text="🌵", font_size='50sp',
            size_hint=(0.1, 0.1),
            pos_hint={'center_x': 1.1, 'center_y': 0.2}
        )
        self.add_widget(obs)
        self.obstacles.append(obs)

    def game_over(self):
        self.game_active = False
        self.info_label.text = f"CRASHED!\nScore: {self.score}\nTap to Try Again"
        self.info_label.opacity = 1
        for obs in self.obstacles:
            self.remove_widget(obs)
        self.obstacles = []

class DinoQuestApp(App):
    def build(self):
        return DinoQuestGame()

if __name__ == '__main__':
    DinoQuestApp().run()
