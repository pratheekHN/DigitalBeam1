import pygame
import random

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Screen dimensions
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 480
CELL_SIZE = 20

# Directions
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

class Snake:
    def __init__(self):
        self.size = 1
        self.elements = [[int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)]]
        self.direction = random.choice([LEFT, RIGHT, UP, DOWN])
        self.score = 0

    def move(self):
        head = self.elements[0].copy()
        if self.direction == LEFT:
            head[0] -= CELL_SIZE
        if self.direction == RIGHT:
            head[0] += CELL_SIZE
        if self.direction == UP:
            head[1] -= CELL_SIZE
        if self.direction == DOWN:
            head[1] += CELL_SIZE

        self.elements = [head] + self.elements[:-1]

    def grow(self):
        self.size += 1
        self.elements.append(self.elements[-1])
        self.score += 1

    def collides_with_boundaries(self):
        head = self.elements[0]
        return head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT

    def collides_with_self(self):
        return self.elements[0] in self.elements[1:]

    def draw(self, screen):
        for segment in self.elements:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

class Food:
    def __init__(self):
        self.x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE

    def consumed_by(self, snake):
        return snake.elements[0] == [self.x, self.y]

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x + CELL_SIZE // 2, self.y + CELL_SIZE // 2), CELL_SIZE // 2)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')

    snake = Snake()
    food = Food()

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        snake.move()

        if snake.collides_with_boundaries() or snake.collides_with_self():
            snake = Snake()
            food = Food()

        if food.consumed_by(snake):
            snake.grow()
            food = Food()

        screen.fill(WHITE)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.flip()
        clock.tick(10 + snake.score // 5)  # Increase speed as score increases

if __name__ == '__main__':
    main()
