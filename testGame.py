import pygame
import random
import math
import sys
import sqlite3
import json
import config
import pause
from button import Button
from main import get_font

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
)
pygame.display.set_caption("Tower Defense")

# Database helper functions for user progress

def get_user_progress(username):
    """
    Liest das JSON-Feld 'progress' aus der Tabelle 'users'.
    Gibt ein Python-Dict zurück, z.B. {"level":25, "points":6000}.
    Falls nicht gefunden oder ungültig: None.
    """
    with sqlite3.connect('tdg_user.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT progress FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            try:
                return json.loads(row[0])
            except json.JSONDecodeError:
                return None
        else:
            return None


def update_user_progress(username, progress_dict):
    """
    Speichert das Python-Dict 'progress_dict' als JSON-String in das Feld 'progress'.
    """
    json_str = json.dumps(progress_dict)
    with sqlite3.connect('tdg_user.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            cursor.execute("UPDATE users SET progress = ? WHERE username = ?", (json_str, username))
            conn.commit()
        else:
            print(f"User '{username}' not found in database.")

# Load assets
BACKGROUND = pygame.transform.scale(
    pygame.image.load("assets/images/level1/tiles.png"),
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)
RAW_CANNON_DOUBLE = pygame.image.load("assets/images/tower/Cannon2.png")
RAW_CANNON_SMALL = pygame.image.load("assets/images/tower/Cannon3.png")
RAW_COIN_ICON = pygame.image.load("assets/images/level1/coin.png")
RAW_HEART_ICON = pygame.image.load("assets/images/level1/heart_icon.png")
# Upgrade icons
RAW_UPGRADE_ICON = pygame.image.load("assets/images/level1/upgrade_icon.png")
RAW_ICON_DAMAGE = pygame.image.load("assets/images/level1/damage_icon.png")
RAW_ICON_RANGE = pygame.image.load("assets/images/level1/sniper_icon.png")
RAW_ICON_RELOAD = pygame.image.load("assets/images/level1/magazine_icon.png")
BULLET_IMG = pygame.image.load("assets/images/tower/bullet_cannon.png")
# Enemy image
RAW_ENEMY_IMG = pygame.image.load("assets/images/enemy/enemy_1.png")
# Projectile images
RAW_BULLET_IMG = pygame.image.load("assets/images/tower/bullet_cannon.png")
RAW_LASER_IMG = pygame.image.load("assets/images/tower/Laser_Bullet.png")
# Upgrade panel background image
RAW_UPGRADE_PANEL = pygame.image.load("assets/images/tower/Upgrade_Panel.png")
# Upgrade button image
RAW_UPGRADE_BUTTON = pygame.image.load("assets/images/tower/Upgrade Button.png")
# Speed buttons
RAW_SPEED_X1 = pygame.image.load("assets/images/tower/SpeedX1.png")
RAW_SPEED_X2 = pygame.image.load("assets/images/tower/SpeedX2.png")
# Sound
SOUND_ENEMY_DEATH = pygame.mixer.Sound("assets/sounds/Uff.mp3")

# Scale icons and images
CANNON_DOUBLE = pygame.transform.scale(RAW_CANNON_DOUBLE, (config.ICON_SIZE, config.ICON_SIZE))
CANNON_SMALL = pygame.transform.scale(RAW_CANNON_SMALL, (config.ICON_SIZE, config.ICON_SIZE))
COIN_ICON = pygame.transform.scale(RAW_COIN_ICON, (config.HUD_FONT_SIZE, config.HUD_FONT_SIZE))
HEART_ICON = pygame.transform.scale(RAW_HEART_ICON, (config.HUD_FONT_SIZE, config.HUD_FONT_SIZE))
UPGRADE_ICON = pygame.transform.scale(RAW_UPGRADE_ICON, (config.ICON_SIZE, config.ICON_SIZE))
ICON_DAMAGE = pygame.transform.scale(RAW_ICON_DAMAGE, (config.ICON_SIZE, config.ICON_SIZE))
ICON_RANGE = pygame.transform.scale(RAW_ICON_RANGE, (config.ICON_SIZE, config.ICON_SIZE))
ICON_RELOAD = pygame.transform.scale(RAW_ICON_RELOAD, (config.ICON_SIZE, config.ICON_SIZE))
# projectile images
BULLET_IMG = pygame.transform.scale(RAW_BULLET_IMG, (20, 20))
LASER_BULLET = pygame.transform.scale(RAW_LASER_IMG, (20, 20))
RAW_UPGRADE_BUTTON = pygame.transform.scale(RAW_UPGRADE_BUTTON, (200, config.ICON_SIZE + 20))
ENEMY_IMG = pygame.transform.scale(RAW_ENEMY_IMG, (config.GRID_SIZE, config.GRID_SIZE))
# Speed images scaled to 140x140
SPEED_X1 = pygame.transform.scale(RAW_SPEED_X1, (140, 140))
SPEED_X2 = pygame.transform.scale(RAW_SPEED_X2, (140, 140))
CANNON_DOUBLE = pygame.transform.scale(RAW_CANNON_DOUBLE, (config.ICON_SIZE, config.ICON_SIZE))
CANNON_SMALL = pygame.transform.scale(RAW_CANNON_SMALL, (config.ICON_SIZE, config.ICON_SIZE))
COIN_ICON = pygame.transform.scale(RAW_COIN_ICON, (config.HUD_FONT_SIZE, config.HUD_FONT_SIZE))
HEART_ICON = pygame.transform.scale(RAW_HEART_ICON, (config.HUD_FONT_SIZE, config.HUD_FONT_SIZE))
UPGRADE_ICON = pygame.transform.scale(RAW_UPGRADE_ICON, (config.ICON_SIZE, config.ICON_SIZE))
ICON_DAMAGE = pygame.transform.scale(RAW_ICON_DAMAGE, (config.ICON_SIZE, config.ICON_SIZE))
ICON_RANGE = pygame.transform.scale(RAW_ICON_RANGE, (config.ICON_SIZE, config.ICON_SIZE))
ICON_RELOAD = pygame.transform.scale(RAW_ICON_RELOAD, (config.ICON_SIZE, config.ICON_SIZE))
# projectile images
BULLET_IMG = pygame.transform.scale(RAW_BULLET_IMG, (20, 20))
LASER_BULLET = pygame.transform.scale(RAW_LASER_IMG, (20, 20))
RAW_UPGRADE_BUTTON = pygame.transform.scale(RAW_UPGRADE_BUTTON, (200, config.ICON_SIZE + 20))
ENEMY_IMG = pygame.transform.scale(RAW_ENEMY_IMG, (config.GRID_SIZE, config.GRID_SIZE))


# Sounds
LASER_SOUNDS_SMALL = [
    pygame.mixer.Sound("assets/sounds/Laser1.mp3"),
    pygame.mixer.Sound("assets/sounds/Laser2.mp3")
]
for sound in LASER_SOUNDS_SMALL:
    sound.set_volume(0.1)

LASER_SOUNDS_DOUBLE = [
    pygame.mixer.Sound("assets/sounds/Laser3.mp3"),
    pygame.mixer.Sound("assets/sounds/Laser4.mp3")
]
for sound in LASER_SOUNDS_DOUBLE:
    sound.set_volume(0.1)


# Path
PATH = [(int(x * SCREEN_WIDTH), int(y * SCREEN_HEIGHT)) for x, y in config.PATH_PERCENTAGES_LEVEL_1]

# Helper functions
def draw_circle(screen, pos, color, radius):
    pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), radius)

