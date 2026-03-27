from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse, PushMatrix, PopMatrix, Scale
import random

# ==========================================
# ⚙️ MASTER GAME SETTINGS (You can change these!)
# ==========================================
FLIP_CHARACTER = True  # True spins your character to face right!
STARTING_SPEED = 6.0   # Slower, fairer start (Was 10.0)
GRAVITY = -0.55        # Floaty, easy-to-control gravity (Was -1.2)
JUMP_POWER = 13.0      # Smooth, controlled jump
# ==========================================

class PlatinumGameWorld(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = (0.4, 0.8, 1.0, 1) # Bright Sky Blue
        
        self.state = 'MENU'
        self.score = 0
        self.high_score = 0
        self.game_speed = STARTING_SPEED
        
        # 1. SCROLLING WORLD (Sun, Mountains, Clouds, Ground)
        with self.canvas.before:
            # The Sun
            Color(1, 0.9, 0.2, 1)
            Ellipse(size=(120, 120), pos=(Window.width * 0.8, Window.height * 0.75))
            
            # Distant Mountains
            Color(0.5, 0.7, 0.6, 1)
            self.mount1 = Ellipse(size=(600, 400), pos=(Window.width * 0.1, Window.height * 0.05))
            self.mount2 = Ellipse(size=(800, 500), pos=(Window.width * 0.6, Window.height * 0.05))
            
            # Clouds
            Color(1, 1, 1, 0.9)
            self.cloud1 = Ellipse(size=(180, 70), pos=(Window.width * 0.2, Window.height * 0.7))
            self.cloud2 = Ellipse(size=(220, 90), pos=(Window.width * 0.7, Window.height * 0.8))
            
            # Solid Ground
            Color(0.2, 0.7, 0.3, 1) # Lush Green
            self.ground = Rectangle(size=(3000, Window.height * 0.15), pos=(0,0))
            
            # Player Silhouette (Safety Net)
            self.player_color = Color(0.2, 0.8, 0.2, 1)
            self.player_shape = Ellipse(size=(90, 90))

        # 2. CHARACTER ROSTER
        self.roster = [
            {'file': 'dino.png', 'name': 'DINO', 'color': (0.2, 0.8, 0.2, 1)},
            {'file': 'hallie.png', 'name': 'HALLIE', 'color': (1, 0.4, 0.7, 1)},
            {'file': 'sky.png', 'name': 'SKY', 'color': (0.2, 0.6, 1, 1)}
        ]
        self.char_idx = 0
        
        # 3. THE PLAYER WIDGET
        self.player_img = Image(
            source=self.roster[self.char_idx]['file'],
            size_hint=(0.25, 0.25), pos_hint={'center_x': 0.2, 'center_y': 0.25}
        )
        
        # Magic Flip Logic inside the canvas
        with self.player_img.canvas.before:
            PushMatrix()
            self.flip_scale = Scale(1, 1, 1)
        with self.player_img.canvas.after:
            PopMatrix()
            
        self.add_widget(self.player_img)
        
        # 4. EPIC UI
        self.title_label = Label(
            text=f"[b]DINO & FRIENDS[/b]\nSelected: {self.roster[self.char_idx]['name']}", 
            markup=True, font_size='45sp', halign='center',
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )
        self.add_widget(self.title_label)
        
        self.score_label = Label(
            text="Score: 0 | High: 0", font_size='28sp', color=(0,0,0,1),
            pos_hint={'center_x': 0.5, 'center_y': 0.92}, opacity=0
        )
        self.add_widget(self.score_label)
        
        # 5. PHYSICS STATE
        self.velocity = 0
        self.jumps_left = 2
        self.obstacles = []
        Clock.schedule_interval(self.update, 1.0/60.0)

    def on_touch_down(self, touch):
        if self.state in ['MENU', 'GAMEOVER']:
            if touch.spos[0] > 0.5: # Tap Right
                self.char_idx = (self.char_idx + 1) % len(self.roster)
                char_data = self.roster[self.char_idx]
                self.player_img.source = char_data['file']
                self.player_color.rgba = char_data['color']
                self.title_label.text = f"[b]DINO & FRIENDS[/b]\nSelected: {char_data['name']}"
            else: # Tap Left
                self.start_game()
        elif self.state == 'PLAYING':
            if self.jumps_left > 0: # Smooth Double Jump
                self.velocity = JUMP_POWER
                self.jumps_left -= 1

    def start_game(self):
        self.state = 'PLAYING'
        self.score = 0
        self.game_speed = STARTING_SPEED
        self.title_label.opacity = 0
        self.score_label.opacity = 1
        self.score_label.text = f"Score: 0 | High: {self.high_score}"
        
        for obs in self.obstacles:
            self.remove_widget(obs['img'])
        self.obstacles = []
        self.player_img.pos_hint['center_y'] = 0.25
        self.velocity = 0

    def update(self, dt):
        # Update Flip Origin
        self.flip_scale.origin = self.player_img.center
        self.flip_scale.x = -1 if FLIP_CHARACTER else 1

        # Keep ground attached
        self.ground.size = (Window.width, Window.height * 0.15)
        self.player_shape.pos = (self.player_img.x + 30, self.player_img.y + 15)
        
        # Parallax Background (Mountains & Clouds move at different speeds)
        self.mount1.pos = (self.mount1.pos[0] - (self.game_speed * 0.1), self.mount1.pos[1])
        self.mount2.pos = (self.mount2.pos[0] - (self.game_speed * 0.1), self.mount2.pos[1])
        if self.mount1.pos[0] < -800: self.mount1.pos = (Window.width, self.mount1.pos[1])
        if self.mount2.pos[0] < -800: self.mount2.pos = (Window.width, self.mount2.pos[1])

        self.cloud1.pos = (self.cloud1.pos[0] - 0.5, self.cloud1.pos[1])
        self.cloud2.pos = (self.cloud2.pos[0] - 0.8, self.cloud2.pos[1])
        if self.cloud1.pos[0] < -200: self.cloud1.pos = (Window.width, self.cloud1.pos[1])
        if self.cloud2.pos[0] < -200: self.cloud2.pos = (Window.width, self.cloud2.pos[1])

        if self.state != 'PLAYING': return

        # Pro Physics Update
        self.velocity += GRAVITY
        self.player_img.pos_hint['center_y'] += (self.velocity / Window.height)
        
        # Hit the Floor smoothly
        if self.player_img.pos_hint['center_y'] <= 0.25:
            self.player_img.pos_hint['center_y'] = 0.25
            self.velocity = 0
            self.jumps_left = 2

        # Fair Spawning (Wait longer between spawns)
        if random.random() < 0.012:
            # Don't spawn if the last obstacle is too close
            if not self.obstacles or self.obstacles[-1]['img'].pos_hint['center_x'] < 0.6:
                self.spawn_obstacle()

        for obs in self.obstacles[:]:
            move_speed = self.game_speed * 1.2 if obs['type'] == 'flying' else self.game_speed
            obs['img'].pos_hint['center_x'] -= (move_speed / Window.width)
            
            # FAIR HITBOXES (Very forgiving)
            if self.player_img.collide_widget(obs['img']):
                dx = abs(self.player_img.center_x - obs['img'].center_x)
                dy = abs(self.player_img.center_y - obs['img'].center_y)
                if dx < (self.player_img.width * 0.25) and dy < (self.player_img.height * 0.3):
                    self.game_over()
                    
            if obs['img'].pos_hint['center_x'] < -0.1:
                self.remove_widget(obs['img'])
                self.obstacles.remove(obs)
                self.score += 1
                if self.score > self.high_score: self.high_score = self.score
                self.score_label.text = f"Score: {self.score} | High: {self.high_score}"
                
                # Gradual speed increase
                if self.score % 5 == 0: self.game_speed += 0.5 

    def spawn_obstacle(self):
        is_flying = random.choice([True, False])
        y_pos = 0.45 if is_flying else 0.22
        
        obs_img = Image(
            source='enemy.png', size_hint=(0.12, 0.15), 
            pos_hint={'center_x': 1.1, 'center_y': y_pos}
        )
        with obs_img.canvas.before:
            Color(0.8, 0.1, 0.1, 1) # Red fallback if image fails
            Rectangle(pos=obs_img.pos, size=obs_img.size)
            
        self.add_widget(obs_img)
        self.obstacles.append({'img': obs_img, 'type': 'flying' if is_flying else 'ground'})

    def game_over(self):
        self.state = 'GAMEOVER'
        self.title_label.text = "[color=ff0000][b]WASTED[/b][/color]\nTap LEFT to restart\nTap RIGHT to change character"
        self.title_label.opacity = 1

class PlatinumApp(App):
    def build(self):
        return PlatinumGameWorld()

if __name__ == '__main__':
    PlatinumApp().run()
