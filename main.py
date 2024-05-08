import pygame
import sys
import random

# Initialize Pygame
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# Function
def game_floor():
    screen.blit(floor_base, (floor_x_position, 700))
    screen.blit(floor_base, (floor_x_position + 600, 700))

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    # check if floor not hit
    if bird_rect.top <= -100 or bird_rect.bottom >= 700:
        die_sound.play()
        return False
    return True

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos-300)) 
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    global score
    global last_pipe
    for pipe in pipes:
        pipe.centerx -= 6
        if pipe.right < bird_rect.left and not pipe.top == 0:
            # Bird has passed the pipe
            if last_pipe != pipe:
                score += 1
                last_pipe = pipe
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 800:  
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)

    
def display_score(score):
    score_surface = font.render(str(int(score/2)), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(screen_width/2, 100))
    screen.blit(score_surface, score_rect)

def end_game():
  global score
  score = 0 # reset score to 0




# Font
font = pygame.font.Font(None, 70)


# Global variable
gravity = 0.2
bird_movement = 0
score = 0
last_pipe = None

# Set the width and height of the screen (in pixels)
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the game window
pygame.display.set_caption("Bird Crack")

# Background
background = pygame.image.load("assets/back.jpg").convert()
background = pygame.transform.scale2x(background)

# Scores
Scores = pygame.image.load("assets/Point.png").convert()
Scores = pygame.transform.scale2x(Scores)

# Bird
bird = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100, 500))



# Base
floor_base = pygame.image.load("assets/base.png").convert()
floor_base = pygame.transform.scale2x(floor_base)
floor_x_position = 0

# Message
message = pygame.image.load("assets/message.png").convert_alpha()
message = pygame.transform.scale2x(message)
game_message_rect = message.get_rect(center = (300, 400)) 

# over
over = pygame.image.load("assets/gameover.png")
over = pygame.transform.scale2x(over)
game_over_rect = message.get_rect(center = (300, 400)) 


# Pipe
pipe_surface = pygame.image.load("assets/pipe-green.png").convert_alpha()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [200, 300, 400, 500, 600]


SPAWPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWPIPE, 1200)

# Sound
flap_sound = pygame.mixer.Sound('Sound/flap.mp3')
die_sound = pygame.mixer.Sound('Sound/die.mp3')
hit_sound = pygame.mixer.Sound('Sound/hit.mp3')


pygame.mixer.init()
pygame.mixer.music.load('Sound/music.mp3')
pygame.mixer.music.set_volume(2)
pygame.mixer.music.play()

bird_rects = [pygame.Rect(bird_rect.left, bird_rect.top, bird_rect.width, bird_rect.height // 2),
              pygame.Rect(bird_rect.left, bird_rect.top + bird_rect.height // 2, bird_rect.width, bird_rect.height // 2)]

show_message = True
game_active = True
# Start the game loop
while True:
    # Handle events (such as closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if show_message:
            screen.blit(message, game_message_rect)
        # Key input
        if event.type == pygame.KEYDOWN:
            screen.blit(message, game_over_rect)
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
                show_message = False
                
                
            if event.key == pygame.K_SPACE and game_active == False:
                bird_rect.center = (100, 400)
                bird_movement = 0
                pipe_list.clear()
                game_active = True

        if event.type == SPAWPIPE and game_active:
            pipe_list.extend(create_pipe())
        

            

    # Update the game state and render graphics on the screen
    
    screen.blit(background, (0, 0))
    screen.blit(Scores, (80, 45))

    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement

        screen.blit(bird, bird_rect)

        # Draw pipe
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Check collision
        game_active = check_collision(pipe_list)
    else:
        screen.blit(message, game_over_rect) 



    # Create base_floor
    floor_x_position -= 1



    game_floor()

    if  floor_x_position <= -600:
        floor_x_position = 0

    # Display score
    display_score(score)

    end_game()

    # Update the display
    pygame.display.update()

    # clock
    clock.tick(80)