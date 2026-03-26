from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
import random

class GameWorld(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (0.5, 0.8, 1, 1) # Sky Blue Background
        
        self.game_active = False
        self.score = 0
        self.speed = 8
        
        # 1. YOUR DINOSAUR
        self.dino = Image(
            source='dino.png', 
            size_hint=(0.2, 0.2), 
            pos_hint={'center_x': 0.2, 'center_y': 0.2}
        )
        self.add_widget(self.dino)
        
        # 2. UI TEXT (Start Screen & Score)
        self.ui_label = Label(
            text="[b]DINO QUEST[/b]\nTap to Start", 
            markup=True, font_size='40sp', 
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        self.add_widget(self.ui_label)
        
        self.score_label = Label(
            text="Score: 0", font_size='25sp', color=(0,0,0,1),
            pos_hint={'center_x': 0.5, 'center_y': 0.9}, opacity=0
        )
        self.add_widget(self.score_label)
        
        # Game Variables
        self.obstacles = []
        self.velocity = 0
        self.gravity = -0.8
        
        # Run the game at 60 Frames Per Second
        Clock.schedule_interval(self.update, 1.0/60.0)
        
    def on_touch_down(self, touch):
        # Start game or jump
        if not self.game_active:
            self.start_game()
        elif self.dino.pos_hint['center_y'] < 0.25: # Only jump if on the ground
            self.velocity = 15
            
    def start_game(self):
        self.game_active = True
        self.score = 0
        self.speed = 8
        self.ui_label.opacity = 0
        self.score_label.opacity = 1
        self.score_label.text = "Score: 0"
        
        # Clear old obstacles
        for obs in self.obstacles:
            self.remove_widget(obs)
        self.obstacles = []
        
        # Reset Dino
        self.dino.pos_hint['center_y'] = 0.2
        self.velocity = 0
        
    def update(self, dt):
        if not self.game_active: return
        
        # Physics (Gravity)
        self.velocity += self.gravity
        self.dino.pos_hint['center_y'] += (self.velocity / Window.height)
        
        # Hit the floor
        if self.dino.pos_hint['center_y'] <= 0.2:
            self.dino.pos_hint['center_y'] = 0.2
            self.velocity = 0
            
        # Spawn Obstacles randomly
        if random.random() < 0.015:
            self.spawn_obstacle()
            
        # Move obstacles and check collisions
        for obs in self.obstacles[:]:
            obs.pos_hint['center_x'] -= (self.speed / Window.width)
            
            # Crash Detection
            if self.dino.collide_widget(obs):
                # A tight hit-box so it feels fair
                if abs(self.dino.center_x - obs.center_x) < (self.dino.width * 0.4):
                    self.game_over()
                    
            # Passed the obstacle? Increase Score!
            if obs.pos_hint['center_x'] < -0.1:
                self.remove_widget(obs)
                self.obstacles.remove(obs)
                self.score += 1
                self.score_label.text = f"Score: {self.score}"
                
                # Level up speed every 5 points
                if self.score % 5 == 0:
                    self.speed += 1
                    
    def spawn_obstacle(self):
        # We use a solid Red Block so it never fails to load
        obs = Button(
            background_color=(0.8, 0.1, 0.1, 1), background_normal='', 
            size_hint=(0.08, 0.12), pos_hint={'center_x': 1.1, 'center_y': 0.18}
        )
        self.add_widget(obs)
        self.obstacles.append(obs)
        
    def game_over(self):
        self.game_active = False
        self.ui_label.text = f"CRASHED!\nFinal Score: {self.score}\nTap to Restart"
        self.ui_label.opacity = 1

class DinoQuestApp(App):
    def build(self):
        return GameWorld()

if __name__ == '__main__':
    DinoQuestApp().run()
