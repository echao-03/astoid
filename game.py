import os
import pygame
import random
from pygame import mixer

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
pygame.font.init()
pygame.mixer.init()
mixer.music.load(os.path.join('Assets', 'Astoids_BG_Music.wav'))



W_WIDTH, W_HEIGHT = 500, 900 # Window Size
WIN = pygame.display.set_mode((W_WIDTH, W_HEIGHT))
FPS = 60
VEL = 5
LASER_VEL = 7
ASTEROID_SPEED = 4
LIGHT_SPEED = 15
RED = (255, 0, 0)
WHITE = (224, 224, 224)
SPAWN_ASTEROIDS = pygame.USEREVENT
pygame.time.set_timer(SPAWN_ASTEROIDS, 500)
SHIP_HIT = pygame.USEREVENT + 1
ASTEROID_HIT = pygame.USEREVENT + 2
BG_LIGHTRAYS = pygame.USEREVENT + 3
pygame.time.set_timer(BG_LIGHTRAYS, 200)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'blaster_sound.wav'))
ASTEROID_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'asteroids_explode.wav'))
SHIP_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'ship_hit.wav'))

SHIP_IMG = pygame.image.load(os.path.join('Assets', 'ship_v1.png'))
ASTEROID = pygame.image.load(os.path.join('Assets', 'asteroid_v.1.png'))
asteroid_rect = ASTEROID.get_rect()
SHIP_WIDTH, SHIP_HEIGHT = 55, 40
AST_WIDTH, AST_HEIGHT = 55, 40

asteroid_score = 0

def ship_movement(keys_pressed, ship):
    if keys_pressed[pygame.K_LEFT] and ship.x - VEL > 0:
         #print("left")
        ship.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and ship.x + VEL + ship.width < W_WIDTH:
        #print("right")
        ship.x += VEL
    if keys_pressed[pygame.K_UP] and ship.y - VEL > 0:
        #print("up")
        ship.y -= VEL
    if keys_pressed[pygame.K_DOWN] and ship.y + VEL + ship.height < W_HEIGHT - 10:
        #print("down")
        ship.y += VEL


def asteroid_movement(asteroids):
    for asteroid in asteroids:
        asteroid[0].y += ASTEROID_SPEED 
      #  asteroid[0].x += asteroid[1]
        
        if asteroid[0].y > W_HEIGHT + 50:
            asteroids.remove(asteroid)

def handle_collision(asteroids, lasers, ship):
    for asteroid in asteroids:
        if ship.colliderect(asteroid[0]):
                pygame.event.post(pygame.event.Event(SHIP_HIT))
                SHIP_HIT_SOUND.play()
                asteroids.remove(asteroid)
                
        
        for laser in lasers:
            if asteroid[0].colliderect(laser):
                pygame.event.post(pygame.event.Event(ASTEROID_HIT))
                ASTEROID_HIT_SOUND.play()
                asteroids.remove(asteroid)
                lasers.remove(laser)
                global asteroid_score 
                asteroid_score += 1
                print(asteroid_score)
                
    

def draw_window(ship, lasers, asteroids, bg_lights, ship_health):
    WIN.fill((0, 0, 0))
    WIN.blit(SHIP_IMG, (ship.x, ship.y))
    
    for light in bg_lights:
        pygame.draw.rect(WIN, WHITE, light)

    for laser in lasers:
        pygame.draw.rect(WIN, RED, laser)

    

    for asteroid in asteroids:
       # asteroid[2] = (asteroid[2] + 1) % 360
        ASTEROID_1 = pygame.transform.rotate(ASTEROID, asteroid[2])
         # Need to find way to rotate asteroid on its center axis
        WIN.blit(ASTEROID_1, (asteroid[0].x, asteroid[0].y))

    ship_health_text = HEALTH_FONT.render("Health: " + str(ship_health), 1, WHITE)
    WIN.blit(ship_health_text, (10, 850))

    pygame.display.update()

def handle_weapons(lasers):
    for laser in lasers:
        laser.y -= LASER_VEL
       # print(laser.y)
        
        if laser.y < 0:
            lasers.remove(laser)

def handle_bg(lights):
    for light in lights:
        if light.width < 3:
            light.y += 3
        else:
            light.y += LIGHT_SPEED

        if light.y > W_HEIGHT:
            lights.remove(light)

def draw_game_over():
    draw_text = GAME_OVER_FONT.render("GAME OVER", 1, WHITE)
    WIN.blit(draw_text, (W_WIDTH // 2 - draw_text.get_width() // 2, W_HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def handle_timing():
    if (pygame.time.get_ticks() / 1000) == 20.0:
        global ASTEROID_SPEED 
        ASTEROID_SPEED += 1
        print("Increasing Asteroid speed")

def main():
    mixer.music.set_volume(0.2)
    mixer.music.play()
    clock = pygame.time.Clock()
    run = True
    ship = pygame.Rect(300, 700, SHIP_WIDTH, SHIP_HEIGHT)
    lasers = []
    asteroids = []
    bg_light = []
    for __ in range(20):
        stars = pygame.Rect(random.randint(0, 490), random.randint(0, 1000), 1, 2)
        bg_light.append(stars)
        

    ship_health = 3
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    BULLET_HIT_SOUND.play()
                    laser = pygame.Rect(ship.x + ship.width // 1.8, ship.y, 5, 10)
                    lasers.append(laser)
                    print(pygame.time.get_ticks() / 1000)
                    
            
            if event.type == SPAWN_ASTEROIDS:
                asteroid = pygame.Rect(random.randint(0, 450), -80, AST_WIDTH, AST_HEIGHT)
                asteroids.append([asteroid, random.choice([-1, 0, 1]), random.randint(0, 360)]) #Appending (asteroid object, direction)

            if event.type == BG_LIGHTRAYS:
                light = pygame.Rect(random.randint(0, 490), -30, 3, 50)
                stars = pygame.Rect(random.randint(0, 490), -30, 1, 2)
                bg_light.append(light)
                bg_light.append(stars)

            if event.type == SHIP_HIT:
                ship_health -= 1
                
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:
            run = False
            pygame.quit()

        if ship_health == 0:
            draw_game_over()
            break

        handle_timing()
        ship_movement(keys_pressed, ship)
        handle_weapons(lasers)
        asteroid_movement(asteroids)
        handle_collision(asteroids, lasers, ship)
        handle_bg(bg_light)
        draw_window(ship, lasers, asteroids, bg_light, ship_health)

if __name__ == "__main__":
    main()