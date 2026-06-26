import pygame

pygame.init()

# Window dimensions
HEIGHT = 600
WIDTH = 800

# Paddle Speed
PADDLE_SPEED = 700
AI_SPEED = 250

# Game Mode
game_mode = "one_player"
# Ball Velocity
ball_speed_x = 350
ball_speed_y = 350

# Scoreboard
player_score = 0
ai_score = 0

# Screen settings
font = pygame.font.Font(None, 60)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
                    #x    #y   #width #height
player = pygame.Rect(50, HEIGHT // 2 - 50, 20, 100)
player_two = pygame.Rect(WIDTH - 70, HEIGHT // 2 - 50, 20, 100)
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)


running = True

dt = 0

def reset_ball(scored_on_left):
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_y = 350


    if scored_on_left:
        ball_speed_x = 350 # From AI to player
    else:
        ball_speed_x = -350 # From player to AI


while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill("purple")

    # Variables for drawing the shame
    pygame.draw.rect(screen, "white", player)
    pygame.draw.rect(screen, "white", player_two)
    pygame.draw.ellipse(screen, "white", ball)

    # Move Players
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.y -= PADDLE_SPEED * dt
    if keys[pygame.K_s]:
        player.y += PADDLE_SPEED * dt
    if keys[pygame.K_ESCAPE]:
        running = False
    
    # Move Player 2

    if game_mode == "two_player":
        if keys[pygame.K_UP]:
            player_two.y -= PADDLE_SPEED * dt
        if keys[pygame.K_DOWN]:
            player_two.y += PADDLE_SPEED * dt

    elif game_mode == "one_player":
        if ball_speed_x > 0:
            if player_two.centery < ball.centery - 20:
                player_two.y += AI_SPEED * dt
            elif player_two.centery > ball.centery + 20:
                player_two.y -= AI_SPEED * dt

    # Paddles in screen
    player.y = max(0, min(player.y, HEIGHT - player.height))

    # Ball Velocity
    ball.x += ball_speed_x * dt
    ball.y += ball_speed_y * dt

    # Bouncing walls
    if ball.top <= 0:
        ball.top = 0
        ball_speed_y *= -1
    elif ball.bottom >= HEIGHT:
        ball.bottom = HEIGHT
        ball_speed_y *= -1

    # Colliding
    if ball.colliderect(player):
        ball_speed_x = abs(ball_speed_x) # Force to the right
        ball.left = player.right         # Snap ball to front

    if ball.colliderect(player_two):
        ball_speed_x = -abs(ball_speed_x)
        ball.right = player_two.left

    # Scoring:
    if ball.left <= 0:
        ai_score += 1
        print("Player 2 scores")
        reset_ball(scored_on_left = True)
    
    if ball.right >= WIDTH:
        player_score += 1
        print("Player 1 scores")
        reset_ball(scored_on_left = False)

    # Scoreboard 
    score_text = font.render(f"{player_score} {ai_score}", True, "white") 
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 30))

    
    player_two.y = max(0, min(player_two.y, HEIGHT - player_two.height))


    pygame.display.flip()


pygame.quit()
