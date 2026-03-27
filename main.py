from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse
import random

class UltimateGameWorld(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 1. Beautiful Sky Background
        Window.clearcolor = (0.3, 0.7, 0.9, 1) 
        
        self.state = 'MENU'
        self.score = 0
        self.high_score = 0
        self.game_speed = 10
        
        # 2. SCROLLING ENVIRONMENT (Clouds & Ground)
        with self.canvas.before:
            # Clouds
            Color(1, 1, 1, 0.8)
            self.cloud1 = Ellipse(size=(150, 60), pos=(Window.width * 0.2, Window.height * 0.7))
            self.cloud2 = Ellipse(size=(200, 80), pos=(Window.width * 0.7, Window.height * 0.8))
            
            # Solid Ground
            Color(0.15, 0.5, 0.15, 1) # Deep Grass Green
            self.ground = Rectangle(size=(3000, Window.height * 0.15), pos=(0,0))
            
            # Player Silhouette (Safety Net if images fail)
            self.player_color = Color(0.2, 0.8, 0.2, 1)
            self.player_shape = Ellipse(size=(90, 90))

        # 3. CHARACTER ROSTER
        # Names of the files you need to upload to GitHub
        self.roster = [
            {'file': 'dino.png', 'name': 'DINO', 'color': (0.2, 0.8, 0.2, 1)},
            {'file': 'hallie.png', 'name': 'HALLIE', 'color': (1, 0.4, 0.7, 1)},
            {'file': 'sky.png', 'name': 'SKY', 'color': (0.2, 0.6, 1, 1)}
        ]
        self.char_idx = 0
        
        # Player Image
        self.player_img = Image(
            source=self.roster[self.char_idx]['file'],
            size_hint=(0.25, 0.25), pos_hint={'center_x': 0.2, 'center_y': 0.25}
        )
        self.add_widget(self.player_img)
        
        # 4. EPIC UI
        self.title_label = Label(
            text=f"[b]DINO & FRIENDS[/b]\nSelected: {self.roster[self.char_idx]['name']}", 
            markup=True, font_size='45sp', halign='center',
            pos_hint={'center_x': 0.5, 'center_y': 0.7}
        )
        self.add_widget(self.title_label)
        
        self.instruct_label = Label(
            text="Tap RIGHT side to change Character\nTap LEFT side to START", 
            font_size='20sp', halign='center',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(self.instruct_label)
        
        self.score_label = Label(
            text="Score: 0 | High: 0", font_size='25sp', color=(0,0,0,1),
            pos_hint={'center_x': 0.5, 'center_y': 0.92}, opacity=0
        )
        self.add_widget(self.score_label)
        
        # 5. ADVANCED PHYSICS
        self.velocity = 0
        self.gravity = -1.0
        self.jump_power = 20
        self.jumps_left = 2
        
        self.obstacles = []
        Clock.schedule_interval(self.update, 1.0/60.0)

    def on_touch_down(self, touch):
        if self.state in ['MENU', 'GAMEOVER']:
            if touch.spos[0] > 0.5: # Tap Right -> Swap Character
                self.char_idx = (self.char_idx + 1) % len(self.roster)
                char_data = self.roster[self.char_idx]
                self.player_img.source = char_data['file']
                self.player_color.rgba = char_data['color']
                self.title_label.text = f"[b]DINO & FRIENDS[/b]\nSelected: {char_data['name']}"
            else: # Tap Left -> Start
                self.start_game()
        elif self.state == 'PLAYING':
            if self.jumps_left > 0: # DOUBLE JUMP
                self.velocity = self.jump_power
                self.jumps_left -= 1

    def start_game(self):
        self.state = 'PLAYING'
        self.score = 0
        self.game_speed = 10
        self.title_label.opacity = 0
        self.instruct_label.opacity = 0
        self.score_label.opacity = 1
        self.score_label.text = f"Score: 0 | High: {self.high_score}"
        
        for obs in self.obstacles:
            self.remove_widget(obs['img'])
        self.obstacles = []
        self.player_img.pos_hint['center_y'] = 0.25
        self.velocity = 0

    def update(self, dt):
        # Keep ground attached and shape behind player
        self.ground.size = (Window.width, Window.height * 0.15)
        self.player_shape.pos = (self.player_img.x + 30, self.player_img.y + 15)
        
        # Parallax Clouds
        self.cloud1.pos = (self.cloud1.pos[0] - 0.5, self.cloud1.pos[1])
        self.cloud2.pos = (self.cloud2.pos[0] - 0.8, self.cloud2.pos[1])
        if self.cloud1.pos[0] < -200: self.cloud1.pos = (Window.width, self.cloud1.pos[1])
        if self.cloud2.pos[0] < -200: self.cloud2.pos = (Window.width, self.cloud2.pos[1])

        if self.state != 'PLAYING': return

        # Physics
        self.velocity += self.gravity
        self.player_img.pos_hint['center_y'] += (self.velocity / Window.height)
        
        # Floor Hit
        if self.player_img.pos_hint['center_y'] <= 0.25:
            self.player_img.pos_hint['center_y'] = 0.25
            self.velocity = 0
            self.jumps_left = 2 # Reset Double Jump!

        # Advanced Enemy Spawning (Ground & Flying)
        if random.random() < 0.02:
            self.spawn_obstacle()

        # Update Obstacles
        for obs in self.obstacles[:]:
            # Flying enemies move faster
            move_speed = self.game_speed * 1.3 if obs['type'] == 'flying' else self.game_speed
            obs['img'].pos_hint['center_x'] -= (move_speed / Window.width)
            
            # Hitbox check
            if self.player_img.collide_widget(obs['img']):
                if abs(self.player_img.center_x - obs['img'].center_x) < (self.player_img.width * 0.35):
                    self.game_over()
                    
            # Score points
            if obs['img'].pos_hint['center_x'] < -0.1:
                self.remove_widget(obs['img'])
                self.obstacles.remove(obs)
                self.score += 1
                if self.score > self.high_score: self.high_score = self.score
                self.score_label.text = f"Score: {self.score} | High: {self.high_score}"
                
                if self.score % 5 == 0: self.game_speed += 1.2 # Level up speed

    def spawn_obstacle(self):
        # Randomly choose between a ground enemy and a flying enemy
        is_flying = random.choice([True, False])
        y_pos = 0.45 if is_flying else 0.22
        
        # Creates a dark red background block just in case 'enemy.png' fails to load
        obs_img = Image(
            source='enemy.png', size_hint=(0.12, 0.15), 
            pos_hint={'center_x': 1.1, 'center_y': y_pos}
        )
        
        with obs_img.canvas.before:
            Color(0.8, 0.1, 0.1, 1) # Red fallback
            Rectangle(pos=obs_img.pos, size=obs_img.size)
            
        self.add_widget(obs_img)
        self.obstacles.append({'img': obs_img, 'type': 'flying' if is_flying else 'ground'})

    def game_over(self):
        self.state = 'GAMEOVER'
        self.title_label.text = "[color=ff0000][b]WASTED[/b][/color]"
        self.title_label.opacity = 1
        self.instruct_label.text = f"Final Score: {self.score}\nTap LEFT to restart\nTap RIGHT to change character"
        self.instruct_label.opacity = 1

class UltimateApp(App):
    def build(self):
        return UltimateGameWorld()

if __name__ == '__main__':
    UltimateApp().run()
