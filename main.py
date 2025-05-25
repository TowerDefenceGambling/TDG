import pygame, sys
from button import Button
import login as login
import saveUser as su
import testGame as tg

# Initialize Pygame
pygame.init()

# Get full screen dimensions for full-screen mode
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

# Create full-screen window with double buffering and hardware acceleration
SCREEN = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
)
pygame.display.set_caption("Menu")

# Load background image
BG = pygame.image.load("assets/images/start_screen/Background1.png")
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))


def get_font(size):
    return pygame.font.Font("assets/images/start_screen/font.ttf", size)


def save_user_progress(level: int, points: int, skins: list):
    new_progress = {"level": level, "points": points, "skins": skins}
    su.update_user_progress(login.check_login_status()[1], new_progress)


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100),
            text_input="BACK",
            font=get_font(75),
            base_color="White",
            hovering_color="Green"
        )
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.flip()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")
        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100),
            text_input="BACK",
            font=get_font(75),
            base_color="Black",
            hovering_color="Green"
        )
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.flip()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        login_status, current_user = login.check_login_status()
        user_logged = "not logged in" if not login_status else current_user
        USERNAME_TEXT = get_font(15).render(f"{user_logged}", True, "White")
        USERNAME_RECT = USERNAME_TEXT.get_rect(bottomleft=(20, SCREEN_HEIGHT - 20))
        SCREEN.blit(USERNAME_TEXT, USERNAME_RECT)

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH//2, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        PLAY_BUTTON = Button(
            image=pygame.image.load("assets/images/start_screen/Play Rect.png"),
            pos=(SCREEN_WIDTH//2, 250),
            text_input="PLAY",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White"
        )
        OPTIONS_BUTTON = Button(
            image=pygame.image.load("assets/images/start_screen/Options Rect.png"),
            pos=(SCREEN_WIDTH//2, 400),
            text_input="OPTIONS",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White"
        )
        QUIT_BUTTON = Button(
            image=pygame.image.load("assets/images/start_screen/Quit Rect.png"),
            pos=(SCREEN_WIDTH//2, 550),
            text_input="QUIT",
            font=get_font(75),
            base_color="#d7fcd4",
            hovering_color="White"
        )

        # Login/Logout button
        if not login_status:
            LOGIN_BUTTON = Button(
                image=None,
                pos=(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50),
                text_input="LOGIN",
                font=get_font(45),
                base_color="White",
                hovering_color="Green"
            )
            LOGIN_BUTTON.changeColor(MENU_MOUSE_POS)
            LOGIN_BUTTON.update(SCREEN)
        else:
            LOGOUT_BUTTON = Button(
                image=None,
                pos=(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 50),
                text_input="LOGOUT",
                font=get_font(35),
                base_color="White",
                hovering_color="Green"
            )
            LOGOUT_BUTTON.changeColor(MENU_MOUSE_POS)
            LOGOUT_BUTTON.update(SCREEN)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_game = tg.TowerDefenseGame()
                    play_game.run()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if login_status and 'LOGOUT_BUTTON' in locals() and LOGOUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    login.logout()
                elif not login_status and LOGIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    login.open_login_window()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
