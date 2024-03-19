import pygame
import random

# pygame setup
pygame.init()
square_width = 800
pixel_width = 50
screen = pygame.display.set_mode([square_width] * 2)
clock = pygame.time.Clock()
running = True
paused = False
font = pygame.font.Font(None, 36)
counter = 0
highScore = 0

eat_sound = pygame.mixer.Sound("beep.wav")

def calculateHighScore():
    global highScore
    if counter > highScore:
        highScore = counter
    return highScore

def generate_starting_position():
    position_range = (pixel_width // 2, square_width - pixel_width // 2, pixel_width)
    return (random.randrange(*position_range), random.randrange(*position_range))


def reset():
    target.center = generate_starting_position()
    snake_pixel.center = generate_starting_position()
    return [snake_pixel.copy()]


def isOutOfBounds():
    return snake_pixel.bottom > square_width or snake_pixel.top < 0 or snake_pixel.left < 0 or snake_pixel.right > square_width



MENU = 0
GAME = 1

current_state = MENU

# playground

# Snake
snake_pixel = pygame.Rect(0, 0, pixel_width - 2, pixel_width - 2)
snake_pixel.center = generate_starting_position()
snake = [snake_pixel.copy()]
snake_direction = (0, 0)
snake_length = 1
current_direction = pygame.K_RIGHT

# Target
target = pygame.Rect(0, 0, pixel_width - 2, pixel_width - 2)
target.center = generate_starting_position()

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from the last frame
    screen.fill("black")

    if current_state == MENU:
        menu_text = font.render("Press Space or Tap Screen to Start", True, (255, 255, 255))
        screen.blit(menu_text, (square_width // 2 - 150, square_width // 2 - 50))

        highScore_text = font.render(f"High Score: {calculateHighScore()}", True, (255, 255, 255))
        screen.blit(highScore_text, (10, 10))

        click = pygame.mouse.get_pressed()
        if click[0]:
            current_state = GAME

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            current_state = GAME

    elif current_state == GAME:
        if isOutOfBounds():
            snake_length = 1
            counter = 0
            snake = reset()
            current_state = MENU

        snake_head = snake[-1]  # head of the snake

        # Check for self-collision
        if any(snake_part.colliderect(snake_head) for snake_part in snake[:-1]):
            snake_length = 1
            counter = 0
            snake = reset()


        if snake_pixel.center == target.center:
            target.center = generate_starting_position()
            snake_length += 1
            counter += 1
            calculateHighScore()
            snake.append(snake_pixel.copy())
            eat_sound.play()
            
        # snake movement logic here
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and current_direction != pygame.K_DOWN:
            snake_direction = (0, -pixel_width)
            current_direction = pygame.K_UP
        if keys[pygame.K_DOWN] and current_direction != pygame.K_UP:
            snake_direction = (0, pixel_width)
            current_direction = pygame.K_DOWN
        if keys[pygame.K_LEFT] and current_direction != pygame.K_RIGHT:
            snake_direction = (-pixel_width, 0)
            current_direction = pygame.K_LEFT
        if keys[pygame.K_RIGHT] and current_direction != pygame.K_LEFT:
            snake_direction = (pixel_width, 0)
            current_direction = pygame.K_RIGHT

        # snake and target
        for snake_part in snake:
            pygame.draw.rect(screen, "green", snake_part)  # Green for snake

        pygame.draw.rect(screen, "red", target)  # Red for target

        counter_text = font.render(f"Score: {counter}", True, (255, 255, 255))
        screen.blit(counter_text, (10, 10))

        # Move the snake (update the position)
        snake_pixel.move_ip(snake_direction)
        snake.append(snake_pixel.copy())

        # Remove the oldest part of the snake if it has grown beyond the specified length
        if len(snake) > snake_length:
            del snake[0]

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(10)  # Adjust the speed of the game by changing the tick rate

pygame.quit()
