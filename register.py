import pygame
import sys
import saveUser as su
from button import Button


pygame.init()

screen_width = 1280
screen_height = 720
center_x = screen_width // 2
center_y = screen_height // 2


def open_register_window():
    # Set up the login window
    login_screen = pygame.display.set_mode((screen_width, screen_height))  # Create a login window
    pygame.display.set_caption("Login")

    font = pygame.font.Font("assets/font.ttf", 35)
    small_font = pygame.font.Font("assets/font.ttf", 25)

    # Input variables
    username = ""
    password = ""
    password_2nd = ""
    active_field = "username"  # Track which field is active

    # Input field activation flags
    username_active = False
    password_active = False
    password_active_2nd = False

    input_box_color_active = (255, 255, 255)
    input_box_color_inactive = (150, 150, 150)

    # Input boxes dimensions
    username_box_rect = pygame.Rect(center_x - 300, 250, 600, 50)
    password_box_rect = pygame.Rect(center_x - 300, 320, 600, 50)
    password_box_rect_2nd = pygame.Rect(center_x - 300, 390, 600, 50)

    # Maximum character limits for username and password fields
    max_username_length = 13
    max_password_length = 13
    max_password_2nd_length = 13

    attempt = ""
    added = None

    ERROR_EMPTY_TEXT = False
    ERROR_NO_MATCH = False

    def error_message(message: str, color):
        ERROR_TEXT = small_font.render(message, True, color)
        ERROR_RECT = ERROR_TEXT.get_rect(center=(center_x, 470))
        login_screen.blit(ERROR_TEXT, ERROR_RECT)

    while True:
        login_screen.fill((30, 30, 30))  # Set background color for the login window

        if ERROR_EMPTY_TEXT:
            error_message("Please type in a username and a Password!", (255, 50, 50))

        elif added:
            SIGN_TEXT = font.render("ACCOUT CREATED SUCCESFULLY!", True, (50, 255, 50))
            SIGN_RECT = SIGN_TEXT.get_rect(center=(center_x, center_y))
            login_screen.blit(SIGN_TEXT, SIGN_RECT)
            pygame.display.update()
            pygame.time.delay(2000)
            return

        elif added == False:
            error_message("Username already exists.", (255, 50, 50))

        elif ERROR_NO_MATCH:
            error_message("Passwords do not match.", (255, 50, 50))


        

        LOGIN_TEXT = font.render("Enter Credentials", True, (255, 255, 255))
        LOGIN_RECT = LOGIN_TEXT.get_rect(center=(center_x, 100))
        login_screen.blit(LOGIN_TEXT, LOGIN_RECT)

        # Draw input boxes
        pygame.draw.rect(login_screen, input_box_color_active if username_active else input_box_color_inactive, username_box_rect, 2)
        pygame.draw.rect(login_screen, input_box_color_active if password_active else input_box_color_inactive, password_box_rect, 2)
        pygame.draw.rect(login_screen, input_box_color_active if password_active_2nd else input_box_color_inactive, password_box_rect_2nd, 2)

        # Render the input text for username and password
        USERNAME_TEXT = small_font.render(f"Username: {username}", True, (255, 255, 255))
        login_screen.blit(USERNAME_TEXT, (username_box_rect.x + 10, username_box_rect.y + 10))

        # Mask password input with asterisks
        PASSWORD_TEXT = small_font.render(f"Password: {'*' * len(password)}", True, (255, 255, 255))
        login_screen.blit(PASSWORD_TEXT, (password_box_rect.x + 10, password_box_rect.y + 10))
        PASSWORD_TEXT_2nd = small_font.render(f"Confirm: {'*' * len(password_2nd)}", True, (255, 255, 255))
        login_screen.blit(PASSWORD_TEXT_2nd, (password_box_rect_2nd.x + 10, password_box_rect_2nd.y + 10))

        LOGIN_MOUSE_POS = pygame.mouse.get_pos()

        LOGIN_LOGIN = Button(image=None, pos=(center_x, 510), 
                            text_input="CREATE ACCOUNT", font=small_font, base_color="White", hovering_color="Green")

        LOGIN_LOGIN.changeColor(LOGIN_MOUSE_POS)
        LOGIN_LOGIN.update(login_screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the mouse is inside the username or password box
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

                if LOGIN_LOGIN.checkForInput(LOGIN_MOUSE_POS):
                    if username == "":
                            print("Please enter a username.")
                            ERROR_EMPTY_TEXT = True

                    else:
                        if password == password_2nd:
                            ERROR_NO_MATCH = False
                            ERROR_EMPTY_TEXT = False
                            print(f"Username: {username}, Password: {password}")  # Mock login attempt
                            username = username.lower()  # Convert username to lowercase
                            add = su.add_user(username, password, '{"level": 1, "points": 0}')
                            
                            if add:
                                print("Successfully added user.")
                                print(su.get_user_progress(username))
                                added = True
                                
                            else:
                                print("Username already exists.")
                                added = False
                        else:
                            print("Passwords do not match.")
                            ERROR_NO_MATCH = True

            if event.type == pygame.KEYDOWN:

                if active_field == "username" and username_active:

                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]  # Remove last character on backspace

                    elif event.key == pygame.K_RETURN:
                        # Focus switches to the password field on enter
                        username_active = False
                        password_active = True
                        password_active_2nd = False
                        active_field = "password"

                    # Add new characters if length is within the limit
                    elif len(username) < max_username_length:
                        username += event.unicode  # Append typed character to username

                elif active_field == "password" and password_active:

                    if event.key == pygame.K_BACKSPACE:
                        password = password[:-1]  # Remove last character on backspace

                    elif event.key == pygame.K_RETURN:
                        # Focus switches to the password field on enter
                        username_active = False
                        password_active = False
                        password_active_2nd = True
                        active_field = "password_2nd"

                    elif len(password) < max_password_length:
                        password+= event.unicode  # Append typed character to password


                elif active_field == "password_2nd" and password_active_2nd:

                    if event.key == pygame.K_BACKSPACE:
                        password_2nd = password_2nd[:-1]  # Remove last character on backspace

                    elif event.key == pygame.K_RETURN:
                        # Attempt login when pressing Enter on the password field
                        
                        if username == "":
                            print("Please enter a username.")
                            ERROR_EMPTY_TEXT = True

                        else:
                            if password == password_2nd:
                                ERROR_NO_MATCH = False
                                ERROR_EMPTY_TEXT = False
                                print(f"Username: {username}, Password: {password}")  # Mock login attempt
                                username = username.lower()  # Convert username to lowercase
                                add = su.add_user(username, password, '{"level": 1, "points": 0}')
                                
                                if add:
                                    print("Successfully added user.")
                                    print(su.get_user_progress(username))
                                    added = True
                                    
                                else:
                                    print("Username already exists.")
                                    added = False
                            else:
                                print("Passwords do not match.")
                                ERROR_NO_MATCH = True


                    elif len(password_2nd) < max_password_2nd_length:
                        password_2nd += event.unicode  # Append typed character to password

        pygame.display.update()

if __name__ == "__main__":
    open_register_window()
    pygame.quit()
    sys.exit()