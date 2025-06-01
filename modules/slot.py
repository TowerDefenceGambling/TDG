import pygame
import random
import math  # Import the math module for trigonometric functions
import os

# Initialisierung
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Initialize the screen in fullscreen mode
pygame.display.set_caption("Retro Slotmaschine")

clock = pygame.time.Clock()
running = True

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (50, 50, 50)  # Darker background color
GOLD = (255, 215, 0)
BOX_COLOR = (200, 200, 200)  # Light gray for the boxes

# Symbole
def scale_image(image, height):
    aspect_ratio = image.get_width() / image.get_height()
    width = int(height * aspect_ratio)
    return pygame.transform.scale(image, (width, height))

def load_image(filepath, height):
    """Load an image and scale it to the specified height."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Image file not found: {filepath}")
    image = pygame.image.load(filepath)
    return scale_image(image, height)

symbols = [
    load_image('c:/Users/VWPE11T/new Website/modules/static/zitroneSlot.png', 60),  # Smaller Zitrone
    load_image('c:/Users/VWPE11T/new Website/modules/static/kirscheS.png', 60),  # Smaller Kirsche
    load_image('c:/Users/VWPE11T/new Website/modules/static/berry.png', 60),  # Smaller Berry
    load_image('c:/Users/VWPE11T/new Website/modules/static/melone.png', 60),  # Smaller Melone
]

# Load explosion image
explosion_image = load_image('c:/Users/VWPE11T/new Website/modules/static/explosion.png', 60)

# Sounds
try:
    win_sound = pygame.mixer.Sound('c:/Users/VWPE11T/new Website/modules/static/slotWin.wav')
    spin_sound = pygame.mixer.Sound('c:/Users/VWPE11T/new Website/modules/static/spinn.wav')
    spin_sound.set_volume(0.3)  # Decrease spin sound volume to 50%
except pygame.error:
    print("Error loading sound files. Ensure the sound files exist in the specified path.")
    win_sound = None
    spin_sound = None

# Load background music
try:
    pygame.mixer.music.load('c:/Users/VWPE11T/new Website/modules/static/background_music.mp3')
    pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
    pygame.mixer.music.play(-1)  # Loop the background music
except pygame.error:
    print("Error loading background music. Ensure the file exists in the specified path.")

# Load background image
try:
    background_image = load_image('c:/Users/VWPE11T/new Website/modules/static/Background1.png', HEIGHT)
except FileNotFoundError:
    print("Error: Background image not found. Ensure 'background1.png' exists in the specified path.")
    background_image = None

# Global spinning flag
spinning = False

# Rad-Klasse
class Wheel:
    def __init__(self):
        self.grid = [[random.choice(symbols) for _ in range(5)] for _ in range(5)]  # 5x5 grid
        self.running = False
        self.spin_frames = int(4 * 60)  # Adjusted for 4.8 seconds at 60 FPS
        self.current_frame = 0

    def spin(self):
        """Start the wheel spinning if it is not already spinning."""
        global spinning
        if not spinning:  # Ensure no other spin is in progress
            self.running = True
            spinning = True  # Set global spinning flag
            self.current_frame = 0  # Reset the frame counter

            # Introduce a small chance for a jackpot
            if random.randint(1, 1000) == 1:  # 1 in 1000 chance
                jackpot_symbol = random.choice(symbols)  # Choose a random symbol for the jackpot
                self.grid = [[jackpot_symbol for _ in range(5)] for _ in range(5)]  # Fill the grid with the same symbol
            else:
                # Normal random grid
                self.grid = [[random.choice(symbols) for _ in range(5)] for _ in range(5)]

    def update(self):
        global spinning
        if self.running:
            self.current_frame += 1
            for row in range(5):
                for col in range(5):
                    if self.current_frame % 8 == 0:  # Update symbols every 8 frames for smoother animation
                        self.grid[row][col] = random.choice(symbols)
            if self.current_frame >= self.spin_frames:  # Stop after the specified number of frames
                self.running = False
                spinning = False  # Reset global spinning flag

    def draw(self, surface, grid_x, grid_y, blinking_boxes=None):
        for row in range(5):
            for col in range(5):
                symbol_image = self.grid[row][col]
                symbol_rect = symbol_image.get_rect()
                symbol_rect.center = (
                    grid_x + col * 80 + 40,  # Adjust spacing for smaller fruits
                    grid_y + row * 80 + 40,  # Adjust spacing for smaller fruits
                )
                # Draw a box around each fruit
                box_rect = pygame.Rect(
                    grid_x + col * 80, grid_y + row * 80, 80, 80  # Box dimensions
                )
                pygame.draw.rect(surface, BOX_COLOR, box_rect, 2)  # Normal box border

                # Handle winning fruits
                if blinking_boxes and (row, col) in blinking_boxes:
                    surface.blit(explosion_image, symbol_rect)  # Replace fruit with explosion
                else:
                    surface.blit(symbol_image, symbol_rect)

def is_blinking():
    """Determine if the fruit should be visible during the blinking phase."""
    return (pygame.time.get_ticks() // 250) % 2 == 0  # Blink every 250ms

# Check for matches of 4
def check_matches(grid):
    """Check for matches of exactly 4 in a row, column, or diagonal."""
    matches = set()  # Use a set to store unique matches

    # Check horizontal matches
    for row in range(5):
        for col in range(2):  # Only check up to the second-to-last column
            if grid[row][col] == grid[row][col + 1] == grid[row][col + 2] == grid[row][col + 3]:
                matches.update([(row, col), (row, col + 1), (row, col + 2), (row, col + 3)])

    # Check vertical matches
    for col in range(5):
        for row in range(2):  # Only check up to the second-to-last row
            if grid[row][col] == grid[row + 1][col] == grid[row + 2][col] == grid[row + 3][col]:
                matches.update([(row, col), (row + 1, col), (row + 2, col), (row + 3, col)])

    # Check diagonal matches (top-left to bottom-right)
    for row in range(2):  # Only check up to the second-to-last row
        for col in range(2):  # Only check up to the second-to-last column
            if grid[row][col] == grid[row + 1][col + 1] == grid[row + 2][col + 2] == grid[row + 3][col + 3]:
                matches.update([(row, col), (row + 1, col + 1), (row + 2, col + 2), (row + 3, col + 3)])

    # Check diagonal matches (top-right to bottom-left)
    for row in range(2):  # Only check up to the second-to-last row
        for col in range(3, 5):  # Only check from the third column to the last column
            if grid[row][col] == grid[row + 1][col - 1] == grid[row + 2][col - 2] == grid[row + 3][col - 3]:
                matches.update([(row, col), (row + 1, col - 1), (row + 2, col - 2), (row + 3, col - 3)])

    return matches

# Initialize the wheel
wheel = Wheel()

# Coins
coins = 10  # Starting coins
current_bet = 1  # Default bet is 1 coin

# Lever
lever_base = (WIDTH - 50, HEIGHT // 2)  # Base of the lever on the side
lever_length = 100  # Shorter lever length
lever_angle = 0  # Angle of the lever (0 = upright)
lever_pulled = False  # Track if the lever is being pulled

# Track awarded matches to prevent duplicate rewards
awarded_matches = set()

def filter_new_matches(matches):
    """Filter out matches that have already been awarded points."""
    global awarded_matches
    new_matches = matches - awarded_matches  # Only include new matches
    awarded_matches.update(new_matches)  # Add new matches to the awarded set
    return new_matches

def get_blinking_positions(matches):
    """Extract the positions of the winning fruits from the matches."""
    return [pos for pos in matches]  # Ensure positions are tuples of (row, col)

def calculate_reward(matches):
    """Calculate the total reward based on the number of distinct matches."""
    reward = 0
    match_positions = set()  # Track unique positions in matches

    for match in matches:  # Iterate over matches directly
        match_positions.add(match)  # Add each matched position to the set

    # Each distinct match of 4 fruits gives a fixed reward of 3 coins
    reward = (len(match_positions) // 4) * 3  # Divide by 4 to count distinct matches of 4 fruits

    return reward, len(matches) // 4  # Return the total reward and the number of distinct groups of 4

# Global variable to control the game loop
running = True

# Draw bet buttons with hover, click effects, and selected feedback
def draw_bet_buttons(surface, mouse_pos, clicked, current_bet):
    font = pygame.font.SysFont(None, 40)
    bets = [1, 2, 5]  # Available bet amounts
    button_width = 100
    button_height = 50
    spacing = 35  # Increased spacing between buttons
    vertical_offset = 90  # Increased spacing above the buttons
    total_width = len(bets) * button_width + (len(bets) - 1) * spacing  # Total width of all buttons with spacing
    start_x = (WIDTH - total_width) // 2  # Center the buttons horizontally

    for i, bet in enumerate(bets):
        button_rect = pygame.Rect(start_x + i * (button_width + spacing), HEIGHT - vertical_offset, button_width, button_height)

        # Change color based on hover, click, or selection
        if bet == current_bet:
            color = (0, 255, 0)  # Green for selected button
        elif button_rect.collidepoint(mouse_pos):
            if clicked:
                color = (255, 165, 0)  # Orange for click effect
            else:
                color = (255, 215, 0)  # Bright gold for hover effect
        else:
            color = GOLD  # Default gold color

        pygame.draw.rect(surface, color, button_rect)
        pygame.draw.rect(surface, BLACK, button_rect, 2)  # Black border
        bet_text = font.render(f"{bet} Coin", True, BLACK)
        text_rect = bet_text.get_rect(center=button_rect.center)
        surface.blit(bet_text, text_rect)

# Handle bet button clicks
def handle_bet_buttons(mouse_pos):
    global current_bet
    bets = [1, 2, 5]
    button_width = 100
    button_height = 50
    total_width = len(bets) * button_width + (len(bets) - 1) * 20
    start_x = (WIDTH - total_width) // 2

    for i, bet in enumerate(bets):
        button_rect = pygame.Rect(start_x + i * (button_width + 20), HEIGHT - 100, button_width, button_height)
        if button_rect.collidepoint(mouse_pos):
            current_bet = bet  # Update the current bet

# Enhanced explosion animation
def play_explosion_animation(surface, positions, is_big_explosion=False):
    """Play an enhanced explosion animation for each position in a 4-in-a-row match."""
    if is_big_explosion:
        # Big explosion in the middle
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        for scale in range(100, 200, 20):  # Gradually increase the size for the big explosion
            surface.fill(RED)  # Clear the screen with the background color
            wheel.draw(surface, WIDTH // 2 - 200, HEIGHT // 2 - 200)  # Redraw the wheel
            explosion_scaled = scale_image(explosion_image, scale)  # Scale the explosion image
            explosion_rect = explosion_scaled.get_rect(center=(center_x, center_y))  # Center the scaled image
            surface.blit(explosion_scaled, explosion_rect)

            # Display explosion text
            font = pygame.font.SysFont(None, 80)
            explosion_text = font.render("BIG WIN!", True, GOLD)
            text_rect = explosion_text.get_rect(center=(center_x, center_y - 100))
            surface.blit(explosion_text, text_rect)

            pygame.display.flip()
            pygame.time.delay(50)  # Reduced delay for smoother animation
    else:
        # Individual explosions for each position
        for pos in positions:
            for scale in range(60, 120, 10):  # Gradually increase the size from 60 to 120
                surface.fill(RED)  # Clear the screen with the background color
                wheel.draw(surface, WIDTH // 2 - 200, HEIGHT // 2 - 200)  # Redraw the wheel
                explosion_scaled = scale_image(explosion_image, scale)  # Scale the explosion image
                explosion_rect = explosion_scaled.get_rect(center=pos)  # Center the scaled image
                surface.blit(explosion_scaled, explosion_rect)

                # Add a glowing effect around the explosion
                pygame.draw.circle(surface, GOLD, pos, scale // 2, 2)  # Glow effect
                pygame.display.flip()
                pygame.time.delay(30)  # Reduced delay for smoother animation

def check_jackpot(grid):
    """Check if the grid contains a jackpot (all symbols are the same)."""
    first_symbol = grid[0][0]  # Take the first symbol as a reference
    for row in grid:
        for symbol in row:
            if symbol != first_symbol:  # If any symbol is different, it's not a jackpot
                return False
    return True  # All symbols are the same, it's a jackpot

def show_popup_message(surface, message):
    """Display a popup message in the center of the screen."""
    font = pygame.font.SysFont(None, 60)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(surface, BLACK, text_rect.inflate(20, 20))  # Background for the popup
    pygame.draw.rect(surface, GOLD, text_rect.inflate(20, 20), 3)  # Border for the popup
    surface.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)  # Show the popup for 2 seconds

def draw_back_button(surface):
    """Draw a semi-transparent 'Back' button at the top-right of the screen."""
    button_width, button_height = 100, 50
    button_x, button_y = WIDTH - button_width - 10, 10  # Position at the top-right corner
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Draw semi-transparent background
    s = pygame.Surface((button_width, button_height), pygame.SRCALPHA)  # Create a surface with alpha
    s.fill((255, 255, 255, 128))  # White with 50% transparency
    surface.blit(s, (button_x, button_y))

    # Draw border
    pygame.draw.rect(surface, WHITE, button_rect, 2)  # White border

    # Draw text
    font = pygame.font.SysFont(None, 30)
    text = font.render("Back", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    surface.blit(text, text_rect)

# Display big win messages directly on the screen instead of using a popup.
try:
    # Spielschleife
    blinking_boxes = []  # Initialize blinking_boxes to track positions of winning fruits
    blink_start_time = None  # Initialize blink_start_time for blinking logic
    while running:
        # Draw the background image or fallback to a gray background
        if background_image:
            screen.blit(background_image, (0, 0))  # Draw the background image
        else:
            screen.fill((128, 128, 128))  # Gray background color as fallback

        # Draw the 'Back' button
        draw_back_button(screen)

        lever_top = (
            lever_base[0] - lever_length * math.sin(math.radians(lever_angle)),  # Adjust for upward lever
            lever_base[1] - lever_length * math.cos(math.radians(lever_angle)),  # Adjust for upward lever
        )

        # Draw lever
        pygame.draw.line(screen, (192, 192, 192), lever_base, lever_top, 8)  # Chrome-like lever
        pygame.draw.circle(screen, (105, 105, 105), lever_base, 10)  # Dark chrome pivot point
        pygame.draw.circle(screen, WHITE, lever_top, 12)  # Red knob at the end of the lever

        # Display coins with a dollar sign before the number
        font = pygame.font.SysFont(None, 50)
        coin_text = font.render(f"Coins: ${coins}", True, WHITE)
        screen.blit(coin_text, (10, 10))

        # Get mouse position and click state
        mouse_pos = pygame.mouse.get_pos()
        clicked = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the click is within the clickable area of the lever
                if (
                    lever_top[0] - 20 < mouse_x < lever_top[0] + 20
                    and lever_top[1] - 20 < mouse_y < lever_top[1] + 20
                ):
                    if not spinning:  # Prevent multiple spins
                        if coins >= current_bet:  # Ensure enough coins for the current bet
                            lever_pulled = True
                            coins -= current_bet  # Deduct the current bet
                            spin_sound.play()  # Play the spin sound once
                            wheel.spin()  # Start spinning
                        else:
                            show_popup_message(screen, "Not enough coins!")  # Show popup if not enough coins

                # Handle bet button clicks
                handle_bet_buttons(mouse_pos)  # Ensure this is called when a button is clicked

            if event.type == pygame.MOUSEBUTTONUP and lever_pulled:
                lever_pulled = False  # Reset lever pull state

        # Update lever angle
        if lever_pulled and lever_angle < 90:  # Allow lever to rotate downward up to 90 degrees
            lever_angle += 5
        elif not lever_pulled and lever_angle > 0:  # Reset lever to its original upward position
            lever_angle -= 5

        # Define grid_x and grid_y for proper alignment
        grid_x = WIDTH // 2 - 200  # Center the grid horizontally
        grid_y = HEIGHT // 2 - 200  # Center the grid vertically

        # Update and draw the wheel
        wheel.update()
        wheel.draw(screen, grid_x, grid_y, blinking_boxes)  # Pass blinking positions

        # Reset spinning flag when the wheel stops
        if not wheel.running and wheel.current_frame == wheel.spin_frames:
            spinning = False  # Reset global spinning flag
            matches = check_matches(wheel.grid)
            new_matches = filter_new_matches(matches)  # Filter out already awarded matches
            if new_matches:
                blinking_boxes = get_blinking_positions(new_matches)  # Get positions to replace with explosions
                blink_start_time = pygame.time.get_ticks()  # Start blinking timer
                if win_sound:
                    win_sound.play()  # Play the win sound
                base_reward, distinct_groups = calculate_reward(new_matches)  # Calculate the base reward and groups
                if base_reward > 0:  # Ensure points are awarded for valid matches
                    coins += base_reward * current_bet  # Multiply the reward by the current bet and add to coins

                # Play explosion animation for all matched positions
                explosion_positions = [
                    (grid_x + col * 80 + 40, grid_y + row * 80 + 40)
                    for row, col in blinking_boxes if (row, col) in new_matches
                ]
                if explosion_positions:  # Ensure explosions are triggered only once
                    if distinct_groups == 1:
                        play_explosion_animation(screen, explosion_positions)
                    elif distinct_groups == 2:
                        play_explosion_animation(screen, explosion_positions, is_big_explosion=True)
                        # Display "DOUBLE WIN!" on the screen
                        font = pygame.font.SysFont(None, 80)
                        double_win_text = font.render("DOUBLE WIN!", True, GOLD)
                        screen.blit(double_win_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
                        pygame.display.flip()  # Ensure the text is rendered on the screen
                        pygame.time.delay(2000)  # Show the message for 2 seconds
                    elif distinct_groups >= 3:
                        play_explosion_animation(screen, explosion_positions, is_big_explosion=True)
                        # Display "TRIPLE WIN!" on the screen
                        font = pygame.font.SysFont(None, 80)
                        triple_win_text = font.render("TRIPLE WIN!", True, GOLD)
                        screen.blit(triple_win_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
                        pygame.display.flip()  # Ensure the text is rendered on the screen
                        pygame.time.delay(2000)  # Show the message for 2 seconds

                # Ensure the screen is updated after explosions and messages
                pygame.display.flip()

            # Check for jackpot
            if check_jackpot(wheel.grid):  # Ensure jackpot logic is correct
                jackpot_reward = 1000 * current_bet  # Multiply jackpot reward by the current bet
                coins += jackpot_reward  # Add the jackpot reward to coins
                print(f"JACKPOT! You won {jackpot_reward} coins!")
                jackpot_text = font.render(f"JACKPOT! +{jackpot_reward} Coins!", True, GOLD)
                screen.blit(jackpot_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
                pygame.display.flip()
                pygame.time.delay(2000)  # Show jackpot message for 2 seconds

        # Handle blinking logic
        if blink_start_time:
            elapsed_time = pygame.time.get_ticks() - blink_start_time
            if elapsed_time > 1000:  # Show explosions for 1 second
                blinking_boxes = []  # Stop showing explosions
                blink_start_time = None

        # Draw bet buttons with hover, click effects, and selected feedback
        draw_bet_buttons(screen, mouse_pos, clicked, current_bet)

        pygame.display.flip()
        clock.tick(60)

except KeyboardInterrupt:
    print("\nGame interrupted. Exiting gracefully...")
finally:
    pygame.mixer.music.stop()  # Stop background music
    pygame.quit()