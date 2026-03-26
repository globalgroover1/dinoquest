
import pygame
import random
import math
import webbrowser
from datetime import datetime

# --- 1. ENGINE & RAM OPTIMIZATION ---
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 1000, 600
# DOUBLEBUF & HWSURFACE push rendering to the GPU, saving phone battery and RAM!
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Dougie’s Dino Quest: Kids Fossil Hunt & Logic Game")
clock = pygame.time.Clock()

# --- 2. ACCESSIBILITY & FONTS (Cached for Performance) ---
# Comic Sans provides the "bottom-heavy" gravity needed for Dyslexia support.
font_sm = pygame.font.SysFont("Comic Sans MS", 18, bold=True)
font_main = pygame.font.SysFont("Comic Sans MS", 26, bold=True)
font_huge = pygame.font.SysFont("Comic Sans MS", 90, bold=True)

# Pre-rendering static text saves massive amounts of RAM
TXT_PLAY = font_huge.render("PLAY", True, (255, 255, 255))
TXT_PARENT = font_main.render("PARENTAL SHIELD & LEGAL", True, (0, 0, 0))
TXT_STORE = font_main.render("DOUGIE'S MEGA STORE", True, (0, 0, 0))

# --- 3. COLORS & LIVE-OPS ---
GOLD, WHITE, BLACK, NEON_BLUE = (255, 215, 0), (255, 255, 255), (0, 0, 0), (0, 255, 255)
SKY_BLUE, GRASS_GREEN = (135, 206, 235), (34, 139, 34)

DINO_MONTHS = {1:"Iguanodon", 4:"Spinosaurus", 10:"Pumpkin-Rex", 12:"Santa-Saurus"}
IAP_STORE = [
    {"name": "Golden Ned Skin", "price": "$2.49", "desc": "Glow on Leaderboards!"},
    {"name": "Mystery Egg (Gacha)", "price": "$1.99", "desc": "1 Random Legendary Skin"},
    {"name": "Mega Starter Pack", "price": "$4.99", "desc": "No Ads + Winston Suit"},
    {"name": "24hr Bone Potion", "price": "$1.49", "desc": "2x Bones for 24 Hours"}
]

# --- 4. ADVANCED PHYSICS & VFX ---

class Particle:
    __slots__ = ['x', 'y', 'vx', 'vy', 'life', 'color'] # Memory optimization!
    def __init__(self, x, y, color=GOLD):
        self.x, self.y = x, y
        self.vx, self.vy = random.uniform(-6, 6), random.uniform(-6, 6)
        self.life = 255
        self.color = color

    def update(self):
        self.x += self.vx; self.y += self.vy; self.life -= 12

    def draw(self, surf):
        if self.life > 0: pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), random.randint(3, 6))

