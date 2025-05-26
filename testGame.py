import pygame
import random
import math
import sys
import config
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
BACKGROUND = pygame.image.load("assets/images/level1/tiles.png")
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
RAW_CANNON_DOUBLE = pygame.image.load("assets/images/tower/Cannon3.png")
RAW_CANNON_SMALL  = pygame.image.load("assets/images/tower/Cannon2.png")
RAW_COIN_ICON     = pygame.image.load("assets/images/level1/coin.png")
RAW_HEART_ICON    = pygame.image.load("assets/images/level1/heart_icon.png")
# Upgrade icons
RAW_ICON_DAMAGE   = pygame.image.load("assets/images/level1/damage_icon.png")
RAW_ICON_RANGE    = pygame.image.load("assets/images/level1/sniper_icon.png")
RAW_ICON_RELOAD   = pygame.image.load("assets/images/level1/magazine_icon.png")
BULLET_IMG        = pygame.image.load("assets/images/tower/bullet_cannon.png")
#Enemy
RAW_ENEMY_IMG = pygame.image.load("assets/images/enemy/enemy_1.png")
ENEMY_IMG = pygame.transform.scale(RAW_ENEMY_IMG, (config.GRID_SIZE, config.GRID_SIZE))

# Scale icons
CANNON_DOUBLE = pygame.transform.scale(RAW_CANNON_DOUBLE, (config.ICON_SIZE, config.ICON_SIZE))
CANNON_SMALL  = pygame.transform.scale(RAW_CANNON_SMALL,  (config.ICON_SIZE, config.ICON_SIZE))
COIN_ICON     = pygame.transform.scale(RAW_COIN_ICON,    (config.HUD_FONT_SIZE, config.HUD_FONT_SIZE))
HEART_ICON    = pygame.transform.scale(RAW_HEART_ICON,   (config.HUD_FONT_SIZE, config.HUD_FONT_SIZE))
ICON_DAMAGE   = pygame.transform.scale(RAW_ICON_DAMAGE,   (config.ICON_SIZE, config.ICON_SIZE))
ICON_RANGE    = pygame.transform.scale(RAW_ICON_RANGE,    (config.ICON_SIZE, config.ICON_SIZE))
ICON_RELOAD   = pygame.transform.scale(RAW_ICON_RELOAD,   (config.ICON_SIZE, config.ICON_SIZE))

# Precompute path
PATH = [(int(x * SCREEN_WIDTH), int(y * SCREEN_HEIGHT)) for x, y in config.PATH_PERCENTAGES]

# Helper functions
def draw_circle(screen, pos, color, radius):
    pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), radius)

def load_font(size):
    return pygame.font.SysFont(None, size)

class Enemy:
    def __init__(self, path):
        self.path = path
        self.index = 0
        self.x, self.y = path[0]
        self.speed = config.ENEMY_SPEED
        self.health = config.ENEMY_HEALTH
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rotated_image = self.image 

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
            self.rect.center = (self.x, self.y)

            angle = math.degrees(math.atan2(-dy, dx)) - 90  # -90 weil die Grafik sonst "nach rechts" schaut
            self.rotated_image = pygame.transform.rotate(ENEMY_IMG, angle)
            self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        bw = config.GRID_SIZE // 2
        bh = 5
        ratio = max(self.health, 0) / config.ENEMY_HEALTH
        bx = self.x - bw // 2
        by = self.y - 20
        pygame.draw.rect(screen, config.RED, (bx, by, bw, bh))
        pygame.draw.rect(screen, config.GREEN, (bx, by, int(bw * ratio), bh))
        screen.blit(self.rotated_image, self.rect.topleft)

    def reached_end(self):
        return self.index >= len(self.path) - 1

class Bullet:
    def __init__(self, x, y, target):
        self.x, self.y = x, y
        self.target = target
        self.speed = getattr(target, 'bullet_speed', 10)
        self.image = pygame.transform.scale(BULLET_IMG, (20, 20))
        self.radius = 10

    def move(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist:
            dx, dy = dx / dist, dy / dist
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, screen):
        screen.blit(self.image, (int(self.x - 10), int(self.y - 10)))

    def hit(self):
        return (self.x - self.target.x)**2 + (self.y - self.target.y)**2 <= self.radius**2

