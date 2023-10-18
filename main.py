# Import necessary libraries
import pygame
import math

# Initialize the pygame library
pygame.init()

# Set up the display window
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity simulation")

# Define constants for the simulation
PLANET_MASS = 250
SHIP_MASS = 50
G = 5  # Gravitational constant
FPS = 60
PLANET_SIZE = 50
OBJ_SIZE = 5
VEL_SCALE = 50  # Scaling factor for velocity

# Load background and planet images
BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
CENTER = pygame.transform.scale(pygame.image.load("jupiter.png"), (PLANET_SIZE * 2, PLANET_SIZE * 2))

# Define color constants
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define a class for the planet
class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass

    def draw(self):
        win.blit(CENTER, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))

# Define a class for spacecraft
class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet=None):
        if planet:
            # Calculate the distance between the spacecraft and the planet
            distance = math.sqrt((self.x - planet.x) ** 2 + (self.y - planet.y) ** 2)

            # Calculate the gravitational force using Newton's law of universal gravitation
            force = (G * self.mass * planet.mass) / distance ** 2

            # Calculate the acceleration due to the gravitational force
            acc = force / self.mass

            # Calculate the angle of the force vector
            angle = math.atan2(planet.y - self.y, planet.x - self.x)

            # Calculate the components of acceleration in x and y directions
            acc_x = acc * math.cos(angle)
            acc_y = acc * math.sin(angle)

            # Update the velocity components
            self.vel_x += acc_x
            self.vel_y += acc_y

        # Update the position based on velocity
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self):
        # Draw the spacecraft as a circle on the screen
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)


# Function to create a spacecraft
def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse

    # Calculate initial velocity based on the difference between the click and release positions
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE

    # Create a spacecraft object with the calculated velocity
    obj = Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)
    return obj

# Main simulation loop
def main():
    running = True
    clock = pygame.time.Clock()

    # Create the planet object
    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)

    # Create a list to store spacecraft objects
    objects = []

    # Variable to store the initial click position
    temp_obj_pos = None

    while running:
        clock.tick(FPS)

        # Get the current mouse position
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    # If there was a previous click (temp_obj_pos), create a spacecraft and add it to the list
                    t_x, t_y = temp_obj_pos
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    # If there was no previous click, store the current click position
                    temp_obj_pos = mouse_pos

        # Draw the background
        win.blit(BG, (0, 0))

        # Draw a line from the initial click position to the current mouse position
        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)

        for obj in objects[:]:
            obj.draw()
            obj.move(planet)

            # Check if the spacecraft is off-screen or has collided with the planet
            off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
            collided = math.sqrt((obj.x - planet.x) ** 2 + (obj.y - planet.y) ** 2) <= PLANET_SIZE

            # Remove the spacecraft if it's off-screen or has collided
            if off_screen or collided:
                objects.remove(obj)

        # Draw the planet
        planet.draw()

        # Update the display
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
