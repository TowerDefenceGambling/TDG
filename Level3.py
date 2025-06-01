import pygame
import random
import math
import sys
import config
import pause
from button import Button

# Initialize Pygame
pygame.init()


# Screen setup
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
)
pygame.display.set_caption("Tower Defense")

# Load assets
BACKGROUND = pygame.transform.scale(
    pygame.image.load("assets/images/level3/Map_Level_3.png"),
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)
RAW_CANNON_DOUBLE = pygame.image.load("assets/images/tower/Cannon2.png")
RAW_CANNON_SMALL  = pygame.image.load("assets/images/tower/Cannon3.png")
RAW_COIN_ICON     = pygame.image.load("assets/images/level1/coin.png")
RAW_HEART_ICON    = pygame.image.load("assets/images/level1/heart_icon.png")
# Upgrade icons
RAW_UPGRADE_ICON = pygame.image.load("assets/images/level1/upgrade_icon.png")
RAW_ICON_DAMAGE   = pygame.image.load("assets/images/level1/damage_icon.png")
RAW_ICON_RANGE    = pygame.image.load("assets/images/level1/sniper_icon.png")
RAW_ICON_RELOAD   = pygame.image.load("assets/images/level1/magazine_icon.png")
BULLET_IMG        = pygame.image.load("assets/images/tower/bullet_cannon.png")
# Enemy image
RAW_ENEMY_IMG     = pygame.image.load("assets/images/enemy/enemy_2.png")
# Projectile images
RAW_BULLET_IMG   = pygame.image.load("assets/images/tower/bullet_cannon.png")
RAW_LASER_IMG    = pygame.image.load("assets/images/tower/Laser_Bullet.png")
# Upgrade panel background image
RAW_UPGRADE_PANEL = pygame.image.load("assets/images/tower/Upgrade_Panel.png")
# Upgrade button image
RAW_UPGRADE_BUTTON = pygame.image.load("assets/images/tower/Upgrade Button.png")
RAW_UPGRADE_PANEL = pygame.image.load("assets/images/tower/Upgrade_Panel.png")
#Sound
SOUND_ENEMY_DEATH = pygame.mixer.Sound("assets/sounds/Uff.mp3")


# Scale icons and images
CANNON_DOUBLE = pygame.transform.scale(RAW_CANNON_DOUBLE, (config.ICON_SIZE, config.ICON_SIZE))
CANNON_SMALL  = pygame.transform.scale(RAW_CANNON_SMALL,  (config.ICON_SIZE, config.ICON_SIZE))
COIN_ICON     = pygame.transform.scale(RAW_COIN_ICON,    (config.HUD_FONT_SIZE, config.HUD_FONT_SIZE))
HEART_ICON    = pygame.transform.scale(RAW_HEART_ICON,   (config.HUD_FONT_SIZE, config.HUD_FONT_SIZE))
UPGRADE_ICON  = pygame.transform.scale(RAW_UPGRADE_ICON, (config.ICON_SIZE, config.ICON_SIZE))
ICON_DAMAGE   = pygame.transform.scale(RAW_ICON_DAMAGE,   (config.ICON_SIZE, config.ICON_SIZE))
ICON_RANGE    = pygame.transform.scale(RAW_ICON_RANGE,    (config.ICON_SIZE, config.ICON_SIZE))
ICON_RELOAD   = pygame.transform.scale(RAW_ICON_RELOAD,   (config.ICON_SIZE, config.ICON_SIZE))
# projectile images
BULLET_IMG    = pygame.transform.scale(RAW_BULLET_IMG,     (20, 20))
LASER_BULLET  = pygame.transform.scale(RAW_LASER_IMG,      (20, 20))
RAW_UPGRADE_BUTTON = pygame.transform.scale(RAW_UPGRADE_BUTTON, (pw if 'pw' in globals() else 200, config.ICON_SIZE+20))  # placeholder size, will scale in draw
ENEMY_IMG     = pygame.transform.scale(RAW_ENEMY_IMG,      (config.GRID_SIZE, config.GRID_SIZE))

#Sounds
LASER_SOUNDS_SMALL = [
    pygame.mixer.Sound("assets/sounds/Laser1.mp3"),
    pygame.mixer.Sound("assets/sounds/Laser2.mp3")
]

LASER_SOUNDS_DOUBLE = [
    pygame.mixer.Sound("assets/sounds/Laser3.mp3"),
    pygame.mixer.Sound("assets/sounds/Laser4.mp3")
]

# Path
PATH = [(int(x * SCREEN_WIDTH), int(y * SCREEN_HEIGHT)) for x, y in config.PATH_PERCENTAGES_LEVEL_3]

# Helper functions
def draw_circle(screen, pos, color, radius):
    pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), radius)

