import pygame
import sys
import saveUser as su
from button import Button
import register as reg

# Initialize Pygame
pygame.init()

# Load background image
BG = pygame.image.load("assets/images/start_screen/Background1.png")

# Define screen dimensions and center points
screen_width = 1280
screen_height = 720
center_x = screen_width // 2
center_y = screen_height // 2

# User-related variables
user_progress = {}
user_progress_on_load = {}
is_logged_in = False
logged_in_user = None

def check_login_status():
    """
    Returns a tuple of (is_logged_in, logged_in_user).
    """
    return is_logged_in, logged_in_user
    
def logout():
    """
    Logs out the current user by resetting the global login status.
    """
    global is_logged_in, logged_in_user
    is_logged_in = False
    logged_in_user = None
    print("User logged out successfully.")

def open_login_window():
    """
    Opens the login window where users can input their credentials (username and password).
    This function displays the login screen, handles input validation, and updates the global
    USERNAME variable when a successful login occurs.
    """
    global user_progress, user_progress_on_load
    global is_logged_in, logged_in_user

    # Set up the login window
    login_screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Login")

    # Font settings
    font = pygame.font.Font("assets/images/start_screen/font.ttf", 35)
    small_font = pygame.font.Font("assets/images/start_screen/font.ttf", 25)

    # Input variables for username and password
    username = ""
    password = ""
    active_field = "username"  # Keep track of which field is active

    # Input field activation flags
    username_active = False
    password_active = False

    # Colors for active/inactive input fields
    input_box_color_active = (255, 255, 255)
    input_box_color_inactive = (150, 150, 150)

    # Input boxes dimensions
    username_box_rect = pygame.Rect(center_x - 300, 250, 600, 50)
    password_box_rect = pygame.Rect(center_x - 300, 320, 600, 50)

    # Maximum character limits for input fields
    max_username_length = 13
    max_password_length = 13

    # Tracks login attempt status
    attempt = ""

    # Flag for empty input error
    ERROR_EMPTY_TEXT = False

    # Blinking caret variables
    caret_visible = True  # Track whether caret is visible
    caret_timer = 0  # Timer to control caret blinking


    # Function to display error messages
    def error_message(message: str, color):
        ERROR_TEXT = small_font.render(message, True, color)
        ERROR_RECT = ERROR_TEXT.get_rect(center=(center_x, 400))
        login_screen.blit(ERROR_TEXT, ERROR_RECT)

    # Main loop for the login window
    while True:
        login_screen.blit(BG, (0, 0))  # Display background image

        # Handle error messages based on login attempt outcomes
        if ERROR_EMPTY_TEXT:
            error_message("Please enter a username and password.", (255, 50, 50))
        elif attempt == "Wrong password.":
            error_message("Wrong password. Please try again.", (255, 50, 50))
        elif attempt == "User not found.":
            error_message("User not found. Please register.", (255, 50, 50))
        elif attempt == "Login successful.":
            SIGN_TEXT = font.render("Login successful! Welcome!", True, (50, 255, 50))
            SIGN_RECT = SIGN_TEXT.get_rect(center=(center_x, center_y))
            login_screen.blit(SIGN_TEXT, SIGN_RECT)
            pygame.display.update()
            pygame.time.delay(2000)  # Delay to display success message
            return

        # Display login prompt
        LOGIN_TEXT = font.render("Enter Credentials", True, (255, 255, 255))
        LOGIN_RECT = LOGIN_TEXT.get_rect(center=(center_x, 100))
        login_screen.blit(LOGIN_TEXT, LOGIN_RECT)

        # Draw input boxes for username and password
        pygame.draw.rect(login_screen, input_box_color_active if username_active else input_box_color_inactive, username_box_rect, 2)
        pygame.draw.rect(login_screen, input_box_color_active if password_active else input_box_color_inactive, password_box_rect, 2)

        # Display typed username and masked password
        USERNAME_TEXT = small_font.render(f"Username: {username}", True, (255, 255, 255))
        login_screen.blit(USERNAME_TEXT, (username_box_rect.x + 10, username_box_rect.y + 13))
        PASSWORD_TEXT = small_font.render(f"Password: {'*' * len(password)}", True, (255, 255, 255))
        login_screen.blit(PASSWORD_TEXT, (password_box_rect.x + 10, password_box_rect.y + 13))

        # Blinking caret for active input fields
        current_time = pygame.time.get_ticks()
        if current_time - caret_timer > 500:  # Toggle caret visibility every 500ms
            caret_visible = not caret_visible
            caret_timer = current_time

        if username_active:
            # Get width of the username text to position caret correctly
            username_surface = small_font.render(username, True, (255, 255, 255))
            username_width = username_surface.get_width()
            if caret_visible:  # Draw caret if visible
                pygame.draw.line(login_screen, (255, 255, 255), (username_box_rect.x + 10 + username_width + 255, username_box_rect.y + 10),
                                 (username_box_rect.x + 10 + username_width + 255, username_box_rect.y + 40), 2)

        elif password_active:
            # Get width of the masked password text to position caret correctly
            password_surface = small_font.render('*' * len(password), True, (255, 255, 255))
            password_width = password_surface.get_width()
            if caret_visible:  # Draw caret if visible
                pygame.draw.line(login_screen, (255, 255, 255), (password_box_rect.x + 10 + password_width + 255, password_box_rect.y + 10),
                                 (password_box_rect.x + 10 + password_width + 255, password_box_rect.y + 40), 2)

        # Mouse position for detecting button hover effects
        LOGIN_MOUSE_POS = pygame.mouse.get_pos()

        # Buttons for login, registration, and back
        LOGIN_BUTTON = Button(image=None, pos=(center_x - 100, 450), text_input="LOGIN", font=small_font, base_color="White", hovering_color="Green")
        REGISTER_BUTTON = Button(image=None, pos=(center_x + 100, 450), text_input="REGISTER", font=small_font, base_color="White", hovering_color="Green")
        BACK_BUTTON = Button(image=None, pos=(screen_width - 100, screen_height - 50), text_input="BACK", font=small_font, base_color="White", hovering_color="Green")

        # Update button states
        for button in [LOGIN_BUTTON, REGISTER_BUTTON, BACK_BUTTON]:
            button.changeColor(LOGIN_MOUSE_POS)
            button.update(login_screen)

        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if user clicked inside username or password input boxes
                if username_box_rect.collidepoint(event.pos):
                    username_active = True
                    password_active = False
                    active_field = "username"
                elif password_box_rect.collidepoint(event.pos):
                    username_active = False
                    password_active = True
                    active_field = "password"
                else:
                    username_active = False
                    password_active = False

                # Handle button clicks
                if REGISTER_BUTTON.checkForInput(LOGIN_MOUSE_POS):
                    reg.open_register_window()  # Open registration window
                if BACK_BUTTON.checkForInput(LOGIN_MOUSE_POS):
                    return  # Exit login screen
                if LOGIN_BUTTON.checkForInput(LOGIN_MOUSE_POS):
                    if username == "" or password == "":
                        ERROR_EMPTY_TEXT = True  # Handle empty input error
                    else:
                        ERROR_EMPTY_TEXT = False
                        username = username.lower()  # Ensure username is lowercase
                        attempt = su.verify_user(username, password)  # Verify user credentials
                        if attempt == "Login successful.":
                            user_progress = su.get_user_progress(username)
                            user_progress_on_load = user_progress
                            logged_in_user = username
                            is_logged_in = True
                        else:
                            ERROR_EMPTY_TEXT = True

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
                        if username != "" and password != "":
                            username = username.lower()
                            attempt = su.verify_user(username, password)
                            if attempt == "Login successful.":
                                logged_in_user = username
                                is_logged_in = True
                                user_progress = su.get_user_progress(username)
                                user_progress_on_load = user_progress
                        else:
                            ERROR_EMPTY_TEXT = True
                    elif len(password) < max_password_length:
                        password += event.unicode

        pygame.display.update()


if __name__ == "__main__":
    open_login_window()
    pygame.quit()
    sys.exit()
