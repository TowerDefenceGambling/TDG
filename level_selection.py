import pygame
from button import Button

def level_selection():
    from main import SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, get_font, main_menu, BG
    import testGame as tg  # <--- Import ergänzen
    running = True
    while running:
        SCREEN.blit(BG, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Level Buttons
        level1_btn = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 200),
            text_input="Level 1",
            font=get_font(50),
            base_color="Black",
            hovering_color="Green"
        )
        level2_btn = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 300),
            text_input="Level 2",
            font=get_font(50),
            base_color="Black",
            hovering_color="Green"
        )
        level3_btn = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 400),
            text_input="Level 3",
            font=get_font(50),
            base_color="Black",
            hovering_color="Green"
        )
        back_btn = Button(
            image=None,
            pos=(SCREEN_WIDTH//2, 500),
            text_input="BACK",
            font=get_font(50),
            base_color="Black",
            hovering_color="Green"
        )

        for btn in [level1_btn, level2_btn, level3_btn, back_btn]:
            btn.changeColor(mouse_pos)
            btn.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_btn.checkForInput(mouse_pos):
                    running = False
                    tg.TowerDefenseGame().run()  # <--- Spiel starten
                if back_btn.checkForInput(mouse_pos):
                    running = False
                    main_menu()

        pygame.display.flip()