def load_font(size):
    return pygame.font.SysFont(None, size)

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
            # compute angle
            self.angle = math.degrees(math.atan2(-uy, ux))

    def draw(self, screen):
        draw_angle = self.angle if self.is_laser else self.angle + 90
        rotated = pygame.transform.rotate(self.image, draw_angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect.topleft)

    def hit(self):
        return (self.x - self.target.x)**2 + (self.y - self.target.y)**2 <= self.radius**2

class Enemy:
    def __init__(self, path):
        self.alive = True
        self.path = path
        self.index = 0
        self.x, self.y = path[0]
        self.speed = config.ENEMY_SPEED
        self.health = config.ENEMY_HEALTH
        # For drawing
        self.rotated_image = ENEMY_IMG
        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def move(self):
        if self.index < len(self.path) - 1:
            tx, ty = self.path[self.index + 1]
            dx, dy = tx - self.x, ty - self.y
            dist = math.hypot(dx, dy)
            if dist:
                dx, dy = dx / dist, dy / dist
            self.x += dx * self.speed
            self.y += dy * self.speed
            if abs(self.x - tx) < self.speed and abs(self.y - ty) < self.speed:
                self.index += 1
            # Update rotation
            angle = math.degrees(math.atan2(-dy, dx)) - 90
            self.rotated_image = pygame.transform.rotate(ENEMY_IMG, angle)
            self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        # Draw the enemy
        screen.blit(self.rotated_image, self.rect.topleft)
        # Draw health bar above enemy
        bar_w = config.GRID_SIZE // 2
        bar_h = 5
        ratio = max(self.health, 0) / config.ENEMY_HEALTH
        bx = self.x - bar_w // 2
        by = self.y - 20
        pygame.draw.rect(screen, config.RED, (bx, by, bar_w, bar_h))
        pygame.draw.rect(screen, config.GREEN, (bx, by, int(bar_w * ratio), bar_h))

    def has_reached_end(self):
        return self.index >= len(self.path) - 1

    # alias for reached_end
    def reached_end(self):
        return self.has_reached_end()
        

