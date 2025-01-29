import math
import pygame
import random
class Character:
    position:tuple
    points:list
    direction:str = "down"
    speed:int
    angle:float = 90 #{"down": 90, "right": 0, "up": 270, "left": 180}
    screen_coordinates:tuple
    width:int
    height:int
    center:tuple
    dead:bool
    
    def initial_rotate(self):
        if self.is_on_screen():
            directions = {"down": 90, "right": 0, "up": 270, "left": 180}
            angle = directions[self.direction] % 360 
            angle_to_rotate = (angle - 90) % 360 
            center = self.calculate_centroid()
            polygon = self.points
            angle_rad = math.radians(angle_to_rotate)
            cos_theta = math.cos(angle_rad)
            sin_theta = math.sin(angle_rad)
            cx, cy = center

            rotated_polygon = []
            for x, y in polygon:
                translated_x = x - cx
                translated_y = y - cy

                rotated_x = translated_x * cos_theta - translated_y * sin_theta
                rotated_y = translated_x * sin_theta + translated_y * cos_theta

                final_x = rotated_x + cx
                final_y = rotated_y + cy

                rotated_polygon.append((final_x, final_y))
            self.points = rotated_polygon
            self.angle = angle
        else:
            self.reverse_move()
        self.center = self.calculate_centroid()     
    def adjust_position(self):
        self.points = [(x + self.position[0], y + self.position[1]) for x, y in self.points]

    def calculate_centroid(self, points = []):
        """Calculates the centroid of a polygon."""
        polygon = self.points if points == [] else points
        n = len(polygon)
        cx = math.ceil(sum(x for x, y in polygon) / n)
        cy = math.ceil(sum(y for x, y in polygon) / n)
        return (cx, cy)
    def reverse_move(self):
        if self.direction == "up":
            self.direction = "down"
            self.points = [(x, y - int(self.height/2) ) for x, y in self.points ]
            self.rotate()
            print("down")
            return
        if self.direction == "down":
            self.direction = "up"
            self.points = [(x, y + int(self.height/2) ) for x, y in self.points ]
            self.rotate()
            print("up")
            return
        if self.direction == "left":
            self.direction = "right"
            self.points = [(x - int(self.width/2), y ) for x, y in self.points ]
            self.rotate()

            print("right")
            return
        if self.direction == "right":
            self.direction = "left"
            self.points = [(x + int(self.width/2), y) for x, y in self.points ]
            self.rotate()
            print("left")
            return
        

    def move(self):
        """Moves the Character by self.speed in self.direction"""
        if self.speed < 0:
            self.speed = 0
        center = self.calculate_centroid()
        # if self.is_on_screen():
        if self.direction == "up":
            self.points = [(x, y - self.speed ) for x, y in self.points ] if center[1] - self.speed > int(self.height/2) else [(x, y + int(self.height/2) ) for x, y in self.points ]
        if self.direction == "down":
            self.points = [(x, y + self.speed ) for x, y in self.points ] if center[1] + self.speed < self.screen_coordinates[1] - int(self.height/2) else [(x, y - int(self.height/2) ) for x, y in self.points ] 
        if self.direction == "left":
            self.points = [(x - self.speed, y ) for x, y in self.points ] if center[0] - self.speed > int(self.width/2) else [(x + int(self.width/2), y ) for x, y in self.points ]
        if self.direction == "right":
            self.points = [(x + self.speed, y) for x, y in self.points ] if center[0] + self.speed < self.screen_coordinates[0] - int(self.width/2) else [(x - int(self.width/2), y) for x, y in self.points ]
        
        
    def is_on_screen(self):
        cx, cy = self.calculate_centroid()
        if cx < int(self.width/2) or cx > self.screen_coordinates[0] or cy < int(self.height/2) or cy > self.screen_coordinates[1]:
            return False  # Center is out of the screen
        return True

    
    def rotate(self, angle = None):
        if self.is_on_screen():
            directions = {"down": 90, "right": 0, "up": 270, "left": 180}
            angle = directions[self.direction] % 360 
            angle_to_rotate = (angle - self.angle) % 360 
            center = self.calculate_centroid()
            polygon = self.points
            angle_rad = math.radians(angle_to_rotate)
            cos_theta = math.cos(angle_rad)
            sin_theta = math.sin(angle_rad)
            cx, cy = center

            rotated_polygon = []
            for x, y in polygon:
                translated_x = x - cx
                translated_y = y - cy

                rotated_x = translated_x * cos_theta - translated_y * sin_theta
                rotated_y = translated_x * sin_theta + translated_y * cos_theta

                final_x = rotated_x + cx
                final_y = rotated_y + cy

                rotated_polygon.append((final_x, final_y))
            self.points = rotated_polygon
            self.angle = angle
        else:
            self.reverse_move()
        self.center = self.calculate_centroid()

