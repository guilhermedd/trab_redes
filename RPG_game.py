import pygame

pygame.init()

# Set the width and height of the screen [width, height]
size = (1280, 720)
screen = pygame.display.set_mode((size[0], size[1]))
pygame.display.set_caption("RPG")

# Load Image
# Background Image
background_image = pygame.image.load('/home/diel/Udesc/Redes/Socket/img/8_bits.jpeg').convert_alpha()
background_image = pygame.transform.scale(background_image, (size[0], size[1]))

# Function to draw background

def draw_bg():
    # screen.llit(background_image, [0, 0])
    screen.blit(background_image, [0, 0])

# Loop until the user clicks the close button.
run = True
while run:

    # Draw background
    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
    pygame.display.update()