def load_font(size):
    return pygame.font.SysFont(None, size)

# Classes
class Bullet:
    def __init__(self, x, y, target, is_laser=False):
        self.x = x
        self.y = y
        self.target = target
        self.speed = getattr(target, 'bullet_speed', 10)
        self.is_laser = is_laser
        self.image = LASER_BULLET if is_laser else BULLET_IMG
        self.radius = 10
        self.angle = 0

    def move(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist:
            ux, uy = dx/dist, dy/dist
            self.x += ux * self.speed
            self.y += uy * self.speed
            self.angle = math.degrees(math.atan2(-uy, ux))

    def draw(self, screen):
        draw_angle = self.angle if self.is_laser else self.angle + 90
        rotated = pygame.transform.rotate(self.image, draw_angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect.topleft)

    def hit(self):
        return (self.x - self.target.x)**2 + (self.y - self.target.y)**2 <= self.radius**2

class Enemy:
    def __init__(self, path, speed=None, health=None, image=None, xp_reward=None):
        self.alive = True
        self.path = path
        self.index = 0
        self.x, self.y = path[0]
        self.speed = speed if speed is not None else config.ENEMY_SPEED
        self.health = health if health is not None else config.ENEMY_HEALTH
        self.xp_reward = xp_reward if xp_reward is not None else 20
        # For drawing
        if image:
            raw = pygame.image.load(image).convert_alpha()
            self.base_image = pygame.transform.scale(raw, (config.GRID_SIZE, config.GRID_SIZE))
        else:
            self.base_image = ENEMY_IMG
        self.rotated_image = self.base_image
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def move(self):
        if self.index < len(self.path) - 1:
            tx, ty = self.path[self.index + 1]
            dx, dy = tx - self.x, ty - self.y
            dist = math.hypot(dx, dy)
            if dist:
                dx /= dist
                dy /= dist
            self.x += dx * self.speed
            self.y += dy * self.speed
            if abs(self.x - tx) < self.speed and abs(self.y - ty) < self.speed:
                self.index += 1
            angle = math.degrees(math.atan2(-dy, dx)) - 90
            self.rotated_image = pygame.transform.rotate(self.base_image, angle)
            self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.rotated_image, self.rect.topleft)
        bar_w = config.GRID_SIZE // 2
        bar_h = 5
        ratio = max(self.health, 0) / config.ENEMY_HEALTH
        bx = self.x - bar_w // 2
        by = self.y - 20
        pygame.draw.rect(screen, config.RED, (bx, by, bar_w, bar_h))
        pygame.draw.rect(screen, config.GREEN, (bx, by, int(bar_w * ratio), bar_h))

    def has_reached_end(self):
        return self.index >= len(self.path) - 1

    def reached_end(self):
        return self.has_reached_end()

