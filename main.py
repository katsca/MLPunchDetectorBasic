import pygame
import random
import numpy as np

punches = {
    1: ["JAB", "white", "black"],  # jab
    2: ["CROSS", "black", "white"],  # cross
    3: ["LEFT HOOK", "red", "white"],
    4: ["RIGHT HOOK", "pink", "white"],  # RH
    5: ["LEFT UPPER CUT", "green", "white"],  # LUC
    6: ["RIGHT UPPER CUT", "blue", "white"],  # RUC
}

level = 0.5  # 1 technque every 2 second


def generate_punch(T):
    # Generate random number from 1 to 6
    punch_int = random.randint(1, 6)
    print(punch_int)

    # Generate new target time for next punch
    target_time = level + np.random.normal(0, 0.8, 1)
    # Reset time to T
    T = 0
    return punch_int, target_time, T


# pygame setup
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont("Comic Sans MS", 30)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
width = screen.get_width()
height = screen.get_height()
running = True
dt = 0
paused = False

T = 0
punchVal, targetT, T = generate_punch(T)

while running:

    # NORMAL EXIT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused  # Toggles the paused state
                print("Paused" if paused else "Unpaused")

    if T >= targetT and paused == False:
        punchVal, targetT, T = generate_punch(T)
        punch_array = punches[punchVal]
        screen.fill(punch_array[1])
        text_surface = my_font.render(punch_array[0], False, punch_array[2])
        text_rect = text_surface.get_rect(center=(width // 2, height // 2))
        screen.blit(text_surface, text_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.

    dt = clock.tick(60) / 1000
    T += dt

pygame.quit()

# Basically randomly generate these and speed at which they are generate depends on level
