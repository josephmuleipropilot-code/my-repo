import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


player_x = 100
player_y = 400
player_size = 40
player_vel_y = 0


GRAVITY = 0.8
JUMP_STRENGTH = -15
GROUND_Y = 500

scroll_speed = 5
score = 0
high_score = 0

obstacles = []


last_obstacle_x = 800
min_gap = 200  
max_gap = 400  

running = True
on_ground = False
game_over = False

def generate_obstacle():
    """Generate a random obstacle"""
    obstacle_type = random.choice(["spike", "spike", "spike", "double_spike", "platform"])
    
    if obstacle_type == "spike":
        return [last_obstacle_x, GROUND_Y - 40, 40, 40, "spike"]
    elif obstacle_type == "double_spike":
        
        obstacles.append([last_obstacle_x, GROUND_Y - 40, 40, 40, "spike"])
        return [last_obstacle_x + 60, GROUND_Y - 40, 40, 40, "spike"]
    elif obstacle_type == "platform":
        height = random.randint(60, 150)
        width = random.randint(80, 150)
        return [last_obstacle_x, GROUND_Y - height, width, 20, "platform"]

def reset_game():
    """Reset game state"""
    global player_y, player_vel_y, on_ground, game_over, obstacles, last_obstacle_x, score, scroll_speed
    player_y = 400
    player_vel_y = 0
    on_ground = False
    game_over = False
    obstacles = []
    last_obstacle_x = 800
    score = 0
    scroll_speed = 5

for i in range(3):
    last_obstacle_x += random.randint(min_gap, max_gap)
    obstacles.append(generate_obstacle())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_ground:
                    player_vel_y = JUMP_STRENGTH
                    on_ground = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and on_ground:
                player_vel_y = JUMP_STRENGTH
                on_ground = False
        else:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if score > high_score:
                    high_score = score
                reset_game()
    
    if not game_over:
        player_vel_y += GRAVITY
        player_y += player_vel_y
        
        if player_y + player_size >= GROUND_Y:
            player_y = GROUND_Y - player_size
            player_vel_y = 0
            on_ground = True
        
        for obstacle in obstacles:
            obstacle[0] -= scroll_speed
    
        obstacles = [obs for obs in obstacles if obs[0] > -200]

        if len(obstacles) == 0 or obstacles[-1][0] < 600:
            last_obstacle_x = obstacles[-1][0] if obstacles else 800
            last_obstacle_x += random.randint(min_gap, max_gap)
            obstacles.append(generate_obstacle())
        
        score += 1
        
        if score % 500 == 0 and scroll_speed < 12:
            scroll_speed += 0.3
        

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        
        for obstacle in obstacles:
            obs_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3])
            
            if player_rect.colliderect(obs_rect):
                if obstacle[4] == "spike":
                    game_over = True
                elif obstacle[4] == "platform":
                    if player_vel_y > 0 and player_y + player_size - player_vel_y <= obstacle[1]:
                        player_y = obstacle[1] - player_size
                        player_vel_y = 0
                        on_ground = True
    
    screen.fill((135, 206, 235))

    pygame.draw.rect(screen, (100, 100, 100), (0, GROUND_Y, 800, 100))
    
    for obstacle in obstacles:
        if obstacle[4] == "spike":
            points = [
                (obstacle[0], obstacle[1] + obstacle[3]),
                (obstacle[0] + obstacle[2] // 2, obstacle[1]),
                (obstacle[0] + obstacle[2], obstacle[1] + obstacle[3])
            ]
            pygame.draw.polygon(screen, (255, 0, 0), points)
        elif obstacle[4] == "platform":
            pygame.draw.rect(screen, (150, 75, 0), (obstacle[0], obstacle[1], obstacle[2], obstacle[3]))
    
    color = (100, 100, 100) if game_over else (255, 255, 0)
    pygame.draw.rect(screen, color, (player_x, player_y, player_size, player_size))
    
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score // 10}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    speed_text = font.render(f"Speed: {scroll_speed:.1f}", True, (0, 0, 0))
    screen.blit(speed_text, (10, 50))
    
    high_score_text = font.render(f"High: {high_score // 10}", True, (0, 0, 0))
    screen.blit(high_score_text, (650, 10))
    
    if game_over:
        font_large = pygame.font.Font(None, 74)
        text = font_large.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (230, 200))
        
        font_small = pygame.font.Font(None, 36)
        text_small = font_small.render("Click to restart", True, (0, 0, 0))
        screen.blit(text_small, (270, 300))
        
        final_score = font_small.render(f"Final Score: {score // 10}", True, (0, 0, 0))
        screen.blit(final_score, (280, 350))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()