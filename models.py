import math
import json
import pygame
import random
def calculate_centroid(polygon):
    """Calculates the centroid of a polygon."""
    n = len(polygon)
    cx = math.ceil(sum(x for x, y in polygon) / n)
    cy = math.ceil(sum(y for x, y in polygon) / n)
    return (cx, cy)

def rotate_polygon(polygon, angle, center):
    """Rotates a polygon around its center."""
    angle_rad = math.radians(angle)
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

    return rotated_polygon


class Character:
    pos_x:float
    pos_y:float
    width:float
    height:float
    direction:str
    speed:float
    points:list
    def calculate_centroid(self):
        """Calculates the centroid of a polygon."""
        polygon = self.points
        n = len(polygon)
        cx = math.ceil(sum(x for x, y in polygon) / n)
        cy = math.ceil(sum(y for x, y in polygon) / n)
        return (cx, cy)

    def rotate_polygon(self, angle, center):
        """Rotates a polygon around its center."""
        pass

class MainCharacter(Character):

    def __init__(self, screen_height, screen_width,pos_x, pos_y, width, height, direction = "up",speed = 5):
        directions = {"right": 0, "down": 90, "left": 180, "up": 270}
        self.screen_height, self.screen_width = screen_height, screen_width
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.direction = direction
        self.speed = speed
        self.angle = directions[direction]
        self.points = [(10,10),(10,40),(25,40),(25,55),(40,55),(40,40),(55,40),(55,10),(10,10)]
        self.adjust_position()
        self.rotate_polygon()

    def adjust_position(self):
        self.points = [(x + self.pos_x, y + self.pos_y) for x, y in self.points]

    def move(self):
        if self.direction == "up":
            self.pos_y = -self.speed
            self.pos_x = 0
            self.adjust_position()
        if self.direction == "down":
            self.pos_x = 0
            self.pos_y = self.speed
            self.adjust_position()
        if self.direction == "left":
            self.pos_y = 0
            self.pos_x = -self.speed
            self.adjust_position()          
        if self.direction == "right":
            self.pos_y = 0
            self.pos_x = self.speed
            self.adjust_position() 
    def rotate_polygon(self):
        directions = {"right": 180, "up": 90, "left": 0, "down": 270}
        angle = directions[self.direction] % 360
        angle_to_rotate = (angle - self.angle) % 360
        self.angle = angle
        center = calculate_centroid(self.points)
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
        return super().rotate_polygon(angle, center) 



class Villain(Character):

    def __init__(self,main_character:MainCharacter, pos_x, pos_y, width, height, direction = "up",speed = 20, move_time = 0.5,rotate_time = 5,shoot_time=1, refresh_rate=60):
        """
        Initializes a Villain object
        """
        self.points = [(10,10),(10,40),(25,40),(25,55),(40,55),(40,40),(55,40),(55,10),(40,10),(40,25),(25,25),(25,10),(10,10)]
        directions = {"right": 0, "down": 90, "left": 180, "up": 270}
        self.main_character = main_character
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.direction = direction
        self.speed = speed
        self.angle = directions[direction]
        self.rotate_polygon()
        self.adjust_position()
        self.move_time = move_time * refresh_rate
        self.rotate_time = rotate_time * refresh_rate #rotate after 5seconds
        self.rotating = False
        self.moving = False
        self.shoot_time = shoot_time * refresh_rate

    def adjust_position(self):
        self.points = [(x + self.pos_x, y + self.pos_y) for x, y in self.points]

    def move(self):
        center = self.calculate_centroid()
        if center[0] < self.width or center[0] > self.main_character.screen_width - self.width or center[1] < self.height or center[1] > self.main_character.screen_height - self.height:
            self.rotate_opposite()
        if self.direction == "up":
            self.pos_y = -self.speed
            self.pos_x = 0
            self.adjust_position()
        if self.direction == "down":
            self.pos_x = 0
            self.pos_y = self.speed
            self.adjust_position()
        if self.direction == "left":
            self.pos_y = 0
            self.pos_x = -self.speed
            self.adjust_position()          
        if self.direction == "right":
            self.pos_y = 0
            self.pos_x = self.speed
            self.adjust_position()
        self.moving = False

    def rotate_opposite(self):
        """
        Rotates the polygon in opposite direction
        :Don't worry about the value of self.rotating before calling
        """
        self.direction = "up" if self.direction == "down" else "left" if self.direction == "right" else "right" if self.direction == "left" else "down"

        self.rotating = True
        self.rotate_polygon()
        self.rotating = False
 
    def rotate_polygon(self):
        """
        Rotates the polygon in the direction of self.direction ['left', 'right','up','down']
        """
        directions = {"right": 180, "up": 90, "left": 0, "down": 270}
        angle = directions[self.direction] % 360
        angle_to_rotate = (angle - self.angle) % 360
        self.angle = angle
        center = calculate_centroid(self.points)
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
        return super().rotate_polygon(angle, center) 

    def rotate_randomly(self):

        if self.moving or not self.rotating:
            return
        
        if self.direction == "up" or self.direction == "down":
            random_direction = ["left", "right"][random.randint(0, 1)]
            self.direction = random_direction
            self.rotate_polygon()
            self.rotating = False
            return
        if self.direction == "left" or self.direction == "right":
            random_direction = ["up", "down"][random.randint(0, 1)]
            self.direction = random_direction
            self.rotate_polygon()
            self.rotating = False
            return         

    def move_only(self):
        if self.direction == "up":
            self.pos_y = -self.speed
            self.pos_x = 0
            self.adjust_position()
        if self.direction == "down":
            self.pos_x = 0
            self.pos_y = self.speed
            self.adjust_position()
        if self.direction == "left":
            self.pos_y = 0
            self.pos_x = -self.speed
            self.adjust_position()          
        if self.direction == "right":
            self.pos_y = 0
            self.pos_x = self.speed
            self.adjust_position()
        self.moving = False
    def get_random_action(self):
        action = ["shoot", "move", "rotate"][random.randint(0,2)]
        return action

class Bullet(Character):

    def __init__(self, shot_by, pos_x, pos_y,width = 15, height= 15, speed = 20, direction = "up"):
        self.shot_by = shot_by
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = direction
        self.points = [self.pos_x, self.pos_y]
        self.object = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def adjust_position(self):
        self.points = [self.points[0]+self.pos_x,self.points[1]+ self.pos_y]
        self.object.x += self.pos_x
        self.object.y += self.pos_y
    def move(self):
        if self.direction == "up":
            self.pos_y = -self.speed
            self.pos_x = 0
            self.adjust_position()
        if self.direction == "down":
            self.pos_x = 0
            self.pos_y = self.speed
            self.adjust_position()
        if self.direction == "left":
            self.pos_y = 0
            self.pos_x = -self.speed
            self.adjust_position()          
        if self.direction == "right":
            self.pos_y = 0
            self.pos_x = self.speed
            self.adjust_position()   
    
    def get_object(self):
        return self.object
    


    
    