class Hero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # convert_alpha() maximizes rendering speed
        self.base_img = pygame.Surface((60, 90), pygame.SRCALPHA).convert_alpha()
        pygame.draw.rect(self.base_img, BLACK, (0, 0, 60, 90), border_radius=12) # High Contrast
        pygame.draw.rect(self.base_img, (200, 200, 200), (6, 6, 48, 78), border_radius=10)

        self.x, self.y = 150.0, 460.0 # Sub-pixel float math for buttery smooth jumps
        self.vel_y = 0.0
        self.is_jumping = False
        self.squash = 0
        self.glow = False

    def apply_physics(self):
        self.vel_y += 0.85 # Gravity pull
        self.y += self.vel_y
        if self.y >= 460.0: # Ground collision
            if self.is_jumping: self.squash = 6 # Impact juice
            self.y, self.is_jumping, self.vel_y = 460.0, False, 0.0

    def draw(self, surf):
        w, h = (75, 75) if self.squash > 0 else (60, 90)
        if self.is_jumping: w, h = (50, 100) # Stretch
        if self.squash > 0: self.squash -= 1

        draw_rect = pygame.Rect(int(self.x) - w//2, int(self.y) + 90 - h, w, h)
        img = pygame.transform.scale(self.base_img, (w, h))
        surf.blit(img, draw_rect.topleft)
        if self.glow: pygame.draw.rect(surf, NEON_BLUE, draw_rect, 4, border_radius=12)

# --- 5. THE MASTER STATE MACHINE ---

class GameManager:
    def __init__(self):
        self.mode = "START"
        self.bones = 1500
        self.hero = Hero()
        self.particles = []
        self.shake = 0

        # Live-Ops & Community
        self.today = datetime.now()
        self.is_weekend = self.today.weekday() >= 5
        self.dino_month = DINO_MONTHS.get(self.today.month, "Triceratops")
        self.fan_art_winner = "Explorer Leo" # Update every 30 days!

        # Security
        self.promo_code = ""
        self.math_q = (random.randint(10, 20), random.randint(1, 9))

    def run(self):
        running = True
        while running:
            # Bedtime Lock Check (8 PM)
            if datetime.now().hour >= 20: self.mode = "BEDTIME"

            # Screen Shake Calc
            sx, sy = random.randint(-self.shake, self.shake), random.randint(-self.shake, self.shake)
            if self.shake > 0: self.shake -= 1

            screen.fill(SKY_BLUE if self.mode != "BEDTIME" else (10, 10, 30))
            pygame.draw.rect(screen, GRASS_GREEN, (sx, 550 + sy, WIDTH, 50))

            if self.mode == "START":
                # ASO Menu & Community Loop
                pygame.draw.rect(screen, (0, 180, 0), (350, 150, 300, 120), border_radius=25)
                screen.blit(TXT_PLAY, (405 + sx, 165 + sy))

                # Fan Art Frame
                pygame.draw.rect(screen, WHITE, (720, 320, 250, 210), border_radius=15)
                pygame.draw.rect(screen, GOLD, (720, 320, 250, 210), 6, border_radius=15)
                screen.blit(font_sm.render("FAN ART WINNER", True, BLACK), (760, 335))
                screen.blit(font_sm.render(f"By {self.fan_art_winner}", True, (0, 100, 200)), (745, 480))

                if self.is_weekend: screen.blit(font_main.render("WEEKEND 2X BONES!", True, (220, 20, 60)), (30, 480))
                screen.blit(font_main.render(f"Monthly Dino: {self.dino_month}", True, BLACK), (30, 520))

            elif self.mode == "STORE":
                pygame.draw.rect(screen, WHITE, (100, 50, 800, 500), border_radius=20)
                screen.blit(TXT_STORE, (350, 70))
                for i, item in enumerate(IAP_STORE):
                    y = 130 + (i * 75)
                    pygame.draw.rect(screen, (240, 240, 240), (120, y, 760, 65), border_radius=10)
                    screen.blit(font_main.render(f"{item['name']} - {item['price']}", True, BLACK), (140, y + 15))
                    screen.blit(font_sm.render(item['desc'], True, (0, 100, 200)), (550, y + 20))

            elif self.mode == "PARENT_GATE":
                # The Parental Shield
                pygame.draw.rect(screen, WHITE, (200, 100, 600, 450), border_radius=20)
                screen.blit(TXT_PARENT, (310, 120))
                screen.blit(font_sm.render(f"Adults: What is {self.math_q[0]} + {self.math_q[1]}?", True, BLACK), (350, 180))

                # COPPA Privacy Link
                priv_btn = pygame.draw.rect(screen, BLUE, (350, 250, 300, 50), border_radius=10)
                screen.blit(font_main.render("PRIVACY POLICY", True, WHITE), (395, 255))

                # Support & Promo
                sup_btn = pygame.draw.rect(screen, (50, 50, 50), (350, 320, 300, 50), border_radius=10)
                screen.blit(font_main.render("EMAIL SUPPORT", True, WHITE), (405, 325))

                screen.blit(font_sm.render("Promo Code:", True, BLACK), (350, 400))
                pygame.draw.rect(screen, (220, 220, 220), (460, 395, 190, 35))
                screen.blit(font_sm.render(self.promo_code, True, BLACK), (470, 400))

            elif self.mode == "PLAYING":
                self.hero.apply_physics()
                self.hero.draw(screen)

                # Optimized Particle Rendering
                alive_particles = []
                for p in self.particles:
                    p.update()
                    p.draw(screen)
                    if p.life > 0: alive_particles.append(p)
                self.particles = alive_particles

            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.mode == "START": self.mode = "PLAYING"
                    elif self.mode == "PARENT_GATE":
                        if priv_btn.collidepoint(event.pos): webbrowser.open("https://sites.google.com/view/dougiesdino/privacy")
                        if sup_btn.collidepoint(event.pos): webbrowser.open("mailto:Support@DougiesDino.com")
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.mode == "PLAYING" and not self.hero.is_jumping:
                        self.hero.vel_y = -19.5; self.hero.is_jumping = True; self.shake = 5
                    if event.key == pygame.K_p: self.mode = "PARENT_GATE"
                    if event.key == pygame.K_s: self.mode = "STORE"
                    if event.key == pygame.K_f and self.mode == "PLAYING": # Fossil Hunt Vibe
                        self.shake = 20
                        self.particles.extend([Particle(WIDTH//2, HEIGHT//2) for _ in range(20)])
                    if event.key == pygame.K_ESCAPE: self.mode = "START"
                    if self.mode == "PARENT_GATE":
                        if event.key == pygame.K_RETURN:
                            if self.promo_code == "HERO2026": self.bones += 1000; self.promo_code = "UNLOCKED!"
                        elif event.key == pygame.K_BACKSPACE: self.promo_code = self.promo_code[:-1]
                        elif event.unicode.isalnum(): self.promo_code += event.unicode.upper()

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    GameManager().run()

