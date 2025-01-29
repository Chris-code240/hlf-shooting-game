import pygame
import math
from gamemodels import Villain, Bullet, Player, GameLevel, VillainController, MainController
import random
import sys
import time
# Pygame setup
pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HLF Shooting Game")
clock = pygame.time.Clock()
player_height=45
player_width= 45
player_color = (0, 250, 10)
villains_on_screen:list[Villain] = []
contrllers = []

game_level = GameLevel(1, 10)

villains_on_screen.append(Villain(((player_width/2), HEIGHT- player_height-(player_height/2)),"up",(WIDTH, HEIGHT),game_level.level_speed))

villains_on_screen.append(Villain((WIDTH-player_width - (player_width/2), HEIGHT- player_height-(player_height/2)),"up",(WIDTH, HEIGHT),game_level.level_speed) )

villains_on_screen.append(Villain((WIDTH-player_width - (player_width/2), int(player_height/2)),"down",(WIDTH, HEIGHT),10))

villain = Villain((player_width/2, int(player_height/2)),"down",(WIDTH, HEIGHT),game_level.level_speed)
villains_on_screen.append(villain)


player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT // 2 - player_height // 2

player = Player((player_x, player_y),"up",(WIDTH, HEIGHT),10)
current_direction = player.direction
bullets = []

for i in villains_on_screen:
    i.speed = random.randint(20, 100)
    contrllers.append(VillainController(i, player, random.randint(100, 150)))

main_contrller = MainController(contrllers)
counter = 0

def resolve_level():
    global villains_on_screen
    main_contrller.sub_controllers = [c for c in main_contrller.sub_controllers if not c.villain.dead]
    villains_on_screen = [v for v in villains_on_screen if not v.dead]
    if len(villains_on_screen) < game_level.number_of_villaisn:
        for i in range( game_level.number_of_villaisn - len(villains_on_screen)):
            villain = Villain((random.randint(int(player_width/2), WIDTH), random.randint(int(player_height/2), HEIGHT)),['up', 'right', 'down', 'left'][random.randint(0, 3)], player.screen_coordinates, game_level.level_speed)
            villains_on_screen.append(villain)
            controller = VillainController(villain, player, operate_time=random.randint(100, 150))
            main_contrller.sub_controllers.append(controller)

def check_collision(character, bullet:Bullet):
    """
    Check if any point of a polygon collides with a pygame.Rect.

    :param rect: pygame.Rect object
    :param polygon_points: List of (x, y) tuples representing the polygon's points
    :return: True if any point collides with the rect, False otherwise
    """
    if isinstance(bullet.shot_by, Villain) and isinstance(character, Villain):
        return False
    if isinstance(bullet.shot_by, Player) and isinstance(character, Player):
        return False
    for point in character.points:
        if bullet.get_object().collidepoint(point):
            return True
    return False
while True:
    counter += 10
    #remove dead villains

    main_contrller.operate(counter = counter)
    villains_on_screen = [v for v in villains_on_screen if v.dead == False]
    for v in villains_on_screen:
        bullets += v.bullets
    bullets = [b for b in bullets+player.bullets if b.points[0][0] >=0 and b.points[0][0] <= WIDTH and b.points[0][1] >=0 and b.points[0][1] <= HEIGHT]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    

    keys = pygame.key.get_pressed()
    # player_center = player.calculate_centroid()
 
    
       
    if keys[pygame.K_RIGHT]:
        if current_direction != "right":
            player.direction = "right"
            player.rotate()
        else:
            player.move()

    if keys[pygame.K_LEFT]:
        if current_direction != "left":
            player.direction = "left"
            player.rotate()
        else:
            player.move()


    if keys[pygame.K_UP]:
        if current_direction != "up":
            player.direction = "up"
            player.rotate()
            
        else:
            player.move()

    if keys[pygame.K_DOWN]:
        if current_direction != "down":
            player.direction = "down"
            player.rotate()
        else:
            player.move()
    current_direction = player.direction
   

    if keys[pygame.K_SPACE]:
        player.shoot()

  


    screen.fill((0, 0, 0))
    for b in bullets:
            for v in villains_on_screen+[player]:
                if check_collision(v, b):
                    v.dead = True
                    if isinstance(v, Player):
                        player_color = (200, 10, 0)
                        game_level = GameLevel(game_level.level_number + 1, game_level.level_speed + 10)
                        resolve_level()
                    continue
            if counter % 10 == 0:
                b.move()
            pygame.draw.rect(screen, (255, 255, 255), b.get_object())
    pygame.draw.polygon(screen, player_color, player.points) 



    for v in villains_on_screen:
        pygame.draw.polygon(screen, (0, 250, 10), v.points)  

    for b in bullets:
        player.dead = check_collision(player, b)
 
    pygame.display.flip()
    clock.tick(60)




