import pygame
import random
import sys

# ================= ИНИЦИАЛИЗАЦИЯ =================
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 60)
GOLD = (255, 215, 0)
BLUE_DAY = (135, 206, 235)
BLUE_NIGHT = (25, 45, 75)
GREEN = (50, 180, 50)
RED = (220, 50, 50)

# Шрифты
font = pygame.font.SysFont("arial", 42, bold=True)
font_small = pygame.font.SysFont("arial", 28)
font_title = pygame.font.SysFont("arial", 52, bold=True)


# ================= КЛАССЫ =================
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.vel = 0
        self.radius = 18
        self.alive = True

    def flap(self):
        self.vel = -8.2

    def update(self):
        self.vel += 0.55
        self.y += self.vel

    def draw(self):
        color = YELLOW if self.alive else (220, 140, 0)
        pygame.draw.circle(screen, color, (self.x, int(self.y)), self.radius)
        # клюв
        pygame.draw.polygon(
            screen,
            (255, 140, 0),
            [
                (self.x + 12, int(self.y)),
                (self.x + 28, int(self.y) - 6),
                (self.x + 28, int(self.y) + 6),
            ],
        )
        # глаз
        pygame.draw.circle(screen, BLACK, (self.x + 8, int(self.y) - 6), 5)
        pygame.draw.circle(screen, WHITE, (self.x + 9, int(self.y) - 7), 2)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(140, 380)
        self.width = 70
        self.passed = False

    def update(self):
        self.x -= 3.2

    def draw(self):  # высота труб, то есть изменить размер зазора между трубами
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_y - 75))
        pygame.draw.rect(screen, GREEN, (self.x, self.gap_y + 75, self.width, HEIGHT))

    def collides_with(self, bird):
        bird_rect = pygame.Rect(
            bird.x - bird.radius, bird.y - bird.radius, bird.radius * 2, bird.radius * 2
        )
        upper = pygame.Rect(self.x, 0, self.width, self.gap_y - 75)
        lower = pygame.Rect(self.x, self.gap_y + 75, self.width, HEIGHT)
        return bird_rect.colliderect(upper) or bird_rect.colliderect(lower)


def draw_score(score):
    score_text = font.render(str(score), True, BLACK)
    outline = font.render(str(score), True, WHITE)
    for dx, dy in [
        (-2, -2),
        (-2, 2),
        (2, -2),
        (2, 2),
        (-3, 0),
        (3, 0),
        (0, -3),
        (0, 3),
    ]:
        screen.blit(outline, (WIDTH // 2 - outline.get_width() // 2 + dx, 40 + dy))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 40))


# ================= ПАУЗА =================
def draw_pause_menu():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    paused_text = font_title.render("ПАУЗА", True, WHITE)
    screen.blit(paused_text, (WIDTH // 2 - paused_text.get_width() // 2, 150))

    resume_text = font_small.render("SPACE / P / ЛКМ — Продолжить", True, WHITE)
    restart_text = font_small.render("R — Рестарт", True, GOLD)
    quit_text = font_small.render("Q / ESC — Выход", True, RED)

    screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, 280))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 330))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, 380))


