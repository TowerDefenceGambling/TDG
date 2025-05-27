import pygame, sys
from button import Button
import login as login
import saveUser as su
import testGame as tg
import json
import os
from level_selection import level_selection

SETTINGS_FILE = "settings.json"

# Initialize Pygame
pygame.init()
pygame.mixer.init()

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


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    else:
        return {
            "language": "Deutsch",
            "sound_on": True,
            "volume": 50
        }

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)


def play_background_music(volume, sound_on=True):
    music_path = "assets/sounds/Rettungsschwimmer.mp3"
    if os.path.exists(music_path):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume / 100 if sound_on else 0)
            if sound_on:
                pygame.mixer.music.play(-1)
    else:
        print(f"Warnung: Musikdatei nicht gefunden: {music_path}")


def get_font(size):
    return pygame.font.Font("assets/images/start_screen/font.ttf", size)


def save_user_progress(level: int, points: int, skins: list):
    new_progress = {"level": level, "points": points, "skins": skins}
    su.update_user_progress(login.check_login_status()[1], new_progress)


def play():
    settings = load_settings()
    play_background_music(settings["volume"], settings["sound_on"])

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
    settings = load_settings()
    selected_language = settings.get("language", "Deutsch")
    sound_on = settings.get("sound_on", True)
    volume = settings.get("volume", 50)

    languages = ["Deutsch", "English"]

    pygame.mixer.music.set_volume(volume / 100 if sound_on else 0)
    if sound_on:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("Options", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH//2, 50))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        lang_buttons = []
        for i, lang in enumerate(languages):
            btn = Button(
                image=None,
                pos=(SCREEN_WIDTH//2, 200 + i*80),
                text_input=lang,
                font=get_font(40),
                base_color="Green" if lang == selected_language else "Black",
                hovering_color="Green"
            )
            btn.changeColor(OPTIONS_MOUSE_POS)
            btn.update(SCREEN)
            lang_buttons.append((btn, lang))

        sound_text = get_font(30).render("Sound:", True, "Black")
        sound_rect = sound_text.get_rect(center=(SCREEN_WIDTH//2, 400))
        SCREEN.blit(sound_text, sound_rect)

        sound_status = "An" if sound_on else "Aus"
        sound_button = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 450),
            text_input=sound_status,
            font=get_font(40),
            base_color="Green" if sound_on else "Black",
            hovering_color="Green"
        )
        sound_button.changeColor(OPTIONS_MOUSE_POS)
        sound_button.update(SCREEN)

        volume_label = get_font(30).render("Lautstärke", True, "Black")
        volume_label_rect = volume_label.get_rect(center=(SCREEN_WIDTH//2, 520))
        SCREEN.blit(volume_label, volume_label_rect)

        volume_text = get_font(40).render(str(volume), True, "Black")
        volume_text_rect = volume_text.get_rect(center=(SCREEN_WIDTH//2, 560))
        SCREEN.blit(volume_text, volume_text_rect)

        vol_down = Button(
            image=None,
            pos=(SCREEN_WIDTH//2 - 100, 560),
            text_input="-",
            font=get_font(40),
            base_color="Black",
            hovering_color="Green"
        )
        vol_up = Button(
            image=None,
            pos=(SCREEN_WIDTH//2 + 100, 560),
            text_input="+",
            font=get_font(40),
            base_color="Black",
            hovering_color="Green"
        )
        vol_down.changeColor(OPTIONS_MOUSE_POS)
        vol_down.update(SCREEN)
        vol_up.changeColor(OPTIONS_MOUSE_POS)
        vol_up.update(SCREEN)

        SAVE_BUTTON = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 180),
            text_input="SAVE",
            font=get_font(50),
            base_color="Black",
            hovering_color="Green"
        )
        SAVE_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        SAVE_BUTTON.update(SCREEN)

        OPTIONS_BACK = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100),
            text_input="BACK",
            font=get_font(50),
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
                for btn, lang in lang_buttons:
                    if btn.checkForInput(OPTIONS_MOUSE_POS):
                        selected_language = lang
                        settings["language"] = selected_language
                        print(f"Sprache gewechselt zu {lang}")

                if sound_button.checkForInput(OPTIONS_MOUSE_POS):
                    sound_on = not sound_on
                    settings["sound_on"] = sound_on
                    if sound_on:
                        if not pygame.mixer.music.get_busy():
                            pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(volume / 100)
                    else:
                        pygame.mixer.music.stop()
                    print(f"Sound {'an' if sound_on else 'aus'}")

                if vol_up.checkForInput(OPTIONS_MOUSE_POS):
                    if volume < 100:
                        volume += 10
                        settings["volume"] = volume
                        if sound_on:
                            pygame.mixer.music.set_volume(volume / 100)
                        print(f"Lautstärke erhöht auf {volume}")

                if vol_down.checkForInput(OPTIONS_MOUSE_POS):
                    if volume > 0:
                        volume -= 10
                        settings["volume"] = volume
                        if sound_on:
                            pygame.mixer.music.set_volume(volume / 100)
                        print(f"Lautstärke verringert auf {volume}")

                if SAVE_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    save_settings(settings)
                    print("Einstellungen gespeichert!")

                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.flip()


def main_menu():
    settings = load_settings()
    play_background_music(settings["volume"], settings["sound_on"])

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
                    level_selection()
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