class Tower:
    def __init__(self, x, y, ttype):
        self.x, self.y = x, y
        self.type = ttype  # 'small' oder 'double'
        cfg = config.TOWER_CONFIG[ttype]
        self.cost = cfg['cost']
        self.base_cooldown = cfg['cooldown']  # Basiskühlzeit
        self.cooldown = self.base_cooldown
        self.range = cfg['range']
        self.damage = cfg['damage']
        self.last_shot = 0
        self.bullets = []
        self.target = None
        self.sound_index = 0
        self.level = 0  # Combined upgrade level
        # Für double tower verzögerten zweiten Schuss
        self.next_shot_time = None
        self._shot_perp = (0,0)
        # Textur laden
        self._update_texture()
        self.x, self.y = x, y
        self.type = ttype  # 'small' or 'double'
        cfg = config.TOWER_CONFIG[ttype]
        self.cost = cfg['cost']
        self.range = cfg['range']
        self.cooldown = cfg['cooldown']
        self.damage = cfg['damage']
        self.last_shot = 0
        self.bullets = []
        self.target = None
        self.sound_index = 0
        self.level = 0
        self.next_shot_time = None
        self._shot_perp = (0, 0)
        self._update_texture()

    def _update_texture(self):
        base_name = "Cannon2" if self.type == 'double' else "Cannon3"
        suffix = f"_{self.level}" if self.level > 0 else ""
        path = f"assets/images/tower/{base_name}{suffix}.png"
        try:
            img = pygame.image.load(path)
        except Exception:
            img = pygame.image.load(f"assets/images/tower/{base_name}.png")
        size = config.ICON_SIZE
        self.image = pygame.transform.scale(img, (size, size))

    def shoot(self, enemies, now):
        if self.type == 'double':
            if self.next_shot_time is None and now - self.last_shot >= self.cooldown:
                for e in enemies:
                    dx = e.x - self.x
                    dy = e.y - self.y
                    if dx*dx + dy*dy <= self.range**2:
                        dist = math.hypot(dx, dy)
                        ux, uy = dx/dist, dy/dist
                        px, py = -uy, ux
                        offset = config.ICON_SIZE // 4
                        sx = self.x + px*offset
                        sy = self.y + py*offset
                        is_laser = (self.level == 3)
                        self.bullets.append(Bullet(sx, sy, e, is_laser))
                        LASER_SOUNDS_DOUBLE[self.sound_index % 2].play()
                        self.sound_index += 1
                        self.next_shot_time = now + 500
                        self.target = e
                        self._shot_perp = (px*offset, py*offset)
                        break
            elif self.next_shot_time is not None and now >= self.next_shot_time:
                e = self.target
                if e and (e.x - self.x)**2 + (e.y - self.y)**2 <= self.range**2:
                    px_off, py_off = self._shot_perp
                    sx = self.x - px_off
                    sy = self.y - py_off
                    is_laser = (self.level == 3)
                    self.bullets.append(Bullet(sx, sy, e, is_laser))
                    LASER_SOUNDS_DOUBLE[self.sound_index % 2].play()
                    self.sound_index += 1
                self.next_shot_time = None
                self.last_shot = now
        else:
            if now - self.last_shot >= self.cooldown:
                for e in enemies:
                    if (e.x - self.x)**2 + (e.y - self.y)**2 <= self.range**2:
                        is_laser = (self.level == 3)
                        self.bullets.append(Bullet(self.x, self.y, e, is_laser))
                        LASER_SOUNDS_SMALL[self.sound_index % 2].play()
                        self.sound_index += 1
                        self.target = e
                        self.last_shot = now
                        break

        for e in enemies:
            if not e.alive:
                continue
            dx = e.x - self.x
            dy = e.y - self.y

    def update(self):
        for b in self.bullets[:]:
            b.move()
            if b.hit():
                if b.target.alive:
                    b.target.health -= self.damage
                    if b.target.health <= 0:
                        b.target.alive = False
                        SOUND_ENEMY_DEATH.play()
                self.bullets.remove(b)

    def draw(self, screen):
        ang = 0
        if self.target:
            dx = self.target.x - self.x
            dy = self.target.y - self.y
            ang = math.degrees(math.atan2(-dy, dx)) - 90
        rot = pygame.transform.rotate(self.image, ang)
        rect = rot.get_rect(center=(self.x, self.y))
        screen.blit(rot, rect.topleft)
        for b in self.bullets:
            b.draw(screen)