class Bullet(Character):
    def __init__(self, speed,shot_by,width:int = 15, height:int = 15):
        if isinstance(shot_by,Villain) or isinstance(shot_by, Player):
            self.shot_by = shot_by
        else:
            raise ValueError("Bullet must be shot by a Villain or Player")

        self.width = width
        self.height = height
        self.speed = speed
        self.screen_coordinates = self.shot_by.screen_coordinates
        self.direction = self.shot_by.direction 
        self.position = self.shot_by.points[-4]
        self.center = self.shot_by.calculate_centroid()
        self.points = [(self.center[0]-10, self.center[1]-10)] if self.direction == "up" or self.direction == "right" else [(self.center[0] -5, self.center[1]-5)]
        self.angle = {"right": 180, "up": 90, "left": 0, "down": 270}[self.direction]
        self.object = pygame.Rect(self.position[0], self.position[1], self.width, self.height)
        self.direction = shot_by.direction
        # self.adjust_position()

    def get_object(self):
        center = self.points[0]
        return pygame.Rect(center[0], center[1], self.width, self.height)
    def move(self):
        if self.direction == "up":
            self.points = [(x, y - self.speed ) for x, y in self.points ] 
        if self.direction == "down":
            self.points = [(x, y + self.speed ) for x, y in self.points ] 
        if self.direction == "left":
            self.points = [(x - self.speed, y ) for x, y in self.points ] 
        if self.direction == "right":
            self.points = [(x + self.speed, y) for x, y in self.points ]   
        # print(self.direction)     

    def rotate(self, angle=None):
            directions = {"down": 90, "right": 0, "up": 270, "left": 180}
            angle = directions[self.direction] % 360
            angle_to_rotate = (angle - self.angle) % 360
            center = self.calculate_centroid()
            polygon = self.points
            angle_rad = math.radians(angle_to_rotate)
            cos_theta = math.cos(angle_rad)
            sin_theta = math.sin(angle_rad)
            cx, cy = center

            rotated_polygon = []
            for x, y in polygon:
                translated_x = x - cx
                translated_y = y - cy

                rotated_x = translated_x * cos_theta - translated_y * sin_theta
                rotated_y = translated_x * sin_theta + translated_y * cos_theta

                final_x = rotated_x + cx
                final_y = rotated_y + cy

                rotated_polygon.append((final_x, final_y))
            self.points = rotated_polygon
            self.angle = angle
            print(f"Original: {angle} Rotated:{angle_to_rotate}")

    

class Villain(Character):
    
    def __init__(self, position:tuple, direction:str, screen_coordinates:tuple, speed:int=10, width=45, height=45) -> None:
        self.position = position
        self.direction = direction
        self.screen_coordinates = screen_coordinates
        self.speed = speed
        self.angle = {"right": 180, "up": 90, "left": 0, "down": 270}[direction]
        self.bullets = []
        self.width = width
        self.height = height
        self.points = [(10, 10), (10, 40), (25, 40), (25, 55), (40, 55), (40, 40),(55, 40), (55, 10), (40, 10), (40, 25), (25, 25), (25, 10),(10, 10)]
        self.initial_rotate()
        self.center = self.calculate_centroid()
        self.adjust_position()
        self.dead = False
        self.revived = False
    
    def shoot(self):
        self.bullets.append(Bullet(speed=20, shot_by=self))
    

    

class Player(Character):
    def __init__(self, position:tuple, direction:str, screen_coordinates:tuple, speed:int=10, width=45, height=45) -> None:
        self.position = position
        self.direction = direction
        self.screen_coordinates = screen_coordinates
        self.speed = speed
        self.angle = {"right": 180, "up": 90, "left": 0, "down": 270}[self.direction]
        self.bullets = []
        self.width = width
        self.height = height
        self.points = [(10,10),(10,40),(25,40),(25,55),(40,55),(40,40),(55,40),(55,10),(10,10)]

        self.rotate()
        self.adjust_position()
        self.center = self.calculate_centroid()
        self.dead = False
    
    def shoot(self):
        self.bullets.append(Bullet(speed=20, shot_by=self))



class GameLevel:
    def __init__(self, level_number:int, level_speed:int):
        self.level_number = level_number
        self.level_speed = level_speed
        self.number_of_villaisn = 4 + self.level_number
    


class VillainController:

    def __init__(self, villain:Villain, player:Player, operate_time=1000):

        self.villain = villain
        self.player = player
        self.pace_moved = 0
        self.shoot_while_in_motion = True
        self.operate_time = operate_time
    
    def regenerate(self):
        self.villain.revived = True
        self.villain.dead = False
        direction = ['up', 'down'][random.randint(0,1)] if self.villain.direction == "left" or self.villain.direction == "right" else ['left', 'down'][random.randint(0,1)]
        # pos = (100, 100)
        pos = (random.randint(0,self.villain.screen_coordinates[0]),random.randint(0,self.villain.screen_coordinates[1]))
        self.villain = Villain(pos, direction, self.villain.screen_coordinates)
        self.operate_time = random.randint(100,500)
    def operate(self, counter):
        # if self.shoot_while_in_motion:

        if counter % self.operate_time == 0:
            
            if self.shoot_while_in_motion:
                self.villain.shoot()
            else:
                if (counter*1/3) % self.operate_time == 0:
                    self.villain.shoot()
                    return 
                
            
            if self.pace_moved < 4 and self.villain.is_on_screen():
                self.villain.move()
                self.pace_moved += 1
                return
            else:
                direction = "left"
                if self.villain.direction == "right" or self.villain.direction == "left":
                    direction = ["up", "down"][random.randint(0,1)]
                if self.villain.direction == "up" or self.villain.direction == "down":
                    direction = ["left", "right"][random.randint(0,1)]
                self.villain.direction = direction
                self.villain.rotate()

                self.pace_moved = 0
                return

class MainController:

    def __init__(self, sub_contrllers:list[VillainController] = []):
        self.sub_controllers = sub_contrllers
        pass

    def operate(self, counter:int = 100):
        for controller in self.sub_controllers:
            controller.operate(counter)

        