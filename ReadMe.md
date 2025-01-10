# **HLF Shooting Game Documentation**

## **Overview**
The *HLF Shooting Game* is a 2D top-down shooter game built using Python and Pygame. The player controls a character, navigates through the screen, and eliminates villains by shooting bullets. The game incorporates movement, rotation, and collision mechanics to create a dynamic gaming experience.

---

## **Game Features**
1. **Player Movement**:
   - Move the main character in four directions: up, down, left, and right.
   - Rotate the character to face the direction of movement.
2. **Villain Behavior**:
   - Villains spawn at specific locations.
   - Villains move randomly and periodically shoot bullets.
   - Each villain has unique attributes like speed, rotation timing, and shooting intervals.
3. **Shooting Mechanic**:
   - The player can shoot bullets in the direction they are facing.
   - Bullets disappear when they exit the screen.
4. **Collision Detection**:
   - Bullets can hit villains, removing them from the game.
   - Collisions with the player result in game over.

---

## **Game Controls**
| Key         | Action                         |
|-------------|--------------------------------|
| `Arrow Keys`| Move the main character        |
| `Space`     | Shoot bullets                  |
---

## **Code Structure**
### **Files**
- `main.py`: Contains the main game loop and core logic.
- `models.py`: Defines reusable classes for game entities like the main character, villains, and bullets.

### **Classes**
#### 1. **MainCharacter**
- Represents the player's character.
- **Attributes**:
  - Position (`pos_x`, `pos_y`)
  - Size (`width`, `height`)
  - Speed (`speed`)
  - Direction (`direction`)
  - Polygon points representing the character.
- **Methods**:
  - `adjust_position()`: Updates the character's position.
  - `move()`: Moves the character based on the current direction.
  - `rotate_polygon()`: Rotates the character to align with the current direction.
  - `calculate_centroid()`: Finds the geometric center of the character's shape.

#### 2. **Villain**
- Represents enemy characters in the game.
- **Attributes**:
  - Position, size, speed, and direction.
  - Timers for movement, rotation, and shooting.
- **Methods**:
  - `adjust_position()`: Updates position based on movement.
  - `rotate_randomly()`: Randomizes the direction of movement.
  - `move()`: Moves the villain on the screen.
  - `calculate_centroid()`: Determines the villain's geometric center.

#### 3. **Bullet**
- Represents a projectile in the game.
- **Attributes**:
  - Position, size, and direction.
  - Source of the shot (`shot_by`).
- **Methods**:
  - `move()`: Updates the bullet's position.
  - `get_object()`: Returns the bullet's rectangle for rendering.

---

## **Core Functions**
- **`check_collision(bullet_point, polygon)`**:
  - Determines if a bullet has hit a polygonal object (character or villain).
- **`check_bullet_collision_with_villain(figure1, figure2)`**:
  - Checks if a villain has been hit by a bullet.
- **`rotate_polygon(polygon, angle, center)`**:
  - Rotates a polygon around a specified center point.

---

## **Game Loop**
1. Process user inputs for movement and shooting.
2. Update positions and states of characters, villains, and bullets.
3. Check for collisions between bullets and characters.
4. Render the game screen with updated entities.
5. Repeat the loop until the game ends.

---

## **Planned Improvements**
1. Implement a scoring system for eliminated villains.
2. Add sound effects for shooting and collisions.
3. Introduce power-ups or special abilities.
4. Expand villain behaviors with advanced AI.
5. Create multiple levels with increasing difficulty.