class TowerDefenseGame:
    def __init__(self, username=None):
        # Falls kein Benutzer übergeben, aktuellen Login aus login.py abfragen
        if username is None:
            from login import check_login_status
            logged_in, current_user = check_login_status()
            if not logged_in:
                print("Kein Benutzer eingeloggt. Bitte zuerst einloggen.")
                sys.exit()
            username = current_user
        self.username = username
        # Spieler-Fortschritt laden
        prog = get_user_progress(self.username)
        if prog is None:
            prog = {"level": 1, "points": 0}
            update_user_progress(self.username, prog)
        self.player_level = prog.get("level", 1)
        self.player_xp = prog.get("points", 0)
        self.xp_to_next_level = self._xp_needed_for_level(self.player_level)
        self.levelup_msg = ""
        self.levelup_time = 0
        
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.enemies = []
        self.towers = []
        self.occupied = set()
        # Dev Mode
        self.dev_mode = False
        self.drawing = False
        self.start_pos = None
        # Placement cells
        self.placement_cells = set(config.PLACEMENT_CELLS)
        self.spawn_timer = 0
        self.spawn_interval = 2000
        self.lives = config.INITIAL_LIVES
        self.coins = config.START_COINS
        self.coin_reward = config.COIN_REWARD
        self.selected = None
        self.selected_tower = None
        self.message = ''
        self.msg_time = 0
        self.upgrade_buttons = {}
        self.upgrade_defs = config.TOWER_UPGRADES
        # Game speed (1x or 2x)
        self.game_speed = 1
        # Neue Wave-Logik
        self.wave_active = False
        self.current_wave = 0
        self.max_waves = 10
        self.enemies_spawned = 0
        self.enemies_to_spawn = 0
        self.enemy_spawn_interval = 800  # Basisintervall
        self.wave_cooldown = 3000       # Pause zwischen den Waves in ms
        self.last_spawn_time = 0
        self.volume = 5
        self.win = False
        self.damage_sound = pygame.mixer.Sound("assets/sounds/damage.mp3")
        self.damage_sound.set_volume(0.1)

    def _xp_needed_for_level(self, lvl: int) -> int:
        return 100 * lvl

    def _on_level_up_bonuses(self):
        self.lives += 1
        self.coins += 50
        self.levelup_msg = f"Level {self.player_level} erreicht!"
        self.levelup_time = pygame.time.get_ticks()

    def _check_player_level_up(self):
        while self.player_xp >= self.xp_to_next_level:
            self.player_xp -= self.xp_to_next_level
            self.player_level += 1
            self._on_level_up_bonuses()
            self.xp_to_next_level = self._xp_needed_for_level(self.player_level)
        new_dict = {"level": self.player_level, "points": self.player_xp}
        update_user_progress(self.username, new_dict)

    def spawn_enemy(self, enemy_type="normal"):
        # Erzeuge Gegner je nach Typ mit skalierenden Werten
        base_speed = config.ENEMY_SPEED
        base_health = config.ENEMY_HEALTH
        wave_factor = self.current_wave
        if enemy_type == "fast":
            speed = base_speed + wave_factor * 0.2
            health = base_health
            xp = 20 + wave_factor * 2
            image = None
        elif enemy_type == "strong":
            speed = base_speed
            health = base_health + wave_factor * 10
            xp = 30 + wave_factor * 3
            image = None
        else:
            speed = base_speed + wave_factor * 0.1
            health = base_health + wave_factor * 5
            xp = 25 + wave_factor * 2
            image = None
        e = Enemy(
            PATH,
            speed=speed,
            health=health,
            image=image,
            xp_reward=int(xp)
        )
        self.enemies.append(e)

    def _clicked_sidebar(self, x, y):
        y0 = config.ICON_PADDING*2 + COIN_ICON.get_height() + HEART_ICON.get_height()
        if config.ICON_PADDING <= x <= config.ICON_PADDING + config.ICON_SIZE:
            if y0 <= y <= y0 + config.ICON_SIZE:
                return 'double'
            if y0 + config.ICON_SIZE + config.ICON_PADDING <= y <= y0 + 2*config.ICON_SIZE + config.ICON_PADDING:
                return 'small'
        return None

    def _clicked_sidebar(self, x, y):
        y0 = config.ICON_PADDING*2 + COIN_ICON.get_height() + HEART_ICON.get_height()
        if config.ICON_PADDING <= x <= config.ICON_PADDING + config.ICON_SIZE:
            if y0 <= y <= y0 + config.ICON_SIZE:
                return 'double'
            if y0 + config.ICON_SIZE + config.ICON_PADDING <= y <= y0 + 2*config.ICON_SIZE + config.ICON_PADDING:
                return 'small'
        return None

    def _handle_upgrade_click(self, x, y):
        if not self.selected_tower:
            return False
        panel_width = 800
        visible_width = 600
        panel_x = SCREEN_WIDTH - visible_width
        panel_y = -200
        btn_w = panel_width - 40
        btn_h = config.ICON_SIZE + 20
        btn_x = panel_x + 20
        btn_y = panel_y + 300
        btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        if btn_rect.collidepoint(x, y):
            lvl = self.selected_tower.level
            if lvl >= 3:
                self.message = "Turm bereits maximal aufgewertet"
            else:
                next_lvl = lvl + 1
                defs = self.upgrade_defs.get(next_lvl)
                if not defs:
                    self.message = "Kein Upgrade definiert"
                else:
                    cost = defs['cost']
                    if self.coins < cost:
                        self.message = f"Upgrade benötigt: {cost} Münzen"
                    else:
                        self.coins -= cost
                        self.selected_tower.damage += defs['Damage']
                        self.selected_tower.range += defs['Range']
                        self.selected_tower.cooldown = max(100, self.selected_tower.cooldown - defs['Reload'])
                        self.selected_tower.level = next_lvl
                        self.selected_tower._update_texture()
                        self.message = "Upgrade erfolgreich"
            self.msg_time = pygame.time.get_ticks()
            return True
        return False

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                p = pause.Pause(self)
                p.pause_menu()
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_d:
                self.dev_mode = not self.dev_mode
                self.message = f"Dev Mode {'ein' if self.dev_mode else 'aus'}"
                self.msg_time = pygame.time.get_ticks()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Speed button area (unten rechts), vergrößerte Fläche
                speed_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, 140, 40)
                if speed_rect.collidepoint(x, y):
                    self.game_speed = 2 if self.game_speed == 1 else 1
                    return
                gx, gy = x // config.GRID_SIZE, y // config.GRID_SIZE
                if self._handle_upgrade_click(x, y):
                    return
                for tw in self.towers:
                    if (tw.x-x)**2 + (tw.y-y)**2 <= (config.GRID_SIZE//2)**2:
                        self.selected_tower = tw
                        self.selected = None
                        return
                self.selected_tower = None
                ch = self._clicked_sidebar(x, y)
                if ch:
                    self.selected = ch
                    return
                if not self.dev_mode and x > config.SHOP_WIDTH:
                    if (gx, gy) in self.placement_cells:
                        if not self.selected:
                            self.message = "Bitte Turm auswählen"
                            self.msg_time = pygame.time.get_ticks()
                            return
                        if (gx, gy) in self.occupied:
                            self.message = "Hier steht bereits ein Turm"
                        else:
                            cost = config.TOWER_CONFIG[self.selected]['cost']
                            if self.coins >= cost:
                                self.coins -= cost
                                wx = gx*config.GRID_SIZE + config.GRID_SIZE//2
                                wy = gy*config.GRID_SIZE + config.GRID_SIZE//2
                                self.towers.append(Tower(wx, wy, self.selected))
                                self.occupied.add((gx, gy))
                                self.selected = None
                            else:
                                self.message = f"Benötigt: {cost} Münzen"
                        self.msg_time = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if not self.wave_active and self.current_wave < self.max_waves:
            if now - self.last_spawn_time > self.wave_cooldown:
                self.current_wave += 1
                self.wave_active = True
                self.enemies_spawned = 0
                # Anzahl Gegner pro Wave: Basis 5 +2 pro Wave
                self.enemies_to_spawn = 5 + (self.current_wave - 1) * 2
                # Spawnintervall pro Wave: Basis 800ms minus 50ms pro Wave, mindestens 200ms
                self.enemy_spawn_interval = max(200, 800 - (self.current_wave - 1) * 50)
                self.last_spawn_time = now
        if self.wave_active:
            if self.enemies_spawned < self.enemies_to_spawn:
                if now - self.last_spawn_time > self.enemy_spawn_interval:
                    idx = self.enemies_spawned
                    if idx % 3 == 0:
                        etype = "fast"
                    elif idx % 3 == 1:
                        etype = "strong"
                    else:
                        etype = "normal"
                    self.spawn_enemy(etype)
                    self.enemies_spawned += 1
                    self.last_spawn_time = now
            else:
                if not self.enemies:
                    self.wave_active = False
                    self.last_spawn_time = now
                self.last_spawn_time = now
        for e in self.enemies:
            e.move()
        for t in self.towers:
            t.shoot(self.enemies, now)
            t.update()
        for e in self.enemies[:]:
            if e.reached_end():
                self.lives -= 1
                self.damage_sound.play()
                self.enemies.remove(e)
            elif not e.alive:
                self.coins += self.coin_reward
                # XP vergeben
                self.player_xp += e.xp_reward
                self._check_player_level_up()
                self.enemies.remove(e)
        if self.lives <= 0:
            self.running = False
        elif self.current_wave >= self.max_waves and not self.enemies and not self.wave_active:
            self.win = True
            self.running = False

    def draw(self):
        self.screen.blit(BACKGROUND, (0,0))
        pygame.draw.rect(self.screen, config.DARK_GREEN, (0,0,config.SHOP_WIDTH,SCREEN_HEIGHT))
        if self.dev_mode:
            overlay = pygame.Surface((config.GRID_SIZE, config.GRID_SIZE), pygame.SRCALPHA)
            overlay.fill((0,0,255,50))
            for gx, gy in self.placement_cells:
                self.screen.blit(overlay, (gx*config.GRID_SIZE, gy*config.GRID_SIZE))
            if self.drawing and self.start_pos:
                x0, y0 = self.start_pos
                x1, y1 = pygame.mouse.get_pos()
                rx, ry = min(x0, x1), min(y0, y1)
                rw, rh = abs(x1 - x0), abs(y1 - y0)
                pygame.draw.rect(self.screen, config.BLUE, (rx, ry, rw, rh), 2)
        font = load_font(config.HUD_FONT_SIZE)
        # Geschwindigkeit-Button unten rechts (mit Bild)
        if self.game_speed == 2:
            self.screen.blit(SPEED_X2, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150))
        else:
            self.screen.blit(SPEED_X1, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 150))
        self.screen.blit(COIN_ICON, (config.ICON_PADDING, config.ICON_PADDING))
        coins_txt = font.render(str(self.coins), True, config.BLACK)
        self.screen.blit(coins_txt, (config.ICON_PADDING+COIN_ICON.get_width()+5, config.ICON_PADDING))
        self.screen.blit(HEART_ICON, (config.ICON_PADDING, config.ICON_PADDING+COIN_ICON.get_height()+config.ICON_PADDING))
        lives_txt = font.render(str(self.lives), True, config.BLACK)
        self.screen.blit(lives_txt, (config.ICON_PADDING+HEART_ICON.get_width()+5, config.ICON_PADDING+COIN_ICON.get_height()+config.ICON_PADDING))
        y0 = config.ICON_PADDING*2 + COIN_ICON.get_height() + HEART_ICON.get_height()
        cd = config.GREEN if self.coins >= config.TOWER_CONFIG['double']['cost'] else config.RED
        pygame.draw.rect(self.screen, cd, (config.ICON_PADDING, y0, config.ICON_SIZE, config.ICON_SIZE))
        self.screen.blit(CANNON_DOUBLE, (config.ICON_PADDING, y0))
        if self.selected == 'double':
            pygame.draw.rect(
                self.screen,
                config.BLUE,
                (
                    config.ICON_PADDING - 3,
                    y0 - 3,
                    config.ICON_SIZE + 6,
                    config.ICON_SIZE + 6
                ),
                width=3
            )
        y1 = y0 + config.ICON_SIZE + config.ICON_PADDING
        cs = config.GREEN if self.coins >= config.TOWER_CONFIG['small']['cost'] else config.RED
        pygame.draw.rect(self.screen, cs, (config.ICON_PADDING, y1, config.ICON_SIZE, config.ICON_SIZE))
        self.screen.blit(CANNON_SMALL, (config.ICON_PADDING, y1))
        if self.selected == 'small':
            pygame.draw.rect(
                self.screen,
                config.BLUE,
                (
                    config.ICON_PADDING - 3,
                    y1 - 3,
                    config.ICON_SIZE + 6,
                    config.ICON_SIZE + 6
                ),
                width=3
            )
        if self.selected:
            mx, my = pygame.mouse.get_pos(); gx, gy = mx//config.GRID_SIZE, my//config.GRID_SIZE
            if (gx, gy) in config.PLACEMENT_CELLS and mx > config.SHOP_WIDTH:
                img = CANNON_DOUBLE if self.selected == 'double' else CANNON_SMALL
                pv = img.copy(); pv.set_alpha(150)
                rect = pv.get_rect(center=(gx*config.GRID_SIZE+config.GRID_SIZE//2, gy*config.GRID_SIZE+config.GRID_SIZE//2))
                self.screen.blit(pv, rect.topleft)
                col = config.GREEN if self.coins >= config.TOWER_CONFIG[self.selected]['cost'] and (gx, gy) not in self.occupied else config.RED
                ov = pygame.Surface((config.GRID_SIZE, config.GRID_SIZE), pygame.SRCALPHA); ov.fill((*col,100)); self.screen.blit(ov, (gx*config.GRID_SIZE, gy*config.GRID_SIZE))
        for e in self.enemies: e.draw(self.screen)
        for t in self.towers: t.draw(self.screen)
        if self.selected_tower:
            pw = 800
            ph = SCREEN_HEIGHT + 400
            visible_w = 600
            px = SCREEN_WIDTH - visible_w
            py = -200
            panel = pygame.transform.scale(RAW_UPGRADE_PANEL, (pw, ph))
            self.screen.blit(panel, (px, py))
            font_small = load_font(28)
            lvl = self.selected_tower.level
            next_lvl = lvl + 1 if lvl < 3 else lvl
            cost = 0
            if lvl < 3:
                cost = self.upgrade_defs[next_lvl]['cost']
            btn_w = pw - 300
            btn_h = config.ICON_SIZE + 200
            btn_x = px + 160
            btn_y = py + 250
            btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            button_img = pygame.transform.scale(RAW_UPGRADE_BUTTON, (btn_w, btn_h))
            self.screen.blit(button_img, (btn_x, btn_y))
            icon_y = btn_y + (btn_h - config.ICON_SIZE) // 2
            self.screen.blit(UPGRADE_ICON, (btn_x + 115, icon_y))
            if lvl < 3:
                coin_x = btn_x + 110 + config.ICON_SIZE
                self.screen.blit(COIN_ICON, (coin_x, icon_y + (config.ICON_SIZE - COIN_ICON.get_height())//2))
                cost_surf = font_small.render(str(cost), True, config.WHITE)
                self.screen.blit(cost_surf, (coin_x + COIN_ICON.get_width() + 10,
                                             icon_y + (config.ICON_SIZE - cost_surf.get_height())//2))
            label = "Upgrade" if lvl < 3 else "Maxed"
            label_surf = font_small.render(label, True, config.WHITE)
            lbl_x = btn_x + btn_w - label_surf.get_width() - 140
            lbl_y = btn_y + (btn_h - label_surf.get_height())//2
            self.screen.blit(label_surf, (lbl_x, lbl_y))
        if self.message and pygame.time.get_ticks() - self.msg_time < 2000:
            mtxt = font.render(self.message, True, config.RED)
            self.screen.blit(mtxt, (SCREEN_WIDTH//2 - mtxt.get_width()//2, config.ICON_PADDING))
        # XP-Leiste und Levelanzeige
        font = load_font(config.HUD_FONT_SIZE)
        lvl_surf = font.render(f"Level: {self.player_level}", True, config.WHITE)
        self.screen.blit(lvl_surf, (SCREEN_WIDTH - lvl_surf.get_width() - 20, 20))
        bar_x = SCREEN_WIDTH - 300
        bar_y = 60
        bar_w = 200
        bar_h = 20
        pygame.draw.rect(self.screen, config.WHITE, (bar_x - 2, bar_y - 2, bar_w + 4, bar_h + 4), 2)
        ratio = self.player_xp / max(1, self.xp_to_next_level)
        pygame.draw.rect(self.screen, config.GREEN, (bar_x, bar_y, int(bar_w * ratio), bar_h))
        if self.levelup_msg and pygame.time.get_ticks() - self.levelup_time < 2000:
            msg_surf = font.render(self.levelup_msg, True, config.YELLOW)
            self.screen.blit(
                msg_surf,
                (
                    SCREEN_WIDTH // 2 - msg_surf.get_width() // 2,
                    SCREEN_HEIGHT // 2 - msg_surf.get_height() // 2
                )
            )
        else:
            self.levelup_msg = ""
                # Anzeige der aktuellen Wave oben mittig
        wave_text = font.render(f"Wave: {self.current_wave} / {self.max_waves}", True, config.WHITE)
        wave_rect = wave_text.get_rect(center=(SCREEN_WIDTH // 2, config.HUD_FONT_SIZE))
        self.screen.blit(wave_text, wave_rect)

        pygame.display.flip()

    def show_win_screen(self):
        win_font = pygame.font.SysFont("arial", 50)
        win_text = win_font.render("Du hast gewonnen!", True, (0, 255, 0))
        self.screen.fill((0, 0, 0))
        self.screen.blit(win_text, (self.screen.get_width() // 2 - win_text.get_width() // 2,
                                self.screen.get_height() // 2 - win_text.get_height() // 2))
        pygame.display.flip()

    def game_over_screen(self):
        font_large = get_font(72)
        font_btn = get_font(48)

        bg_image = pygame.image.load("assets/images/start_screen/Background1.png").convert()
        bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        gameover_sounds = [
            pygame.mixer.Sound("assets/sounds/Fortnite.mp3"),
            pygame.mixer.Sound("assets/sounds/death-bong.mp3")
        ]
        for sound in gameover_sounds:
            sound.set_volume(0.1)
        random.choice(gameover_sounds).play()
        restart_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30), "Restart", font_btn, config.WHITE, config.RED)
        exit_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30), "Exit", font_btn, config.WHITE, config.RED)
        while True:
            self.screen.blit(bg_image, (0, 0))
            title_surf = font_large.render("GAME OVER", True, config.RED)
            self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150)))
            mouse_pos = pygame.mouse.get_pos()
            for btn in [restart_btn, exit_btn]:
                btn.changeColor(mouse_pos)
                btn.update(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_btn.checkForInput(mouse_pos):
                        return
                    elif exit_btn.checkForInput(mouse_pos):
                        self.running = False
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return
                    elif event.key == pygame.K_e:
                        self.running = False
                        return

    def winner_screen(self):
        font_large = get_font(72)
        font_btn = get_font(48)

        bg_image = pygame.image.load("assets/images/start_screen/Background1.png").convert()
        bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        win_sound = pygame.mixer.Sound("assets/sounds/gewonnen.mp3")
        win_sound.set_volume(0.1)
        win_sound.play()
        restart_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30), "Restart", font_btn, config.WHITE, config.GREEN)
        exit_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30), "Exit", font_btn, config.WHITE, config.GREEN)
        while True:
            self.screen.blit(bg_image, (0, 0))
            title_surf = font_large.render("YOU WIN!", True, config.GREEN)
            self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150)))
            mouse_pos = pygame.mouse.get_pos()
            for btn in [restart_btn, exit_btn]:
                btn.changeColor(mouse_pos)
                btn.update(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_btn.checkForInput(mouse_pos):
                        return
                    elif exit_btn.checkForInput(mouse_pos):
                        self.running = False
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return
                    elif event.key == pygame.K_e:
                        self.running = False
                        return

    def end_game(self):
        if self.win:
            self.winner_screen()
        else:
            self.game_over_screen()

    def run(self):
        while self.running:
            self.handle_events()
            # Update mehrfach je nach game_speed für erhöhte Geschwindigkeit
            for _ in range(self.game_speed):
                self.update()
            self.draw()
            self.clock.tick(60)
        self.end_game()

if __name__ == "__main__":
    # Prüfe Login-Status und nutze eingeloggten Benutzer
    from login import check_login_status
    logged_in, current_user = check_login_status()
    if not logged_in:
        print("Kein Benutzer eingeloggt. Bitte zuerst über main.py einloggen.")
        sys.exit()
    username = current_user
    game = TowerDefenseGame(username)
    game.run()
    pygame.quit()
