import pygame
import math
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self-Driving Car Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Car properties
CAR_WIDTH, CAR_HEIGHT = 40, 20
car_x, car_y = WIDTH // 2, HEIGHT - 100
car_angle = 0
car_speed = 5

# Road properties
ROAD_WIDTH = 200
road_x = (WIDTH - ROAD_WIDTH) // 2

# Obstacle properties
obstacles = [
    {"x": road_x + ROAD_WIDTH // 4, "y": 200, "width": 40, "height": 40},
    {"x": road_x + 3 * ROAD_WIDTH // 4, "y": 100, "width": 40, "height": 40}
]

# Banner properties
BANNER_HEIGHT = 50
font = pygame.font.SysFont("Arial", 24)
banner_text = "Coded by Pakistani Ethical Hacker Mr Sabaz Ali Khan"
banner_text_surface = font.render(banner_text, True, WHITE)

# Sensor properties
SENSOR_LENGTH = 100
SENSOR_ANGLE_OFFSETS = [-30, 0, 30]  # Degrees relative to car angle

FPS = 60
clock = pygame.time.Clock()

def draw_car(x, y, angle):
    car_surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
    car_surface.fill(RED)
    rotated_car = pygame.transform.rotate(car_surface, -angle)
    car_rect = rotated_car.get_rect(center=(x, y))
    screen.blit(rotated_car, car_rect.topleft)
    return car_rect

def draw_road():
    pygame.draw.rect(screen, GRAY, (road_x, 0, ROAD_WIDTH, HEIGHT))
    # Draw lane markings
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, WHITE, (WIDTH // 2, y), (WIDTH // 2, y + 20), 2)

def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, (obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))

def draw_banner():
    pygame.draw.rect(screen, GREEN, (0, 0, WIDTH, BANNER_HEIGHT))
    text_rect = banner_text_surface.get_rect(center=(WIDTH // 2, BANNER_HEIGHT // 2))
    screen.blit(banner_text_surface, text_rect)

def draw_sensors(car_x, car_y, car_angle, car_rect):
    sensor_data = []
    for offset in SENSOR_ANGLE_OFFSETS:
        angle_rad = math.radians(car_angle + offset)
        end_x = car_x + SENSOR_LENGTH * math.cos(angle_rad)
        end_y = car_y - SENSOR_LENGTH * math.sin(angle_rad)
        pygame.draw.line(screen, WHITE, (car_x, car_y), (end_x, end_y), 1)
        
        # Check for collision with obstacles
        sensor_rect = pygame.Rect(min(car_x, end_x), min(car_y, end_y), 
                                abs(end_x - car_x), abs(end_y - car_y))
        collision = False
        for obstacle in obstacles:
            obs_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"])
            if sensor_rect.colliderect(obs_rect):
                collision = True
                break
        sensor_data.append(collision)
    return sensor_data

def move_car(sensor_data):
    global car_x, car_y, car_angle
    # Simple self-driving logic: avoid obstacles
    if sensor_data[1]:  # Front sensor detects obstacle
        car_speed = 0
    else:
        car_speed = 5
        if sensor_data[0]:  # Left sensor detects obstacle
            car_angle += 5
        elif sensor_data[2]:  # Right sensor detects obstacle
            car_angle -= 5
    
    # Keep car within road bounds
    if car_x < road_x + CAR_WIDTH // 2:
        car_angle -= 5
    elif car_x > road_x + ROAD_WIDTH - CAR_WIDTH // 2:
        car_angle += 5
    
    # Update car position
    angle_rad = math.radians(car_angle)
    car_x += car_speed * math.cos(angle_rad)
    car_y -= car_speed * math.sin(angle_rad)

def setup():
    pass  # Initialization if needed

def update_loop():
    global car_x, car_y
    screen.fill(BLACK)
    draw_road()
    draw_obstacles()
    draw_banner()
    car_rect = draw_car(car_x, car_y, car_angle)
    sensor_data = draw_sensors(car_x, car_y, car_angle, car_rect)
    move_car(sensor_data)
    pygame.display.flip()
    
    # Move obstacles (simulate scrolling road)
    for obstacle in obstacles:
        obstacle["y"] += 2
        if obstacle["y"] > HEIGHT:
            obstacle["y"] = -obstacle["height"]

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())