import pygame

pygame.init()
clock = pygame.time.Clock()
fps = 60

# Set the width and height of the screen [width, height]
size = (800, 400)
bottom_panel = 150
screen = pygame.display.set_mode((size[0], size[1] + bottom_panel))
pygame.display.set_caption("RPG")

# Load Image
# Background Image
background_image = pygame.image.load('.\img\Background/background.png').convert_alpha()
background_image = pygame.transform.scale(background_image, (size[0], size[1]))

panel_image = pygame.image.load('./img/Icons/panel.png').convert_alpha()
panel_image = pygame.transform.scale(panel_image, (size[0], bottom_panel))
# Function to draw background

def draw_bg():
    # screen.llit(background_image, [0, 0])
    screen.blit(background_image, (0, 0))

def draw_panel():
    # screen.llit(background_image, [0, 0])
    screen.blit(panel_image, (0, size[1]))

def write_panel(fighter):
    WHITE = (255, 255, 255)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(str(fighter.room), True, WHITE)
    txt = text.get_rect()
    txt.center = (size[0] // 2, 50)
    screen.blit(text, txt)

class Fighter():
    def __init__(self, x, y, max_health, points, room):
        self.max_health = max_health
        self.health = max_health
        self.x = x
        self.y = y
        self.points = points
        self.room = room
        self.alive = True
        self.img_path = './img\Knight\Idle/0.png'
        img = pygame.image.load(self.img_path).convert_alpha()
        self.image = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
    
    def loose_health(self, hp):
        self.health -= hp
    
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

knight = Fighter(70, 180, 100, 0, 0)
# Loop until the user clicks the close button.
run = True
while run:
    clock.tick(fps)

    # Draw background
    draw_bg()
    draw_panel()
    write_panel(knight)

    knight.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
    pygame.display.update()
