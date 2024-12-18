import pygame, sys
from button import Button
import login as login
import saveUser as su
import testGame as tg

pygame.init()

user_progress_on_load = login.user_progress  # {'level': 1, 'points': 0} etc...

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/images/start_screen/Background1.png")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/images/start_screen/font.ttf", size)


def save_user_progress(level: int, points: int, skins: list):
    new_progress = {
        "level": level,
        "points": points,
        "skins": skins
    }
    su.update_user_progress(login.check_login_status()[1], new_progress)


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                           text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        # Get the updated login status and logged-in username
        login_status, current_user = login.check_login_status()
        user_logged = "not logged in" if login_status is False else current_user

        USERNAME_TEXT = get_font(15).render(f"{user_logged}", True, "White")
        USERNAME_RECT = USERNAME_TEXT.get_rect(bottomleft=(20, 690))
        SCREEN.blit(USERNAME_TEXT, USERNAME_RECT)

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/images/start_screen/Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/start_screen/Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/images/start_screen/Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # Handle login or logout button display
        if not login_status:
            LOGIN_BUTTON = Button(image=None, pos=(1100, 670),
                                  text_input="LOGIN", font=get_font(45), base_color="White", hovering_color="Green")
            LOGIN_BUTTON.changeColor(MENU_MOUSE_POS)
            LOGIN_BUTTON.update(SCREEN)
        else:
            LOGOUT_BUTTON = Button(image=None, pos=(1100, 670),
                                   text_input="LOGOUT", font=get_font(35), base_color="White", hovering_color="Green")
            LOGOUT_BUTTON.changeColor(MENU_MOUSE_POS)
            LOGOUT_BUTTON.update(SCREEN)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play = tg.TowerDefenseGame()
                    play.run()

                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()

                if login_status and 'LOGOUT_BUTTON' in locals() and LOGOUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    login.logout()
                    login_status, current_user = login.check_login_status()  # Refresh status after logout
                    print(login_status, current_user)
                
                elif not login_status and LOGIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    login.open_login_window()
                    login_status, current_user = login.check_login_status()  # Refresh status after login
                    print(login_status, current_user)
                    

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()
