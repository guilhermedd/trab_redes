import pygame

# Initialize Pygame
pygame.init()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

# Set the font and font size
FONT = pygame.font.Font(None, 32)

# Set the text color and background color
TEXT_COLOR = pygame.Color("white")
BG_COLOR = pygame.Color("black")

# Create a window and set the title
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Input Box")

# Set the input box dimensions
input_box = pygame.Rect(50, 100, 300, 50)

# Set the initial user input
user_input = ""

# Create a variable to check if the input box is active
input_active = False

# Set the clock to control the frame rate
clock = pygame.time.Clock()

# Run the game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Exit the game if the user closes the window
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Set the input box to active if the user clicks on it
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
        elif event.type == pygame.KEYDOWN:
            # Add characters to the user input if the input box is active
            if input_active:
                if event.key == pygame.K_RETURN:
                    # Save the user input and clear the input box
                    print("User input:", user_input)
                    user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character from the user input
                    user_input = user_input[:-1]
                else:
                    # Add the character to the user input
                    user_input += event.unicode

    # Draw the text inside the input box
    text_surface = FONT.render(user_input, True, TEXT_COLOR)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)
