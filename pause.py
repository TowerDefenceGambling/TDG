import pygame
import sys
import config
from button import Button
from main import load_settings
from main import save_settings
import json


# Verwende hier ggf. auch globale Konstanten SCREEN_WIDTH und SCREEN_HEIGHT
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h


def load_translations():
    with open("translations.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
class Pause:
    def __init__(self, game):
            self.game = game
            self.screen = game.screen
            self.volume = getattr(game, 'volume', 5)
            
            self.settings = load_settings()
            self.language = self.settings.get("language", "Deutsch")
            self.translations = load_translations()

            self.bg_image = pygame.image.load("assets/images/start_screen/Background1.png").convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


    def t(self, key):
        # Übersetzt anhand der aktuellen Sprache
        return self.translations.get(self.language, {}).get(key, key)

    def pause_menu(self):
        paused = True
        font_large = pygame.font.SysFont(None, 72)
        font_btn = pygame.font.SysFont(None, 48)

        # Update Sprache aus Einstellungen (falls sie sich geändert hat)
        self.settings = load_settings()
        self.language = self.settings.get("language", "Deutsch")

        # Jetzt Texte dynamisch laden
        text_paused = self.t("paused")
        text_resume = self.t("resume")
        text_options = self.t("options")
        text_exit = self.t("exit")
        text_back = self.t("back")

        resume_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90), text_resume, font_btn, config.WHITE, config.RED)
        options_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30), text_options, font_btn, config.WHITE, config.RED)
        exit_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30), text_exit, font_btn, config.WHITE, config.RED)
        back_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60), text_back, font_btn, config.WHITE, config.RED)

        options_menu = False

        while paused:
            mpos = pygame.mouse.get_pos()
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if not options_menu:
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if resume_btn.checkForInput(mpos):
                            paused = False
                        elif options_btn.checkForInput(mpos):
                            self.show_options()

                            # Sprache neu laden nach Optionsmenü
                            self.settings = load_settings()
                            self.language = self.settings.get("language", "Deutsch")

                            # Texte neu laden
                            text_paused = self.t("paused")
                            text_resume = self.t("resume")
                            text_options = self.t("options")
                            text_exit = self.t("exit")
                            text_back = self.t("back")

                            # Buttons mit neuen Texten neu erstellen
                            resume_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 90), text_resume, font_btn, config.WHITE, config.RED)
                            options_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30), text_options, font_btn, config.WHITE, config.RED)
                            exit_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30), text_exit, font_btn, config.WHITE, config.RED)
                            back_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60), text_back, font_btn, config.WHITE, config.RED)

                        elif exit_btn.checkForInput(mpos):
                            from main import main_menu
                            main_menu()
                            return

                else:
                    if ev.type == pygame.KEYDOWN:
                        if ev.key == pygame.K_UP and self.volume < 10:
                            self.volume += 1
                            self.game.set_volume(self.volume)
                        elif ev.key == pygame.K_DOWN and self.volume > 0:
                            self.volume -= 1
                            self.game.set_volume(self.volume)
                    if ev.type == pygame.MOUSEBUTTONDOWN:
                        if back_btn.checkForInput(mpos):
                            options_menu = False

            self.screen.blit(self.bg_image, (0, 0))
            if not options_menu:
                t = font_large.render(text_paused, True, config.WHITE)
                self.screen.blit(t, t.get_rect(center=(SCREEN_WIDTH // 2, 150)))
                for b in [resume_btn, options_btn, exit_btn]:
                    b.changeColor(mpos)
                    b.update(self.screen)
            else:
                opt_title = font_large.render(text_options.upper(), True, config.WHITE)
                self.screen.blit(opt_title, opt_title.get_rect(center=(SCREEN_WIDTH // 2, 150)))
                vol_text = font_btn.render(f"{self.t('volume')}: {self.volume}", True, config.WHITE)
                self.screen.blit(vol_text, (SCREEN_WIDTH // 2 - vol_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
                back_btn.changeColor(mpos)
                back_btn.update(self.screen)

            pygame.display.flip()

        self.game.volume = self.volume


    def show_options(self):
        settings = load_settings()
        selected_language = settings.get("language", "Deutsch")
        sound_on = settings.get("sound_on", True)
        volume = settings.get("volume", 50)

        self.languages = ["Deutsch", "English"]

        font_large = pygame.font.SysFont(None, 60)
        font = pygame.font.SysFont(None, 40)

        pygame.mixer.music.set_volume(volume / 100 if sound_on else 0)
        if sound_on and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
        elif not sound_on:
            pygame.mixer.music.stop()

        running = True
        while running:
            mpos = pygame.mouse.get_pos()
            self.screen.blit(self.bg_image, (0, 0))

            # Titel
            title = font_large.render(self.t("options"), True, config.WHITE)
            self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 50)))

            # Sprache
            lang_buttons = []
            for i, lang in enumerate(self.languages):
                btn = Button(
                    image=None,
                    pos=(SCREEN_WIDTH // 2, 150 + i * 50),
                    text_input=lang,
                    font=font,
                    base_color="Green" if lang == selected_language else "White",
                    hovering_color="Green"
                )
                btn.changeColor(mpos)
                btn.update(self.screen)
                lang_buttons.append((btn, lang))

            # Sound an/aus
            sound_label = font.render(self.t("sound"), True, config.WHITE)
            self.screen.blit(sound_label, sound_label.get_rect(center=(SCREEN_WIDTH // 2, 270)))

            sound_button = Button(
                image=None,
                pos=(SCREEN_WIDTH // 2, 310),
                text_input=self.t("on") if sound_on else self.t("off"),
                font=font,
                base_color="Green" if sound_on else "White",
                hovering_color="Green"
            )
            sound_button.changeColor(mpos)
            sound_button.update(self.screen)

            # Lautstärke
            vol_label = font.render(self.t("volume"), True, config.WHITE)
            self.screen.blit(vol_label, vol_label.get_rect(center=(SCREEN_WIDTH // 2, 370)))

            vol_value = font.render(str(volume), True, config.WHITE)
            self.screen.blit(vol_value, vol_value.get_rect(center=(SCREEN_WIDTH // 2, 410)))

            vol_down = Button(None, (SCREEN_WIDTH // 2 - 100, 410), "-", font, config.WHITE, "Green")
            vol_up = Button(None, (SCREEN_WIDTH // 2 + 100, 410), "+", font, config.WHITE, "Green")
            vol_down.changeColor(mpos)
            vol_down.update(self.screen)
            vol_up.changeColor(mpos)
            vol_up.update(self.screen)

            # Buttons unten
            save_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120), self.t("save"), font, config.WHITE, "Green")
            back_btn = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60), self.t("back"), font, config.WHITE, "Green")
            save_btn.changeColor(mpos)
            save_btn.update(self.screen)
            back_btn.changeColor(mpos)
            back_btn.update(self.screen)

            # Events
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if ev.type == pygame.MOUSEBUTTONDOWN:
                    for btn, lang in lang_buttons:
                        if btn.checkForInput(mpos):
                            selected_language = lang
                            settings["language"] = selected_language

                    if sound_button.checkForInput(mpos):
                        sound_on = not sound_on
                        settings["sound_on"] = sound_on
                        if sound_on:
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(volume / 100)
                        else:
                            pygame.mixer.music.stop()

                    if vol_up.checkForInput(mpos) and volume < 100:
                        volume += 10
                        settings["volume"] = volume
                        if sound_on:
                            pygame.mixer.music.set_volume(volume / 100)

                    if vol_down.checkForInput(mpos) and volume > 0:
                        volume -= 10
                        settings["volume"] = volume
                        if sound_on:
                            pygame.mixer.music.set_volume(volume / 100)

                    if save_btn.checkForInput(mpos):
                        save_settings(settings)
                        self.settings = load_settings()
                        self.language = self.settings.get("language", "Deutsch")

                    if back_btn.checkForInput(mpos):
                        running = False

            pygame.display.flip()