class Tower:
    def __init__(self, x, y, ttype):
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
        self.level = 0  # Combined upgrade level
        # For double tower delayed second shot
        self.next_shot_time = None
        self._shot_perp = (0,0)
        # Load initial texture
        self._update_texture()

    def _update_texture(self):
        # Dynamically load tower image based on type and level
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
    def __init__(self):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.enemies = []
        self.towers = []
        self.occupied = set()
        # Dev Mode: placement area editor
        self.dev_mode = False
        self.drawing = False
        self.start_pos = None
        # Initialize placement cells from config
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
        # Upgrade definitions loaded from config
        self.upgrade_defs = config.TOWER_UPGRADES
        self.wave_active = False
        self.enemies_spawned = 0
        self.enemy_spawn_interval = 1000
        self.wave_cooldown = 5000
        self.last_spawn_time = 0
        self.lives = config.INITIAL_LIVES
        self.coins = config.START_COINS
        self.coin_reward = config.COIN_REWARD
        self.selected = None
        self.selected_tower = None
        self.message = ''
        self.msg_time = 0
        self.upgrade_buttons = {}
        # Upgrade definitions loaded from config
        self.upgrade_defs = config.TOWER_UPGRADES
        self.wave_active = False
        self.enemies_spawned = 0
        self.enemy_spawn_interval = 1000
        self.wave_cooldown = 5000
        self.last_spawn_time = 0
        self.volume = 5

    def spawn_enemy(self):
        self.enemies.append(Enemy(PATH))

    def _clicked_sidebar(self, x, y):
        y0 = config.ICON_PADDING*2 + COIN_ICON.get_height() + HEART_ICON.get_height()
        if config.ICON_PADDING <= x <= config.ICON_PADDING + config.ICON_SIZE:
            if y0 <= y <= y0 + config.ICON_SIZE:
                return 'double'
            if y0 + config.ICON_SIZE + config.ICON_PADDING <= y <= y0 + 2*config.ICON_SIZE + config.ICON_PADDING:
                return 'small'
        return None

    def _handle_upgrade_click(self, x, y):
        # Combined upgrade click detection aligned with drawn panel
        if not self.selected_tower:
            return False
        # Panel drawing parameters
        panel_width = 800
        visible_width = 600
        panel_x = SCREEN_WIDTH - visible_width
        panel_y = -200
        # Button parameters same as draw()
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
        pw = 200
        px = SCREEN_WIDTH - pw
        if x < px:
            return False
        # Upgrade button area
        rect = pygame.Rect(px + 10, 50, pw - 20, config.ICON_SIZE)
        if rect.collidepoint(x, y):
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
                        self.selected_tower.cooldown = max(
                            100,
                            self.selected_tower.cooldown - defs['Reload']
                        )
                        self.selected_tower.level = next_lvl
                        # Update tower texture for new level
                        self.selected_tower._update_texture()
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
                # Toggle Dev Mode (d)
                self.dev_mode = not self.dev_mode
                self.message = f"Dev Mode {'ein' if self.dev_mode else 'aus'}"
                self.msg_time = pygame.time.get_ticks()
            elif self.dev_mode and ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # Start drawing area
                self.drawing = True
                self.start_pos = pygame.mouse.get_pos()
            elif self.dev_mode and ev.type == pygame.MOUSEBUTTONUP and ev.button == 1:
                # Finish drawing; add cells
                self.drawing = False
                x0, y0 = self.start_pos
                x1, y1 = pygame.mouse.get_pos()
                gx0, gy0 = x0//config.GRID_SIZE, y0//config.GRID_SIZE
                gx1, gy1 = x1//config.GRID_SIZE, y1//config.GRID_SIZE
                for gx in range(min(gx0, gx1), max(gx0, gx1)+1):
                    for gy in range(min(gy0, gy1), max(gy0, gy1)+1):
                        self.placement_cells.add((gx, gy))
                # Persist new placement cells to config
                config.PLACEMENT_CELLS = list(self.placement_cells)
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                #percent_x = round(x / SCREEN_WIDTH, 4)
                #percent_y = round(y / SCREEN_HEIGHT, 4)
                #print(f"({percent_x}, {percent_y})")
                # Compute grid cell for placement and hover
                gx, gy = x // config.GRID_SIZE, y // config.GRID_SIZE
                # Handle upgrade panel clicks
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
                        # No tower selected?
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

        # Neue Welle starten
        if not self.wave_active:
            if now - self.last_spawn_time > self.wave_cooldown:
                self.wave_active = True
                self.enemies_spawned = 0

        # Gegner spawnen
        if self.wave_active:
            if self.enemies_spawned < 3:
                if now - self.last_spawn_time > self.enemy_spawn_interval:
                    self.spawn_enemy()
                    self.enemies_spawned += 1
                    self.last_spawn_time = now
            else:
                self.wave_active = False
                self.last_spawn_time = now

        # Gegner bewegen
        for e in self.enemies:
            e.move()

        # Türme feuern
        for t in self.towers:
            t.shoot(self.enemies, now)
            t.update()

        # Gegner entfernen (tot oder Ziel erreicht)
        for e in self.enemies[:]:
            if e.reached_end():
                self.lives -= 1
                self.enemies.remove(e)
            elif not e.alive:
                self.coins += self.coin_reward
                self.enemies.remove(e)

        # Spielende prüfen
        if self.lives <= 0:
            self.running = False



    def draw(self):
        self.screen.blit(BACKGROUND, (0,0))
        pygame.draw.rect(self.screen, config.GRAY, (0,0,config.SHOP_WIDTH,SCREEN_HEIGHT))
        # Dev overlay: show editable placement area
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
        # Coins & Lives
        self.screen.blit(COIN_ICON, (config.ICON_PADDING, config.ICON_PADDING))
        coins_txt = font.render(str(self.coins), True, config.BLACK)
        self.screen.blit(coins_txt, (config.ICON_PADDING+COIN_ICON.get_width()+5, config.ICON_PADDING))
        self.screen.blit(HEART_ICON, (config.ICON_PADDING, config.ICON_PADDING+COIN_ICON.get_height()+config.ICON_PADDING))
        lives_txt = font.render(str(self.lives), True, config.BLACK)
        self.screen.blit(lives_txt, (config.ICON_PADDING+HEART_ICON.get_width()+5, config.ICON_PADDING+COIN_ICON.get_height()+config.ICON_PADDING))
        # Tower icons
        y0 = config.ICON_PADDING*2 + COIN_ICON.get_height() + HEART_ICON.get_height()
        # draw double cannon button background and icon
        cd = config.GREEN if self.coins >= config.TOWER_CONFIG['double']['cost'] else config.RED
        pygame.draw.rect(self.screen, cd, (config.ICON_PADDING, y0, config.ICON_SIZE, config.ICON_SIZE))
        self.screen.blit(CANNON_DOUBLE, (config.ICON_PADDING, y0))
        # highlight selected tower type in blue
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
        # small cannon button
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
        # Preview and hover
        if self.selected:
            mx,my=pygame.mouse.get_pos(); gx,gy=mx//config.GRID_SIZE,my//config.GRID_SIZE
            if (gx,gy) in config.PLACEMENT_CELLS and mx>config.SHOP_WIDTH:
                img = CANNON_DOUBLE if self.selected=='double' else CANNON_SMALL
                pv = img.copy(); pv.set_alpha(150)
                rect=pv.get_rect(center=(gx*config.GRID_SIZE+config.GRID_SIZE//2,gy*config.GRID_SIZE+config.GRID_SIZE//2))
                self.screen.blit(pv,rect.topleft)
                col=config.GREEN if self.coins>=config.TOWER_CONFIG[self.selected]['cost'] and (gx,gy) not in self.occupied else config.RED
                ov=pygame.Surface((config.GRID_SIZE,config.GRID_SIZE),pygame.SRCALPHA); ov.fill((*col,100)); self.screen.blit(ov,(gx*config.GRID_SIZE,gy*config.GRID_SIZE))
        # Draw entities
        for e in self.enemies: e.draw(self.screen)
        for t in self.towers: t.draw(self.screen)
        # Upgrade panel (combined)
        if self.selected_tower:
            # Upgrade panel dimensions (extended, wider, off-screen)
            pw = 800           # panel width (extends off-screen)
            ph = SCREEN_HEIGHT + 400  # extend vertically beyond top/bottom
            visible_w = 600    # visible part width
            px = SCREEN_WIDTH - visible_w  # start so panel extends beyond right edge
            py = -200          # extend above top
            # Blit upgrade panel background image
            panel = pygame.transform.scale(RAW_UPGRADE_PANEL, (pw, ph))
            self.screen.blit(panel, (px, py))
            panel = pygame.transform.scale(RAW_UPGRADE_PANEL, (pw, ph))
            self.screen.blit(panel, (px, py))
            # Draw upgrade button inside panel
            font_small = load_font(28)
            # Determine next level and cost
            lvl = self.selected_tower.level
            next_lvl = lvl + 1 if lvl < 3 else lvl
            cost = 0
            if lvl < 3:
                cost = self.upgrade_defs[next_lvl]['cost']
            # Button rectangle relative to panel
            btn_w = pw - 40
            btn_h = config.ICON_SIZE + 20
            btn_x = px + 20
            btn_y = py + 300
            btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
            # Draw button background border
            border_color = config.GREEN if lvl < 3 and self.coins >= cost else config.RED
            # Blit upgrade button image
            button_img = pygame.transform.scale(RAW_UPGRADE_BUTTON, (btn_w, btn_h))
            self.screen.blit(button_img, (btn_x, btn_y))

            # Draw upgrade panel icon
            icon_y = btn_y + (btn_h - config.ICON_SIZE) // 2
            self.screen.blit(UPGRADE_ICON, (btn_x + 10, icon_y))
            # Draw cost with coin icon if upgradable
            if lvl < 3:
                coin_x = btn_x + 20 + config.ICON_SIZE
                self.screen.blit(COIN_ICON, (coin_x, icon_y + (config.ICON_SIZE - COIN_ICON.get_height())//2))
                cost_surf = font_small.render(str(cost), True, config.BLACK)
                self.screen.blit(cost_surf, (coin_x + COIN_ICON.get_width() + 10,
                                             icon_y + (config.ICON_SIZE - cost_surf.get_height())//2))
            # Draw button label
            label = "Upgrade" if lvl < 3 else "Maxed"
            label_surf = font_small.render(label, True, config.BLACK)
            lbl_x = btn_x + btn_w - label_surf.get_width() - 20
            lbl_y = btn_y + (btn_h - label_surf.get_height())//2
            self.screen.blit(label_surf, (lbl_x, lbl_y))
        # Message
        if self.message and pygame.time.get_ticks()-self.msg_time<2000:
            mtxt=font.render(self.message,True,config.RED); self.screen.blit(mtxt,(SCREEN_WIDTH//2-mtxt.get_width()//2,config.ICON_PADDING))
        pygame.display.flip()


    def game_over_screen(self):
        font_large = pygame.font.SysFont(None, 72)
        font_btn = pygame.font.SysFont(None, 48)

        # Hintergrundbild laden und skalieren
        bg_image = pygame.image.load("assets/images/start_screen/Background1.png").convert()
        bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        #Sounds 
        gameover_sounds = [
            pygame.mixer.Sound("assets/sounds/Fortnite.mp3"),
            pygame.mixer.Sound("assets/sounds/death-bong.mp3")
        ]
        random.choice(gameover_sounds).play()

        restart_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30), "Restart", font_btn, config.WHITE, config.RED)
        exit_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30), "Exit", font_btn, config.WHITE, config.RED)

        while True:
            self.screen.blit(bg_image, (0, 0))  # Hintergrund zeichnen

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
                        return  # Spiel neustarten
                    elif exit_btn.checkForInput(mouse_pos):
                        self.running = False
                        return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return
                    elif event.key == pygame.K_e:
                        self.running = False
                        return


    def run(self):
        while self.running:
            self.handle_events(); self.update(); self.draw(); self.clock.tick(60)
        self.game_over_screen()

if __name__=="__main__":
    TowerDefenseGame().run()
