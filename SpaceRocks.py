import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 900, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Infinite Space Craft")

# Set up fonts and colors
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)  # New font for smaller text
white = (255, 255, 255)
black = (0, 0, 0)

# Load images
background_image = pygame.image.load('space.jpg')
background_image = pygame.transform.scale(background_image, (screen_width * 2, screen_height))
jetship_image = pygame.image.load('jetship.png')
jetship_image = pygame.transform.scale(jetship_image, (50, 50))
asteroid_images = [pygame.image.load('rock1.png'), pygame.image.load('rock2.png'), pygame.image.load('rock3.png')]

# Developer images
moi_image = pygame.image.load('Moi.jpg')
kin_image = pygame.image.load('Kin.jpg')
roger_image = pygame.image.load('Roger.png')
marc_image = pygame.image.load('Cram.jpg')

# Resize developer images
developer_image_size = (120, 120)
moi_image = pygame.transform.scale(moi_image, developer_image_size)
kin_image = pygame.transform.scale(kin_image, developer_image_size)
roger_image = pygame.transform.scale(roger_image, developer_image_size)
marc_image = pygame.transform.scale(marc_image, developer_image_size)

# Set up game variables
jetship_rect = jetship_image.get_rect(topleft=(50, screen_height // 2 - 25))
jetship_speed = 10
background_x = 0
asteroids = []
score = 0
clock = pygame.time.Clock()
game_active = False
game_over = False
show_developers = False  # Flag to show the Developers section

# Create a start button
start_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 - 25, 100, 50)
start_text = font.render("Start", True, black)

# Create an instruction button
instruction_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50)
instruction_text = font.render("How to play", True, black)

# Create a Developers button
developers_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 120, 200, 50)
developers_text = font.render("Developers", True, black)



