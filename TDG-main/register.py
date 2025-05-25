import pygame
import sys
import saveUser as su
from button import Button

# Initialize Pygame
pygame.init()

# Load background image
BG = pygame.image.load("assets/images/start_screen/Background1.png")

# Define screen dimensions and center points
screen_width = 1280
screen_height = 720
center_x = screen_width // 2
center_y = screen_height // 2

def open_register_window():
    """
    Opens the registration window where users can create a new account.
    This function displays input fields for the username, password, and password confirmation.
    It also handles input validation and account creation.
    """
    # Set up the registration window
    login_screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sign Up")

    # Font settings
    font = pygame.font.Font("assets/images/start_screen/font.ttf", 35)
    small_font = pygame.font.Font("assets/images/start_screen/font.ttf", 25)

    # Input variables for username, password, and password confirmation
    username = ""
    password = ""
    password_2nd = ""
    active_field = "username"  # Keep track of which field is active

    # Input field activation flags
    username_active = False
    password_active = False
    password_active_2nd = False

    # Colors for active/inactive input fields
    input_box_color_active = (255, 255, 255)
    input_box_color_inactive = (150, 150, 150)

    # Input boxes dimensions
    username_box_rect = pygame.Rect(center_x - 300, 250, 600, 50)
    password_box_rect = pygame.Rect(center_x - 300, 320, 600, 50)
    password_box_rect_2nd = pygame.Rect(center_x - 300, 390, 600, 50)

    # Maximum character limits for input fields
    max_username_length = 13
    max_password_length = 13
    max_password_2nd_length = 13

    # Track login attempt status and account creation status
    attempt = ""
    added = None

    # Flags for error messages
    ERROR_EMPTY_TEXT = False
    ERROR_NO_MATCH = False

    # Blinking caret variables
    caret_visible = True
    caret_timer = 0

    def error_message(message: str, color):
        """
        Helper function to display error messages on the registration screen.
        :param message: The error message to display.
        :param color: The color of the error message.
        """
        ERROR_TEXT = small_font.render(message, True, color)
        ERROR_RECT = ERROR_TEXT.get_rect(center=(center_x, 470))
        login_screen.blit(ERROR_TEXT, ERROR_RECT)

    # Main loop for the registration window
    while True:
        login_screen.blit(BG, (0, 0))  # Display background image

        # Handle error messages based on account creation outcomes
        if ERROR_EMPTY_TEXT:
            error_message("Please type in a username and a Password!", (255, 50, 50))
        if added:
            SIGN_TEXT = font.render("ACCOUNT CREATED SUCCESSFULLY!", True, (50, 255, 50))
            SIGN_RECT = SIGN_TEXT.get_rect(center=(center_x, center_y))
            login_screen.blit(SIGN_TEXT, SIGN_RECT)
            pygame.display.update()
            pygame.time.delay(2000)  # Delay to display success message
            return
        elif added == False:
            error_message("Username already exists.", (255, 50, 50))
        if ERROR_NO_MATCH:
            error_message("Passwords do not match.", (255, 50, 50))

        # Display registration prompt
        LOGIN_TEXT = font.render("Sign Up", True, (255, 255, 255))
        LOGIN_RECT = LOGIN_TEXT.get_rect(center=(center_x, 100))
        login_screen.blit(LOGIN_TEXT, LOGIN_RECT)

        # Draw input boxes for username, password, and password confirmation
        pygame.draw.rect(login_screen, input_box_color_active if username_active else input_box_color_inactive, username_box_rect, 2)
        pygame.draw.rect(login_screen, input_box_color_active if password_active else input_box_color_inactive, password_box_rect, 2)
        pygame.draw.rect(login_screen, input_box_color_active if password_active_2nd else input_box_color_inactive, password_box_rect_2nd, 2)

        # Display typed username and masked password/password confirmation
        USERNAME_TEXT = small_font.render(f"Username: {username}", True, (255, 255, 255))
        login_screen.blit(USERNAME_TEXT, (username_box_rect.x + 10, username_box_rect.y + 13))
        PASSWORD_TEXT = small_font.render(f"Password: {'*' * len(password)}", True, (255, 255, 255))
        login_screen.blit(PASSWORD_TEXT, (password_box_rect.x + 10, password_box_rect.y + 13))
        PASSWORD_TEXT_2nd = small_font.render(f"Confirm: {'*' * len(password_2nd)}", True, (255, 255, 255))
        login_screen.blit(PASSWORD_TEXT_2nd, (password_box_rect_2nd.x + 10, password_box_rect_2nd.y + 13))

        # Blinking caret logic
        current_time = pygame.time.get_ticks()
        if current_time - caret_timer > 500:  # Toggle caret visibility every 500ms
            caret_visible = not caret_visible
            caret_timer = current_time

        # Draw caret in the active field
        if username_active:
            username_surface = small_font.render(username, True, (255, 255, 255))
            username_width = username_surface.get_width()
            if caret_visible:
                pygame.draw.line(login_screen, (255, 255, 255),
                                 (username_box_rect.x + 10 + username_width + 255, username_box_rect.y + 10),
                                 (username_box_rect.x + 10 + username_width + 255, username_box_rect.y + 40), 2)
        elif password_active:
            password_surface = small_font.render('*' * len(password), True, (255, 255, 255))
            password_width = password_surface.get_width()
            if caret_visible:
                pygame.draw.line(login_screen, (255, 255, 255),
                                 (password_box_rect.x + 10 + password_width + 255, password_box_rect.y + 10),
                                 (password_box_rect.x + 10 + password_width + 255, password_box_rect.y + 40), 2)
        elif password_active_2nd:
            password_2nd_surface = small_font.render('*' * len(password_2nd), True, (255, 255, 255))
            password_2nd_width = password_2nd_surface.get_width()
            if caret_visible:
                pygame.draw.line(login_screen, (255, 255, 255),
                                 (password_box_rect_2nd.x + 10 + password_2nd_width + 230, password_box_rect_2nd.y + 10),
                                 (password_box_rect_2nd.x + 10 + password_2nd_width + 230, password_box_rect_2nd.y + 40), 2)

        # Mouse position for detecting button hover effects
        LOGIN_MOUSE_POS = pygame.mouse.get_pos()

        # Buttons for creating account and going back
        CREATE_ACCOUNT_BUTTON = Button(image=None, pos=(center_x, 510), text_input="CREATE ACCOUNT", font=small_font, base_color="White", hovering_color="Green")
        BACK_BUTTON = Button(image=None, pos=(screen_width - 100, screen_height - 50), text_input="BACK", font=small_font, base_color="White", hovering_color="Green")

        # Update button states
        for button in [CREATE_ACCOUNT_BUTTON, BACK_BUTTON]:
            button.changeColor(LOGIN_MOUSE_POS)
            button.update(login_screen)

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if user clicked inside the username or password input boxes
                if username_box_rect.collidepoint(event.pos):
                    username_active = True
                    password_active = False
                    password_active_2nd = False
                    active_field = "username"
                elif password_box_rect.collidepoint(event.pos):
                    username_active = False
                    password_active = True
                    password_active_2nd = False
                    active_field = "password"
                elif password_box_rect_2nd.collidepoint(event.pos):
                    username_active = False
                    password_active = False
                    password_active_2nd = True
                    active_field = "password_2nd"
                else:
                    username_active = False
                    password_active = False
                    password_active_2nd = False

                # Handle button clicks
                if BACK_BUTTON.checkForInput(LOGIN_MOUSE_POS):
                    return  # Exit registration screen
                if CREATE_ACCOUNT_BUTTON.checkForInput(LOGIN_MOUSE_POS):
                    if username == "":
                        ERROR_EMPTY_TEXT = True  # Handle empty input error
                    else:
                        if password == password_2nd:
                            ERROR_NO_MATCH = False
                            ERROR_EMPTY_TEXT = False
                            username = username.lower()  # Ensure username is lowercase
                            add = su.add_user(username, password, '{"level": 1, "points": 0}')
                            if add:
                                added = True  # Account creation success
                            else:
                                added = False  # Username already exists
                        else:
                            ERROR_NO_MATCH = True  # Passwords do not match

            # Handle keyboard input for username and password fields
            if event.type == pygame.KEYDOWN:
                if active_field == "username" and username_active:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN:
                        active_field = "password"
                        username_active = False
                        password_active = True
                    elif len(username) < max_username_length:
                        username += event.unicode
                elif active_field == "password" and password_active:
                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]
                    elif event.key == pygame.K_RETURN:
                        active_field = "password_2nd"
                        password_active = False
                        password_active_2nd = True
                    elif len(password) < max_password_length:
                        password += event.unicode
                elif active_field == "password_2nd" and password_active_2nd:
                    if event.key == pygame.K_BACKSPACE:
                        password_2nd = password_2nd[:-1]
                    elif event.key == pygame.K_RETURN:
                        if username == "":
                            ERROR_EMPTY_TEXT = True  # Handle empty input error
                        else:
                            if password == password_2nd:
                                ERROR_NO_MATCH = False
                                ERROR_EMPTY_TEXT = False
                                username = username.lower()  # Ensure username is lowercase
                                add = su.add_user(username, password, '{"level": 1, "points": 0}')
                                if add:
                                    added = True  # Account creation success
                                else:
                                    added = False  # Username already exists
                            else:
                                ERROR_EMPTY_TEXT = False
                                ERROR_NO_MATCH = True  # Passwords do not match
                    elif len(password_2nd) < max_password_2nd_length:
                        password_2nd += event.unicode

        pygame.display.update()

if __name__ == "__main__":
    open_register_window()
    pygame.quit()
    sys.exit()
