import pygame
from pygame.locals import *
import random



# Initialize game settings
size = x, y = (800, 800)
space_w = int(x / 5)
startind = False
speed = 10
speed_increment = 0.2
obstacle_crossings = 0  # Counter for obstacle crossings

pygame.init()
run = True
screen = pygame.display.set_mode(size)
pygame.display.set_caption("RUN PIRATE RUN")

# Load images
back = pygame.image.load('assets/Space BG.png')
title = pygame.image.load('assets/Gametitle.png')
start = pygame.image.load('assets/Start Msg.png')
compete = pygame.image.load('assets/er.png')
obstacle = pygame.image.load('assets/oi.png')
over = pygame.image.load('assets/Game over.png')
pause_image = pygame.image.load(r"assets/pause.png")
resume_image = pygame.image.load(r"assets/resume.png")
quiz_images = [
    pygame.image.load(r"assets/quiz1.png"),
    pygame.image.load(r"assets/quiz2.png"),
    pygame.image.load(r"assets/quiz3.png"),
    pygame.image.load(r"assets/quiz4.png"),
    pygame.image.load(r"assets/quiz5.png"),
    pygame.image.load(r"assets/quiz6.png"),
    pygame.image.load(r"assets/quiz7.png"),
    pygame.image.load(r"assets/quiz8.png"),
    pygame.image.load(r"assets/quiz9.png"),
    pygame.image.load(r"assets/quiz10.png")
]

# Create image locations
back_loc = back.get_rect()
title_loc = title.get_rect()
title_loc.center = x / 2, y / 2

start_loc = start.get_rect()
start_loc.center = x / 2, y / 2

compete_loc = compete.get_rect()
compete_loc.center = space_w, y * 0.8

obstacle_loc = obstacle.get_rect()
obstacle_loc.center = space_w, y * 0.1

over_loc = over.get_rect()
over_loc.center = x / 2, y / 2

paused = False
pause_displayed = False  
quiz_active = False
current_quiz_index = -1  


quiz_intervals = {
    (10.599999999999998, 10.799999999999997): 0,  # Display quiz1
    (10.999999999999996, 11.199999999999996): 1,  # Display quiz2
    (11.399999999999995, 11.599999999999994): 2,  # Display quiz3
    (11.799999999999994, 11.999999999999993): 3,  # Display quiz4
    (12.199999999999992, 12.399999999999991): 4,  # Display quiz5
    (12.59999999999999, 12.79999999999999): 5,    # Display quiz6
    (12.99999999999999, 13.199999999999989): 6,   # Display quiz7
    (13.399999999999988, 13.599999999999987): 7,  # Display quiz8
    (13.799999999999986, 13.999999999999986): 8,  # Display quiz9
    (14.199999999999985, 14.399999999999984): 9   # Display quiz10
}


shown_quizzes = {}

def draw_background_and_elements():
    screen.blit(back, back_loc)
    screen.blit(compete, compete_loc)
    screen.blit(obstacle, obstacle_loc)
    screen.blit(title, title_loc)

def display_image(image):
    screen.blit(image, (0, 0))
    pygame.display.flip()

# Initial screen setup
draw_background_and_elements()
screen.blit(start, start_loc)
pygame.display.update()

while run:
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN:
            if event.key == K_s:
                startind = True
            if event.key == K_r:
                compete_loc.center = space_w, y * 0.8
                obstacle_loc.center = space_w, y * 0.1
                startind = True
                speed = 10

    while startind:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in [K_l, K_LEFT]:
                    new_x = compete_loc[0] + space_w
                    if new_x >= 0:
                        compete_loc = compete_loc.move(-space_w, 0)
                if event.key in [K_r, K_RIGHT]:
                    new_x = compete_loc[0] - space_w
                    if new_x <= x - 480:
                        compete_loc = compete_loc.move(space_w, 0)

                if event.key == K_p and not paused:
                    if pause_displayed:
                        paused = True
                        pause_displayed = False
                        draw_background_and_elements()
                        pygame.display.update()
                        pygame.time.wait(1000)
                        draw_background_and_elements()
                        if current_quiz_index is not None:
                            display_image(quiz_images[current_quiz_index])
                        quiz_active = True

                if event.key == K_q:
                    paused = False
                    quiz_active = False
                    draw_background_and_elements()
                    pygame.display.update()

            if event.type == QUIT:
                run = False
                startind = False

        if not paused:
            current_quiz_index = None
            for (start, end), index in quiz_intervals.items():
                if start <= speed < end:
                    current_quiz_index = index
                    if (start, end) not in shown_quizzes:
                        shown_quizzes[(start, end)] = True
                        if not pause_displayed:
                            pause_displayed = True
                            draw_background_and_elements()
                            display_image(pause_image)
                            paused = True   
                    break

            if paused and current_quiz_index is not None and not quiz_active:
                draw_background_and_elements()
                display_image(quiz_images[current_quiz_index])
                quiz_active = True

            obstacle_loc[1] += speed
            if obstacle_loc[1] > y:
                obstacle_loc.center = space_w * random.randint(0, 5), -100
                obstacle_crossings += 1  

                if obstacle_crossings >= 2:
                    speed += speed_increment
                    print(speed)
                    obstacle_crossings = 0  

            if compete_loc[0] == obstacle_loc[0] and compete_loc[1] < obstacle_loc[1] + 175 and compete_loc[1] > obstacle_loc[1] - 175:
                draw_background_and_elements()
                screen.blit(over, over_loc)
                pygame.display.update()
                pygame.time.wait(2000)
                startind = False

        if paused:
            while paused:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_b  and current_quiz_index in [0, 2, 4, 9] or event.key == K_a and current_quiz_index == 1 or  event.key == K_c and current_quiz_index in [3, 5, 6, 7, 8]:
                            draw_background_and_elements()
                            display_image(resume_image)
                            quiz_active = False
                            paused = False
                            pause_displayed = False

                        if event.key == pygame.K_q:
                            paused = False
                            quiz_active = False
                            draw_background_and_elements()
                            pygame.display.update()

                    if event.type == pygame.QUIT:
                        paused = False
                        run = False

                pygame.time.delay(10)

        if not paused:
            draw_background_and_elements()

        pygame.display.update()


pygame.quit()

