from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse, PushMatrix, PopMatrix, Scale
import random

# ==========================================
# ⚙️ MASTER GAME SETTINGS
# ==========================================
FLIP_CHARACTER = True  
STARTING_SPEED = 7.0   
GRAVITY = -0.6        
JUMP_POWER = 15.0      
# ==========================================

class UltimateDimensionWorld(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.state = 'MENU'
        self.score = 0
        self.high_score = 0
        self.game_speed = STARTING_SPEED
        self.dimension = 'NORMAL' # NORMAL or MUSHROOM
        
        # 1. THE WORLD ENVIRONMENT
        with self.canvas.before:
            # Sky Background
            self.sky_color = Color(0.3, 0.7, 0.9, 1) # Normal Blue
            self.sky_bg = Rectangle(size=(3000, 3000), pos=(0,0))
            
            # Sun / Moon
            self.sun_color = Color(1, 0.9, 0.2, 1)
            self.sun = Ellipse(size=(150, 150), pos=(Window.width * 0.8, Window.height * 0.75))
            
            # Weather System (Rain/Snow)
            Color(1, 1, 1, 0.6)
            self.raindrops = []
            for _ in range(20):
                drop = Rectangle(size=(5, 15), pos=(random.randint(0, 2000), random.randint(0, 1000)))
                self.raindrops.append(drop)
            
            # Trees (Background)
            self.tree_color = Color(0.1, 0.4, 0.1, 1)
            self.tree1 = Rectangle(size=(80, 200), pos=(Window.width * 0.3, Window.height * 0.15))
            self.tree2 = Rectangle(size=(100, 250), pos=(Window.width * 0.8, Window.height * 0.15))
            
            # Solid Ground
            self.ground_color = Color(0.2, 0.7, 0.3, 1) # Normal Green
            self.ground = Rectangle(size=(3000, Window.height * 0.15), pos=(0,0))
            
            # Player Silhouette (Safety Net)
            self.player_color = Color(0.2, 0.8, 0.2, 1)
            self.player_shape = Ellipse(size=(150, 150))

        # 2. FULL CHARACTER ROSTER
        self.roster = [
            {'file': 'dino.png', 'name': 'DINO', 'color': (0.2, 0.8, 0.2, 1)},
            {'file': 'hallie.png', 'name': 'HALLIE', 'color': (1, 0.4, 0.7, 1)},
            {'file': 'sky.png', 'name': 'SKY', 'color': (0.2, 0.6, 1, 1)},
            {'file': 'winston.png', 'name': 'WINSTON (Bulldog)', 'color': (0.6, 0.4, 0.2, 1)},
            {'file': 'bruno.png', 'name': 'BRUNO (Spaniel)', 'color': (0.4, 0.2, 0.1, 1)},
            {'file': 'ned.png', 'name': 'NED (Spaniel)', 'color': (0.8, 0.8, 0.8, 1)}
        ]
        self.char_idx = 0
        
        # 3. MASSIVE PLAYER WIDGET (Size Tripled!)
        self.player_img = Image(
            source=self.roster[self.char_idx]['file'],
            size_hint=(0.4, 0.4), # TRIPLED IN SIZE
            pos_hint={'center_x': 0.25, 'center_y': 0.3}
        )
        
        # Flip Logic
        with self.player_img.canvas.before:
            PushMatrix()
            self.flip_scale = Scale(1, 1, 1)
        with self.player_img.canvas.after:
            PopMatrix()
            
        self.add_widget(self.player_img)
        
        # 4. UI
        self.title_label = Label(
            text=f"[b]DINO & FRIENDS: MULTIVERSE[/b]\nSelected: {self.roster[self.char_idx]['name']}", 
            markup=True, font_size='40sp', halign='center',
            pos_hint={'center_x': 0.5, 'center_y': 0.65}
        )
        self.add_widget(self.title_label)
        
        self.score_label = Label(
            text="Score: 0 | High: 0", font_size='30sp', color=(1,1,1,1),
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
            if touch.spos[0] > 0.5: # Swap Character
                self.char_idx = (self.char_idx + 1) % len(self.roster)
                char_data = self.roster[self.char_idx]
                self.player_img.source = char_data['file']
                self.player_color.rgba = char_data['color']
                self.title_label.text = f"[b]DINO & FRIENDS[/b]\nSelected: {char_data['name']}"
            else: # Start
                self.start_game()
        elif self.state == 'PLAYING':
            if self.jumps_left > 0:
                self.velocity = JUMP_POWER
                self.jumps_left -= 1

    def start_game(self):
        self.state = 'PLAYING'
        self.score = 0
        self.game_speed = STARTING_SPEED
        self.dimension = 'NORMAL'
        self.change_dimension('NORMAL')
        
        self.title_label.opacity = 0
        self.score_label.opacity = 1
        self.score_label.text = f"Score: 0 | High: {self.high_score}"
        
        for obs in self.obstacles:
            self.remove_widget(obs['img'])
        self.obstacles = []
        self.player_img.pos_hint['center_y'] = 0.3
        self.velocity = 0

    def change_dimension(self, dim):
        self.dimension = dim
        if dim == 'MUSHROOM':
            self.sky_color.rgba = (0.5, 0.1, 0.5, 1) # Purple Sky
            self.ground_color.rgba = (1.0, 0.2, 0.6, 1) # Neon Pink Ground
            self.sun_color.rgba = (0.1, 0.8, 0.1, 1) # Green Sun
            self.tree_color.rgba = (0.1, 0.8, 0.9, 1) # Blue Trees
            self.game_speed += 2 # Speed boost in Mushroom Dimension
        else:
            self.sky_color.rgba = (0.3, 0.7, 0.9, 1) 
            self.ground_color.rgba = (0.2, 0.7, 0.3, 1) 
            self.sun_color.rgba = (1, 0.9, 0.2, 1)
            self.tree_color.rgba = (0.1, 0.4, 0.1, 1)

    def update(self, dt):
        self.flip_scale.origin = self.player_img.center
        self.flip_scale.x = -1 if FLIP_CHARACTER else 1

        # Keep ground attached and update shapes
        self.sky_bg.size = (Window.width, Window.height)
        self.ground.size = (Window.width, Window.height * 0.15)
        self.player_shape.pos = (self.player_img.x + 40, self.player_img.y + 20)
        
        # Weather Animation
        for drop in self.raindrops:
            drop.pos = (drop.pos[0] - 2, drop.pos[1] - 10)
            if drop.pos[1] < 0:
                drop.pos = (random.randint(0, int(Window.width)), Window.height)

        # Tree Parallax
        self.tree1.pos = (self.tree1.pos[0] - (self.game_speed * 0.5), self.tree1.pos[1])
        self.tree2.pos = (self.tree2.pos[0] - (self.game_speed * 0.5), self.tree2.pos[1])
        if self.tree1.pos[0] < -200: self.tree1.pos = (Window.width + 100, self.tree1.pos[1])
        if self.tree2.pos[0] < -200: self.tree2.pos = (Window.width + 400, self.tree2.pos[1])

        if self.state != 'PLAYING': return

        # Dimension Check!
        if self.score >= 10 and self.dimension == 'NORMAL':
            self.change_dimension('MUSHROOM')

        # Physics
        self.velocity += GRAVITY
        self.player_img.pos_hint['center_y'] += (self.velocity / Window.height)
        
        # Floor Hit (Adjusted for massive size)
        if self.player_img.pos_hint['center_y'] <= 0.28:
            self.player_img.pos_hint['center_y'] = 0.28
            self.velocity = 0
            self.jumps_left = 2

        # Spawn Enemies
        if random.random() < 0.015:
            if not self.obstacles or self.obstacles[-1]['img'].pos_hint['center_x'] < 0.5:
                self.spawn_obstacle()

        for obs in self.obstacles[:]:
            move_speed = self.game_speed * 1.2 if obs['type'] == 'flying' else self.game_speed
            obs['img'].pos_hint['center_x'] -= (move_speed / Window.width)
            
            # HUGE HITBOXES
            if self.player_img.collide_widget(obs['img']):
                dx = abs(self.player_img.center_x - obs['img'].center_x)
                dy = abs(self.player_img.center_y - obs['img'].center_y)
                if dx < (self.player_img.width * 0.3) and dy < (self.player_img.height * 0.3):
                    self.game_over()
                    
            if obs['img'].pos_hint['center_x'] < -0.2:
                self.remove_widget(obs['img'])
                self.obstacles.remove(obs)
                self.score += 1
                if self.score > self.high_score: self.high_score = self.score
                self.score_label.text = f"Score: {self.score} | High: {self.high_score}"

    def spawn_obstacle(self):
        is_flying = random.choice([True, False])
        y_pos = 0.55 if is_flying else 0.25
        
        # MASSIVE ENEMIES
        obs_img = Image(
            source='enemy.png', size_hint=(0.25, 0.25), 
            pos_hint={'center_x': 1.2, 'center_y': y_pos}
        )
        with obs_img.canvas.before:
            Color(0.8, 0.1, 0.1, 1) 
            Rectangle(pos=obs_img.pos, size=obs_img.size)
            
        self.add_widget(obs_img)
        self.obstacles.append({'img': obs_img, 'type': 'flying' if is_flying else 'ground'})

    def game_over(self):
        self.state = 'GAMEOVER'
        self.title_label.text = "[color=ff0000][b]WASTED[/b][/color]\nTap LEFT to restart\nTap RIGHT to change character"
        self.title_label.opacity = 1

class UltimateApp(App):
    def build(self):
        return UltimateDimensionWorld()

if __name__ == '__main__':
    UltimateApp().run()
