import pygame
import sys
import saveUser as su
from button import Button

# Initialize Pygame
pygame.init()

# Get full screen dimensions
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

# Create full-screen window with double buffering and hardware acceleration
SCREEN = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
)
pygame.display.set_caption("Sign Up")

# Load and scale background image
BG = pygame.image.load("assets/images/start_screen/Background1.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Center points
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2


def open_register_window():
    """
    Opens the registration window where users can create a new account.
    Handles input fields for username, password, and confirmation.
    """
    global SCREEN  # use the full-screen surface

    # Font settings
    font = pygame.font.Font("assets/images/start_screen/font.ttf", 35)
    small_font = pygame.font.Font("assets/images/start_screen/font.ttf", 25)

    # Input state
    username = ""
    password = ""
    password_2nd = ""
    active_field = "username"
    username_active = False
    password_active = False
    password_active_2nd = False

    # Colors
    input_box_active = (255, 255, 255)
    input_box_inactive = (150, 150, 150)

    # Input boxes
    box_w, box_h = 600, 50
    username_box = pygame.Rect(CENTER_X - box_w // 2, 250, box_w, box_h)
    password_box = pygame.Rect(CENTER_X - box_w // 2, 320, box_w, box_h)
    confirm_box  = pygame.Rect(CENTER_X - box_w // 2, 390, box_w, box_h)

    # Limits
    max_len = 13

    # Error flags
    attempt = None
    added = None
    ERROR_EMPTY = False
    ERROR_NO_MATCH = False

    # Caret
    caret_visible = True
    caret_timer = 0

    def error_message(msg, color):
        txt = small_font.render(msg, True, color)
        rect = txt.get_rect(center=(CENTER_X, 470))
        SCREEN.blit(txt, rect)

    # Main loop
    while True:
        SCREEN.blit(BG, (0, 0))

        # Error handling
        if ERROR_EMPTY:
            error_message("Please fill all fields!", (255, 50, 50))
        elif attempt == False:
            error_message("Username exists!", (255, 50, 50))
        elif ERROR_NO_MATCH:
            error_message("Passwords do not match!", (255, 50, 50))
        elif added:
            txt = font.render("ACCOUNT CREATED!", True, (50, 255, 50))
            rect = txt.get_rect(center=(CENTER_X, CENTER_Y))
            SCREEN.blit(txt, rect)
            pygame.display.update()
            pygame.time.delay(2000)
            return

        # Title
        title = font.render("Sign Up", True, (255, 255, 255))
        SCREEN.blit(title, title.get_rect(center=(CENTER_X, 100)))

        # Draw input boxes
        pygame.draw.rect(SCREEN, input_box_active if username_active else input_box_inactive, username_box, 2)
        pygame.draw.rect(SCREEN, input_box_active if password_active else input_box_inactive, password_box, 2)
        pygame.draw.rect(SCREEN, input_box_active if password_active_2nd else input_box_inactive, confirm_box, 2)

        # Render text inside boxes
        SCREEN.blit(small_font.render(f"Username: {username}", True, (255,255,255)),
                    (username_box.x+10, username_box.y+13))
        SCREEN.blit(small_font.render(f"Password: {'*'*len(password)}", True, (255,255,255)),
                    (password_box.x+10, password_box.y+13))
        SCREEN.blit(small_font.render(f"Confirm: {'*'*len(password_2nd)}", True, (255,255,255)),
                    (confirm_box.x+10, confirm_box.y+13))

        # Blink caret
        now = pygame.time.get_ticks()
        if now - caret_timer > 500:
            caret_visible = not caret_visible
            caret_timer = now

        # Draw caret
        if username_active and caret_visible:
            w = small_font.size(username)[0]
            x = username_box.x + 10 + w + 220
            pygame.draw.line(SCREEN, (255,255,255), (x, username_box.y+10), (x, username_box.y+40), 2)
        if password_active and caret_visible:
            w = small_font.size('*'*len(password))[0]
            x = password_box.x + 10 + w + 220
            pygame.draw.line(SCREEN, (255,255,255), (x, password_box.y+10), (x, password_box.y+40), 2)
        if password_active_2nd and caret_visible:
            w = small_font.size('*'*len(password_2nd))[0]
            x = confirm_box.x + 10 + w + 220
            pygame.draw.line(SCREEN, (255,255,255), (x, confirm_box.y+10), (x, confirm_box.y+40), 2)

        # Buttons
        mx, my = pygame.mouse.get_pos()
        create_btn = Button(None, (CENTER_X, 510), "CREATE ACCOUNT", small_font, "White", "Green")
        back_btn   = Button(None, (SCREEN_WIDTH-100, SCREEN_HEIGHT-50), "BACK", small_font, "White", "Green")
        for btn in [create_btn, back_btn]:
            btn.changeColor((mx,my))
            btn.update(SCREEN)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if username_box.collidepoint(event.pos):
                    username_active = True; password_active = False; password_active_2nd = False; active_field = 'username'
                elif password_box.collidepoint(event.pos):
                    username_active = False; password_active = True; password_active_2nd = False; active_field = 'password'
                elif confirm_box.collidepoint(event.pos):
                    username_active = False; password_active = False; password_active_2nd = True; active_field = 'confirm'
                else:
                    username_active = password_active = password_active_2nd = False

                if back_btn.checkForInput((mx,my)):
                    return
                if create_btn.checkForInput((mx,my)):
                    if not username or not password or not password_2nd:
                        ERROR_EMPTY = True; ERROR_NO_MATCH = False
                    elif password != password_2nd:
                        ERROR_NO_MATCH = True; ERROR_EMPTY = False
                    else:
                        ERROR_EMPTY = ERROR_NO_MATCH = False
                        added = su.add_user(username.lower(), password, '{"level":1,"points":0}')

            if event.type == pygame.KEYDOWN:
                if active_field == 'username' and username_active and len(username) < max_len:
                    if event.key == pygame.K_BACKSPACE: username = username[:-1]
                    elif event.key == pygame.K_RETURN: active_field='password'; username_active=False; password_active=True
                    else: username += event.unicode
                if active_field == 'password' and password_active and len(password) < max_len:
                    if event.key == pygame.K_BACKSPACE: password=password[:-1]
                    elif event.key == pygame.K_RETURN: active_field='confirm'; password_active=False; password_active_2nd=True
                    else: password += event.unicode
                if active_field == 'confirm' and password_active_2nd and len(password_2nd) < max_len:
                    if event.key == pygame.K_BACKSPACE: password_2nd=password_2nd[:-1]
                    elif event.key == pygame.K_RETURN:
                        if username and password == password_2nd:
                            added = su.add_user(username.lower(), password, '{"level":1,"points":0}')
                        else:
                            ERROR_NO_MATCH = True
                    else: password_2nd += event.unicode

        pygame.display.flip()

if __name__ == "__main__":
    open_register_window()
    pygame.quit()
    sys.exit()