class Tower:
    def __init__(self, x, y, ttype):
        self.x, self.y = x, y
        cfg = config.TOWER_CONFIG[ttype]
        self.cost = cfg['cost']
        self.range = cfg['range']
        self.cooldown = cfg['cooldown']
        self.damage = cfg['damage']
        self.last_shot = 0
        self.bullets = []
        self.target = None
        self.image = CANNON_DOUBLE if ttype == 'double' else CANNON_SMALL

    def shoot(self, enemies, now):
        if now - self.last_shot >= self.cooldown:
            for e in enemies:
                if (e.x - self.x)**2 + (e.y - self.y)**2 <= self.range**2:
                    self.bullets.append(Bullet(self.x, self.y, e))
                    self.target = e
                    self.last_shot = now
                    break

    def update(self):
        for b in self.bullets[:]:
            b.move()
            if b.hit():
                b.target.health -= self.damage
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
        # Load upgrade definitions from config
        self.upgrade_defs = config.TOWER_UPGRADES

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
        if not self.selected_tower:
            return False
        pw = 260
        px = SCREEN_WIDTH - pw
        if x < px:
            return False
        for opt, rect in self.upgrade_buttons.items():
            if rect.collidepoint(x, y):
                d = self.upgrade_defs[opt]
                cost = d['cost']
                if self.coins >= cost:
                    self.coins -= cost
                    if 'increment' in d:
                        setattr(self.selected_tower, opt.lower(), getattr(self.selected_tower, opt.lower()) + d['increment'])
                    else:
                        self.selected_tower.cooldown = max(100, self.selected_tower.cooldown - d['decrement'])
                else:
                    self.message = f"Upgrade benötigt: {cost} Münzen"
                    self.msg_time = pygame.time.get_ticks()
                return True
        return False

    def handle_events(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.running = False
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                self.pause_menu()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
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
                if x > config.SHOP_WIDTH:
                    if not self.selected:
                        self.message = "Bitte Turm auswählen"
                        self.msg_time = pygame.time.get_ticks()
                        return
                    gx, gy = x//config.GRID_SIZE, y//config.GRID_SIZE
                    if (gx, gy) in config.PLACEMENT_CELLS:
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
        if now - self.spawn_timer > self.spawn_interval:
            self.spawn_enemy()
            self.spawn_timer = now
        for e in self.enemies:
            e.move()
        for t in self.towers:
            t.shoot(self.enemies, now)
            t.update()
        for e in self.enemies[:]:
            if e.reached_end():
                self.lives -= 1
                self.enemies.remove(e)
            elif e.health <= 0:
                self.coins += self.coin_reward
                self.enemies.remove(e)
        if self.lives <= 0:
            self.running = False

    def draw(self):
        self.screen.blit(BACKGROUND, (0,0))
        pygame.draw.rect(self.screen, config.GRAY, (0,0,config.SHOP_WIDTH,SCREEN_HEIGHT))
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
        cd = config.GREEN if self.coins>=config.TOWER_CONFIG['double']['cost'] else config.RED
        pygame.draw.rect(self.screen,cd,(config.ICON_PADDING,y0,config.ICON_SIZE,config.ICON_SIZE)); self.screen.blit(CANNON_DOUBLE,(config.ICON_PADDING,y0))
        y1=y0+config.ICON_SIZE+config.ICON_PADDING; cs=config.GREEN if self.coins>=config.TOWER_CONFIG['small']['cost'] else config.RED
        pygame.draw.rect(self.screen,cs,(config.ICON_PADDING,y1,config.ICON_SIZE,config.ICON_SIZE)); self.screen.blit(CANNON_SMALL,(config.ICON_PADDING,y1))
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
        # Upgrade panel
        if self.selected_tower:
            pw=260; px=SCREEN_WIDTH-pw
            pygame.draw.rect(self.screen,config.WHITE,(px,0,pw,SCREEN_HEIGHT))
            font_small=load_font(24)
            y=20
            for key, icon in [('Damage',ICON_DAMAGE),('Range',ICON_RANGE),('Reload',ICON_RELOAD)]:
                self.screen.blit(icon,(px+10,y))
                cost=self.upgrade_defs[key]['cost']
                cost_txt=font_small.render(f"{cost}",True,config.BLACK)
                self.screen.blit(COIN_ICON,(px+10+icon.get_width()+5,y+(icon.get_height()-COIN_ICON.get_height())//2))
                self.screen.blit(cost_txt,(px+10+icon.get_width()+5+COIN_ICON.get_width()+2,y+(icon.get_height()-cost_txt.get_height())//2))
                rect=pygame.Rect(px+10,y,pw-20,icon.get_height())
                pygame.draw.rect(self.screen,config.GREEN,rect,2); self.upgrade_buttons[key]=rect; y+=icon.get_height()+15
        # Message
        if self.message and pygame.time.get_ticks()-self.msg_time<2000:
            mtxt=font.render(self.message,True,config.RED); self.screen.blit(mtxt,(SCREEN_WIDTH//2-mtxt.get_width()//2,config.ICON_PADDING))
        pygame.display.flip()

    def pause_menu(self):
        paused = True
        font_large = pygame.font.SysFont(None, 72)
        font_btn = pygame.font.SysFont(None, 48)

        resume_btn = Button(None, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 90), "Resume", font_btn, config.WHITE, config.RED)
        options_btn = Button(None, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30), "Options", font_btn, config.WHITE, config.RED)
        exit_btn = Button(None, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30), "Exit", font_btn, config.WHITE, config.RED)

        options_menu = False
        volume = getattr(self, 'volume', 5)  # falls self.volume schon existiert, sonst 5

        while paused:
            self.screen.fill((50, 50, 50))
            t = font_large.render("PAUSED", True, config.WHITE)
            self.screen.blit(t, t.get_rect(center=(SCREEN_WIDTH//2, 150)))

            mpos = pygame.mouse.get_pos()

            if not options_menu:
                for b in [resume_btn, options_btn, exit_btn]:
                    b.changeColor(mpos)
                    b.update(self.screen)
                pygame.display.flip()

                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if resume_btn.checkForInput(mpos):
                            paused = False
                        elif options_btn.checkForInput(mpos):
                            options_menu = True
                        elif exit_btn.checkForInput(mpos):
                            self.running = False
                            return
            else:
                # Options-Menü mit Lautstärke-Regler
                self.screen.fill((30, 30, 30))
                opt_title = font_large.render("OPTIONS", True, config.WHITE)
                self.screen.blit(opt_title, opt_title.get_rect(center=(SCREEN_WIDTH//2, 150)))

                vol_text = font_btn.render(f"Volume: {volume}", True, config.WHITE)
                self.screen.blit(vol_text, (SCREEN_WIDTH//2 - vol_text.get_width()//2, SCREEN_HEIGHT//2 - 30))

                back_btn = Button(None, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60), "Back", font_btn, config.WHITE, config.RED)
                back_btn.changeColor(mpos)
                back_btn.update(self.screen)
                pygame.display.flip()

                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_UP and volume < 10:
                            volume += 1
                            self.set_volume(volume)
                        elif ev.key == pygame.K_DOWN and volume > 0:
                            volume -= 1
                            self.set_volume(volume)
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if back_btn.checkForInput(mpos):
                            options_menu = False

        self.volume = volume  # Lautstärke speichern


    def game_over_screen(self):
        font_large = pygame.font.SysFont(None, 72)
        font_btn = pygame.font.SysFont(None, 48)
        restart_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60), "Restart", font_btn, config.WHITE, config.RED)
        options_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), "Options", font_btn, config.WHITE, config.RED)
        exit_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60), "Exit", font_btn, config.WHITE, config.RED)

        while True:
            self.screen.fill((0, 0, 0))
            title_surf = font_large.render("GAME OVER", True, config.RED)
            self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150)))

            mouse_pos = pygame.mouse.get_pos()
            for btn in [restart_btn, options_btn, exit_btn]:
                btn.changeColor(mouse_pos)
                btn.update(self.screen)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_btn.checkForInput(mouse_pos):
                        return  # restart game
                    elif options_btn.checkForInput(mouse_pos):
                        self.show_options()
                    elif exit_btn.checkForInput(mouse_pos):
                        self.running = False
                        return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return
                    elif event.key == pygame.K_o:
                        self.show_options()
                    elif event.key == pygame.K_e:
                        self.running = False
                        return

    def show_options(self):
        # Einfaches Optionsmenü als Platzhalter
        font_large = pygame.font.SysFont(None, 72)
        font_btn = pygame.font.SysFont(None, 48)
        back_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100), "Back", font_btn, config.WHITE, config.RED)

        while True:
            self.screen.fill((30, 30, 30))
            title_surf = font_large.render("OPTIONS", True, config.WHITE)
            self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150)))

            mouse_pos = pygame.mouse.get_pos()
            back_btn.changeColor(mouse_pos)
            back_btn.update(self.screen)

            # Hier kannst du weitere Options-Elemente hinzufügen

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_btn.checkForInput(mouse_pos):
                        return  # zurück zum Game Over Screen

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return


    def run(self):
        while self.running:
            self.handle_events(); self.update(); self.draw(); self.clock.tick(60)
        self.game_over_screen()

if __name__=="__main__":
    TowerDefenseGame().run()
