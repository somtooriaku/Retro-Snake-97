import pygame, sys, random
from pygame.math import Vector2

# game Setup
pygame.init()

title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)
level_font = pygame.font.Font(None, 40)
# define attritubes
GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

# create the grid cells
cellSize = 30
numOfCells = 25

OFFSET = 75


class Food:
    def __init__(self, snakeBody):
        self.position = self.generate_random_pos(snakeBody)

    
    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cellSize, OFFSET + self.position.y * cellSize, cellSize, cellSize)
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, numOfCells - 1)
        y = random.randint(0, numOfCells - 1)
        return Vector2(x, y)
    
    def generate_random_pos(self, snakeBody):

        position = self.generate_random_cell()

        while position in snakeBody:
            position = self.generate_random_cell()
        return position

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1,0)
        self.addSegment = False
        self.eatSound = pygame.mixer.Sound("Sounds/eat.mp3")
        self.wallSound = pygame.mixer.Sound("Sounds/wall.mp3")

    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * cellSize, OFFSET + segment.y * cellSize, cellSize, cellSize)
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)
    
    def update(self):
        # remove last vector and add a vector in the direction
        self.body.insert(0, self.body[0] + self.direction)
        if self.addSegment == True:
            self.addSegment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5,9), Vector2(4,9)]
        self.direction = Vector2(1,0)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
        self.level = 1

    def draw(self):
        self.food.draw()
        self.snake.draw()

    def update(self):
        if self.score > 900 and self.score < 1900:
            pygame.time.set_timer(SNAKE_UPDATE, 150)
        if self.score > 1900 and self.score < 2900:
            pygame.time.set_timer(SNAKE_UPDATE, 100)
        if self.score > 2400 and self.score < 3900:
            pygame.time.set_timer(SNAKE_UPDATE, 80)
        if self.score > 3400 and self.score < 4900:
            pygame.time.set_timer(SNAKE_UPDATE, 60)
        if self.score > 4400 and self.score < 5900:
            pygame.time.set_timer(SNAKE_UPDATE, 30)
        if self.state == "RUNNING":
            self.level = 1 + (self.score // 1000)
            self.snake.update()
            self.checkIfSnakeEatsFood()
            self.checkCollisions()
            self.checkCollisionWithSnake()

    def checkIfSnakeEatsFood(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.addSegment = True
            self.score += 100
            self.snake.eatSound.play()
    
    def checkCollisions(self):
        if self.snake.body[0].x == numOfCells or self.snake.body[0].x == -1:
            self.gameOver()
        if self.snake.body[0].y == numOfCells or self.snake.body[0].y == -1:
            self.gameOver()

    def gameOver(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0
        self.snake.wallSound.play()
        pygame.time.set_timer(SNAKE_UPDATE, 200)
        

    def checkCollisionWithSnake(self):
        headless_body = self.snake.body[1: ]
        if self.snake.body[0] in headless_body:
            self.gameOver()

            

# display 
screen = pygame.display.set_mode((2 * OFFSET + cellSize * numOfCells, 2 * OFFSET + cellSize * numOfCells))

pygame.display.set_caption("Retro Snake")

# clock object for tracking framerate
clock = pygame.time.Clock()

game = Game()
food_surface = pygame.image.load("Graphics/food.png")

SNAKE_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SNAKE_UPDATE, 200)


while True:
    # event are the changes since the last loop that pygame ran.
    for event in pygame.event.get():
        # one of the types of the event can be a qit command
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"

            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)
        
        

    

    screen.fill(GREEN)
    pygame.draw.rect(screen, DARK_GREEN, (OFFSET-5, OFFSET-5, cellSize*numOfCells+10, cellSize*numOfCells+10), 5)
    game.draw()
    title_surface = title_font.render("Snake '97: retro phone classic", True, DARK_GREEN)
    score_surface = score_font.render(str(game.score), True, DARK_GREEN)
    level_surface = level_font.render("Level: " + str(game.level), True, DARK_GREEN)
    screen.blit(title_surface, (OFFSET-5, 20))
    screen.blit(score_surface, (OFFSET-5, OFFSET + cellSize * numOfCells + 10))
    screen.blit(level_surface, (cellSize * numOfCells + 10, OFFSET + cellSize * numOfCells + 10))

    pygame.display.update()
    clock.tick(60)
    

        