# ================= ОСНОВНАЯ ФУНКЦИЯ =================
def main():
    bird = Bird()
    pipes = [Pipe(WIDTH + 100)]
    score = 0
    high_score = 0
    game_state = "start"  # start / playing / paused / gameover

    clouds = [
        {
            "x": random.randint(-200, WIDTH),
            "y": random.randint(40, 180),
            "speed": random.uniform(0.4, 1.2),
        }
        for _ in range(8)
    ]

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if game_state == "start":
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        game_state = "playing"
                        bird = Bird()
                        pipes = [Pipe(WIDTH + 100)]
                        score = 0
                elif game_state == "playing":
                    if event.key == pygame.K_SPACE:
                        bird.flap()
                    elif event.key in (pygame.K_p, pygame.K_ESCAPE):
                        game_state = "paused"
                elif game_state == "paused":
                    if event.key in (pygame.K_SPACE, pygame.K_p, pygame.K_ESCAPE):
                        game_state = "playing"
                    elif event.key == pygame.K_r:
                        game_state = "start"
                    elif event.key == pygame.K_q:
                        running = False
                elif game_state == "gameover":
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        game_state = "start"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "start":
                    game_state = "playing"
                    bird = Bird()
                    pipes = [Pipe(WIDTH + 100)]
                    score = 0
                elif game_state == "playing" and bird.alive:
                    bird.flap()
                elif game_state == "paused":
                    game_state = "playing"
                elif game_state == "gameover":
                    game_state = "start"

        # ─── ЛОГИКА ИГРЫ ───
        if game_state == "playing":
            bird.update()

            if pipes[-1].x < WIDTH - 150:  # отступ между трубами по горизонтали
                pipes.append(Pipe(WIDTH + 120))

            for p in pipes[:]:
                p.update()
                if p.x + p.width < -10:
                    pipes.remove(p)
                if not p.passed and p.x + p.width < bird.x:
                    p.passed = True
                    score += 1

                if p.collides_with(bird):
                    bird.alive = False
                    break

            if bird.y - bird.radius < 0 or bird.y + bird.radius > HEIGHT:
                bird.alive = False

            if not bird.alive:
                game_state = "gameover"
                high_score = max(high_score, score)

        # ─── ОБЛАКА ───
        if game_state != "gameover":
            for c in clouds:
                c["x"] -= c["speed"]
                if c["x"] < -120:
                    c["x"] = WIDTH + random.randint(50, 300)

        # ─── ОТРИСОВКА ───
        is_night = (score // 10) % 2 == 1
        screen.fill(BLUE_NIGHT if is_night else BLUE_DAY)

        # облака
        for c in clouds:
            pygame.draw.circle(screen, (255, 255, 255, 80), (int(c["x"]), c["y"]), 45)
            pygame.draw.circle(
                screen, (255, 255, 255, 80), (int(c["x"]) + 35, c["y"] - 15), 38
            )
            pygame.draw.circle(
                screen, (255, 255, 255, 80), (int(c["x"]) - 30, c["y"] + 10), 50
            )

        # трубы и птица
        for p in pipes:
            p.draw()
        bird.draw()

        # счёт
        draw_score(score)

        # рекорд в углу
        if high_score > 0:
            hs_text = font_small.render(f"Рекорд: {high_score}", True, GOLD)
            screen.blit(hs_text, (10, 10))

        if game_state == "start":
            title = font_small.render("Нажми SPACE или ЛКМ", True, WHITE)
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
            info = font_small.render("P = пауза", True, GOLD)
            screen.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 2 + 20))

        elif game_state == "gameover":
            if score >= 50:
                medal = "ЗОЛОТО"
                color = (255, 215, 0)
            elif score >= 25:
                medal = "СЕРЕБРО"
                color = (192, 192, 192)
            elif score >= 10:
                medal = "БРОНЗА"
                color = (205, 127, 50)
            else:
                medal = "ДЕРЕВО"
                color = (139, 69, 19)

            go = font.render("GAME OVER", True, RED)
            sc = font_small.render(f"Счёт: {score}", True, WHITE)
            hs = font_small.render(f"Рекорд: {high_score}", True, GOLD)
            md = font_small.render(medal, True, color)

            screen.blit(go, (WIDTH // 2 - go.get_width() // 2, 140))
            screen.blit(sc, (WIDTH // 2 - sc.get_width() // 2, 240))
            screen.blit(hs, (WIDTH // 2 - hs.get_width() // 2, 290))
            screen.blit(md, (WIDTH // 2 - md.get_width() // 2, 350))

            restart = font_small.render("SPACE / ЛКМ — заново", True, WHITE)
            screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 450))

        elif game_state == "paused":
            draw_pause_menu()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