# Create a Quit button
quit_button = pygame.Rect(screen_width // 2 - 50, screen_height // 2 + 190, 100, 50)
quit_text = font.render("Quit", True, black)



# Center the text within the buttons
text_x_start = start_button.centerx - start_text.get_width() // 2
text_y_start = start_button.centery - start_text.get_height() // 2

text_x_instruction = instruction_button.centerx - instruction_text.get_width() // 2
text_y_instruction = instruction_button.centery - instruction_text.get_height() // 2

text_x_developers = developers_button.centerx - developers_text.get_width() // 2
text_y_developers = developers_button.centery - developers_text.get_height() // 2


text_x_quit = quit_button.centerx - quit_text.get_width() // 2
text_y_quit = quit_button.centery - quit_text.get_height() // 2



# Functions
def reset_jetship_position():
    global jetship_rect
    jetship_rect.topleft = (50, screen_height // 2 - 25)

def draw_start_button():
    pygame.draw.rect(screen, white, start_button)
    screen.blit(start_text, (text_x_start, text_y_start))

def draw_instruction_button():
    pygame.draw.rect(screen, white, instruction_button)
    screen.blit(instruction_text, (text_x_instruction, text_y_instruction))

def draw_developers_button():
    pygame.draw.rect(screen, white, developers_button)
    screen.blit(developers_text, (text_x_developers, text_y_developers))

def draw_try_again_button():
    pygame.draw.rect(screen, white, try_again_button)
    screen.blit(try_again_text, (text_x_try_again, text_y_try_again))

def draw_quit_button():
    pygame.draw.rect(screen, white, quit_button)
    screen.blit(quit_text, (text_x_quit, text_y_quit))

def spawn_asteroid():
    if random.randint(0, 100) < 2:
        asteroid_x = screen_width
        asteroid_y = random.randint(0, screen_height - 50)
        asteroid_image = random.choice(asteroid_images)
        asteroid_speed = random.uniform(2, 5)
        asteroids.append((asteroid_x, asteroid_y, asteroid_image, asteroid_speed))

def draw_elements():
    screen.blit(background_image, (background_x, 0))
    screen.blit(background_image, (background_x + screen_width, 0))
    screen.blit(jetship_image, jetship_rect.topleft)

    for asteroid in asteroids:
        asteroid_x, asteroid_y, asteroid_image, _ = asteroid
        screen.blit(asteroid_image, (asteroid_x, asteroid_y))

def check_collisions():
    for asteroid in asteroids:
        asteroid_rect = pygame.Rect(asteroid[:2], (50, 50))
        if jetship_rect.colliderect(asteroid_rect):
            reset_jetship_position()
            return True
    return False

def update_game_state():
    global jetship_rect, background_x, game_over, score

    if game_active and not game_over:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            jetship_rect.y -= jetship_speed
        if keys[pygame.K_DOWN]:
            jetship_rect.y += jetship_speed
        if keys[pygame.K_LEFT]:
            jetship_rect.x -= jetship_speed
        if keys[pygame.K_RIGHT]:
            jetship_rect.x += jetship_speed

        jetship_rect.y = max(0, min(jetship_rect.y, screen_height - jetship_rect.height))
        jetship_rect.x = max(0, min(jetship_rect.x, screen_width - jetship_rect.width))

        background_x -= jetship_speed

        if background_x < -screen_width:
            background_x = 0

        for i in range(len(asteroids)):
            x, y, image, speed = asteroids[i]
            x -= speed
            asteroids[i] = (x, y, image, speed)

        asteroids[:] = [(x, y, image, speed) for x, y, image, speed in asteroids if x > -50]

        spawn_asteroid()

        if check_collisions():
            game_over = True
        else:
            score += 1

def draw_score():
    if game_active:  # Only show the score when the game is active
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

def show_instructions():
    instruction_text = "Use the arrow keys to navigate the spaceship. Avoid the asteroids and survive as long as you can!"
    instruction_font = pygame.font.Font(None, 24)
    instruction_surface = instruction_font.render(instruction_text, True, white)
    instruction_rect = instruction_surface.get_rect(center=(screen_width // 2, screen_height // 2))

    while True:
        screen.fill(black)
        screen.blit(instruction_surface, instruction_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return

def show_developers_section():
    while True:
        screen.fill(black)

        # Check if the Developers button is clicked to exit the Developers section
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                return

        developers_title = font.render("Developers", True, white)
        screen.blit(developers_title, (screen_width // 2 - developers_title.get_width() // 2, 150))

        # Display developer images and names (larger and centered)
        developer_images = [moi_image, kin_image, roger_image, marc_image]
        developer_names = ["Moissan Guevarra", "Jason Kin Tajor", "Roger Ray Cruz ", "Marc Angelo Bangcal"]

        total_width = sum(image.get_width() for image in developer_images)
        spacing = (screen_width - total_width) // (len(developer_images) + 1)

        current_x = spacing

        for i, image in enumerate(developer_images):
            y = screen_height // 2 - image.get_height() // 2
            screen.blit(image, (current_x, y))

            # Display developer names below images with smaller font
            name_text = small_font.render(developer_names[i], True, white)
            name_x = current_x + image.get_width() // 2 - name_text.get_width() // 2
            name_y = y + image.get_height() + 10
            screen.blit(name_text, (name_x, name_y))

            current_x += image.get_width() + spacing

        pygame.display.flip()

def show_start_screen():
    text1 = "Get lucky with the Ghost Rocks"
    text2 = "Press any key"

    font_large = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 24)  # Change the font size as needed
    
    text1_surface = font_large.render(text1, True, white)
    text1_rect = text1_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 20))  # Adjust the vertical position
    
    text2_surface = font_small.render(text2, True, white)
    text2_rect = text2_surface.get_rect(midbottom=(screen_width // 2, screen_height - 20))  # Adjust the vertical position
    
    waiting_for_key = True
    while waiting_for_key:
        screen.fill(black)
        screen.blit(text1_surface, text1_rect)
        screen.blit(text2_surface, text2_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                waiting_for_key = False

show_start_screen()


# Create a Back to Home button
back_to_home_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 190, 200, 50)
back_to_home_text = font.render("Back to Home", True, black)

# Center the text within the Back to Home button
text_x_back_to_home = back_to_home_button.centerx - back_to_home_text.get_width() // 2
text_y_back_to_home = back_to_home_button.centery - back_to_home_text.get_height() // 2
# Create a Try Again button
try_again_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 120, 200, 50)
try_again_text = font.render("Try Again!", True, black)

text_x_try_again = try_again_button.centerx - try_again_text.get_width() // 2
text_y_try_again = try_again_button.centery - try_again_text.get_height() // 2

def draw_back_to_home_button():
    pygame.draw.rect(screen, white, back_to_home_button)
    screen.blit(back_to_home_text, (text_x_back_to_home, text_y_back_to_home))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not game_active:
                if start_button.collidepoint(event.pos):
                    game_active = True
                    asteroids = []
                    score = 0  # Reset the score when the game starts
                elif instruction_button.collidepoint(event.pos):
                    show_instructions()
                elif developers_button.collidepoint(event.pos):
                    show_developers_section()
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            elif game_over:
                if try_again_button.collidepoint(event.pos):
                    game_active = True
                    game_over = False
                    reset_jetship_position()
                    asteroids = []
                    score = 0  # Reset the score to zero
                elif back_to_home_button.collidepoint(event.pos):
                    game_active = False
                    game_over = False

    update_game_state()

    screen.fill(black)
    draw_elements()
    draw_score()

    if not game_active:
        draw_start_button()
        draw_instruction_button()
        draw_developers_button()
        draw_quit_button()  # Draw the Quit button
    elif game_over:
        draw_try_again_button()
        draw_back_to_home_button()  # Draw the Back to Home button

    pygame.display.flip()
    clock.tick(60)

    