import pygame
import math
from models import  MainCharacter, Villain, Bullet
import random
import sys
# Pygame setup
pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HLF Shooting Game")
clock = pygame.time.Clock()

# Character setup
player_width, player_height = [45, 45]
player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT // 2 - player_height // 2
player_speed = 5
villain_width, villain_height, villain_speed = [45, 45, 20]
main_character = MainCharacter(HEIGHT, WIDTH,player_x, player_y, player_width, player_height)

villain = Villain(main_character,100, 100, player_width, player_height,"down")
# rotate_polygon(main_character, 180, calculate_centroid(main_character))
villains_on_screen = list()
villains_on_screen.append(Villain(main_character,100, 100, villain_width, villain_height, "up", villain_speed,2,4,1,60))
villains_on_screen.append(Villain(main_character,WIDTH-100, 100, villain_width, villain_height, "up", villain_speed,0.5,6,2,60))
villains_on_screen.append(Villain(main_character,WIDTH-100, HEIGHT-100, villain_width, villain_height, "up", villain_speed,1.5,5,1,60))
villains_on_screen.append(Villain(main_character,50, HEIGHT-100, villain_width, villain_height, "up", villain_speed,1,3,2,60))
current_direction = main_character.direction
counter = 0
bullets = []
eliminated_color = (255, 0, 0)
color = (255, 255, 255)
main_character_bullets = []
main_character_dead = False
def check_collision(bullet_point:tuple, polygon:list):
    x,y = bullet_point
    inside = False
    n = len(polygon)
    px1, py1 = polygon[0]
    for i in range(n +1):
        px2, py2 = polygon[i % n]
        if y  > min(py1, py2):
            if y <= max(py1, py2):
                if x <= max(px1, px2):
                    if py1 != py2:
                        xinters = (y - py1) * (px2 - px1) / (py2 - py1) + px1
                        if px1 == px2 or x <= xinters:
                            inside = not inside
        px1,py1 = px2, py2
    return inside

    
def check_bullet_collision_with_villain(figure1:Villain, figure2:Bullet):
    if figure2.shot_by == main_character:
        return False
    for point in figure1.points:
        return figure2.object.collidepoint(point)
        figure2.object.collideobjectsall()
    return False
    
while not main_character_dead:
    counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    bullets = [b for b in bullets if  b.object.x < WIDTH and b.object.y < HEIGHT and b.object.x > 0 and b.object.y > 0 and (b.shot_by in villains_on_screen or b.shot_by == main_character)]

    keys = pygame.key.get_pressed()
    main_character_center = main_character.calculate_centroid()
    if keys[pygame.K_RIGHT]:
        if current_direction != "right":
            main_character.direction = "right"
            main_character.rotate_polygon()
            current_direction = main_character.direction
        if main_character_center[0] < WIDTH:
            main_character.pos_x = player_speed
            main_character.pos_y = 0
            main_character.adjust_position()

    if keys[pygame.K_LEFT]:
        if current_direction != "left":
            main_character.direction = "left"
            main_character.rotate_polygon()
            current_direction = main_character.direction
        if main_character_center[0] > 0:
            main_character.move()


    if keys[pygame.K_UP]:
        if current_direction != "up":
            main_character.direction = "up"
            main_character.rotate_polygon()
            current_direction = main_character.direction

        if main_character_center[1]> 0:
            main_character.move()

    if keys[pygame.K_DOWN]:
        if current_direction != "down":
            main_character.direction = "down"
            main_character.rotate_polygon()
            current_direction = main_character.direction
        if main_character_center[1] < HEIGHT:
            main_character.move()

    if keys[pygame.K_SPACE]:
        
        main_character_bullets.append(Bullet(main_character,main_character_center[0]-player_width //2,main_character_center[1] -player_height//2,direction=current_direction))
    for villain in villains_on_screen:
        if counter % villain.rotate_time == 0:
            villain.rotating = True
            villain.rotate_randomly()
        villain_center = villain.calculate_centroid()
        if counter % villain.move_time == 0:
            villain.moving = True
            villain.move()
        if counter % villain.shoot_time == 0:
            v_center = villain.calculate_centroid()
            bullets.append(Bullet(main_character,v_center[0]-player_width //2,v_center[1] -player_height//2,direction=villain.direction))

    screen.fill((0, 0, 0))
   
    # Draw bullets

    for bullet in bullets + main_character_bullets:
        bullet.move()
        # main_character_dead = True if check_collision((bullet.object.x, bullet.object.y), main_character.points) else False
        pygame.draw.rect(screen,(255, 255, 255), bullet.get_object())

    for bullet in main_character_bullets:
        villains_on_screen = [v for v in villains_on_screen if not check_collision((bullet.object.x, bullet.object.y),v.points)]

    pygame.draw.polygon(screen, (0, 250, 10), main_character.points)

    for villain in villains_on_screen:
        pygame.draw.polygon(screen, color, villain.points)



    pygame.display.flip()
    clock.tick(60)



