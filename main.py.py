import pygame
import sys

pygame.init()

# ----- WINDOW SETTINGS -----
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pickleball Game (Pygame)")

# ----- COLORS -----
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)

# ----- GAME OBJECTS -----
paddle_width = 15
paddle_height = 80
ball_size = 15

# Paddles (Left = Team A, Right = Team B)
paddleA_y = HEIGHT // 2 - paddle_height // 2
paddleB_y = HEIGHT // 2 - paddle_height // 2
paddle_speed = 6

# Ball
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5
ball_dy = 5

# ----- SCORING -----
score_A = 0
score_B = 0
server = "A"        # A starts serving
font = pygame.font.SysFont("Arial", 32)

clock = pygame.time.Clock()

# ----- FUNCTIONS -----
def draw_everything():
    win.fill(BLACK)

    # Draw paddles
    pygame.draw.rect(win, WHITE, (20, paddleA_y, paddle_width, paddle_height))
    pygame.draw.rect(win, WHITE, (WIDTH - 20 - paddle_width, paddleB_y, paddle_width, paddle_height))

    # Draw ball
    pygame.draw.rect(win, GREEN, (ball_x, ball_y, ball_size, ball_size))

    # Draw score & server info
    score_text = font.render(f"A: {score_A}     B: {score_B}    Server: {server}", True, WHITE)
    win.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.update()


def reset_ball(direction):
    """Reset ball to center and send it toward the side that scored."""
    global ball_x, ball_y, ball_dx, ball_dy

    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = 5 if direction == "right" else -5
    ball_dy = 5


def check_win():
    """Check if a team won."""
    global running

    if (score_A >= 11 or score_B >= 11) and abs(score_A - score_B) >= 2:
        winner = "TEAM A" if score_A > score_B else "TEAM B"
        print(f"🏆 {winner} WINS! Final Score {score_A} - {score_B}")
        pygame.quit()
        sys.exit()


# ----- MAIN GAME LOOP -----
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ----- CONTROL PADDLES -----
    keys = pygame.key.get_pressed()

    # Team A paddle (left)
    if keys[pygame.K_w] and paddleA_y > 0:
        paddleA_y -= paddle_speed
    if keys[pygame.K_s] and paddleA_y < HEIGHT - paddle_height:
        paddleA_y += paddle_speed

    # Team B paddle (right)
    if keys[pygame.K_UP] and paddleB_y > 0:
        paddleB_y -= paddle_speed
    if keys[pygame.K_DOWN] and paddleB_y < HEIGHT - paddle_height:
        paddleB_y += paddle_speed

    # ----- MOVE BALL -----
    ball_x += ball_dx
    ball_y += ball_dy

    # Bounce off top/bottom
    if ball_y <= 0 or ball_y + ball_size >= HEIGHT:
        ball_dy *= -1

    # ----- PADDLE COLLISION -----
    # Left paddle (A)
    if (20 < ball_x < 20 + paddle_width and
        paddleA_y < ball_y < paddleA_y + paddle_height):
        ball_dx = abs(ball_dx)

    # Right paddle (B)
    if (WIDTH - 20 - paddle_width < ball_x + ball_size < WIDTH - 20 and
        paddleB_y < ball_y < paddleB_y + paddle_height):
        ball_dx = -abs(ball_dx)

    # ----- SCORING LOGIC -----
    # Ball goes off left side = point/fault for B
    if ball_x <= 0:
        if server == "B":   # server scores
            score_B += 1
            reset_ball("left")
        else:               # fault → switch server
            server = "B"
            reset_ball("left")

        check_win()

    # Ball goes off right side = point/fault for A
    if ball_x + ball_size >= WIDTH:
        if server == "A":
            score_A += 1
            reset_ball("right")
        else:
            server = "A"
            reset_ball("right")

        check_win()

    # ----- DRAW EVERYTHING -----
    draw_everything()
    clock.tick(60)

pygame.quit()