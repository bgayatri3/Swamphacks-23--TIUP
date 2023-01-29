import pygame
import os
import random
from button import Button
import sys
import pygame
import winsound


pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Gator", "GatorRun1.png")),
          pygame.image.load(os.path.join("Assets/Gator", "GatorRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Gator", "GatorJump.png"))

SMALL_Plant = [pygame.image.load(os.path.join("Assets/Plant", "SmallPlant1.png")),
                pygame.image.load(os.path.join("Assets/Plant", "SmallPlant2.png")),
    pygame.image.load(os.path.join("Assets/Plant", "SmallPlant3.png"))]
LARGE_Plant = [pygame.image.load(os.path.join("Assets/Plant", "LargePlant1.png")),
                pygame.image.load(os.path.join("Assets/Plant", "LargePlant2.png")),
                pygame.image.load(os.path.join("Assets/Plant", "LargePlant3.png"))]

Bee = [pygame.image.load(os.path.join("Assets/Bee", "Bee1.png")),
        pygame.image.load(os.path.join("Assets/Bee", "Bee2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Swamp.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 10

    def __init__(self):
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallPlant(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargePlant(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bee(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1


def startgame():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallPlant(SMALL_Plant))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargePlant(LARGE_Plant))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bee(Bee))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Click the Flying Gator then Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0],(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                startgame()


menu(death_count=0)

def workperiod():
	# defines size of the screen
	pygame.init()
	WIDTH, HEIGHT = 900, 600
	SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

	CLOCK = pygame.time.Clock() #clock

	# background and main button
	BACKDROP = pygame.image.load("backdrop.png")
	WHITE_BUTTON = pygame.image.load("button.png")


	#configuring look of time
	FONT = pygame.font.Font("ArialRoundedMTBold.ttf", 100)
	FONT2=pygame.font.Font("ArialRoundedMTBold.ttf", 80)
	FONT3=pygame.font.Font("ArialRoundedMTBold.ttf", 30)
	work_text = FONT.render("20:00", True, "white")
	work_text_rect = work_text.get_rect(center=(WIDTH/3+10, HEIGHT/2-25))

	break_text = FONT.render("50:00", True, "white")
	break_text_rect = break_text.get_rect(center=(2*WIDTH/3+10, HEIGHT/2-25))

	START_PAUSE_BUTTON = Button(WHITE_BUTTON, (WIDTH/2, HEIGHT/2+100), 170, 60, "START",
						pygame.font.Font("ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")

	END_BUTTON = Button(None, (WIDTH/2, HEIGHT/2+140), 120, 30, "Start break",
						pygame.font.Font("ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")

	title_surface= FONT2.render("Work Period", 0, "black")
	title_rectangle= title_surface.get_rect(center= (WIDTH // 2, HEIGHT // 2-225))

	work_surface= FONT3.render("Work Time", 0, "black")
	work_rectangle= title_surface.get_rect(center= (WIDTH // 2 +30, HEIGHT // 2-60))

	break_surface= FONT3.render("Break Time", 0, "black")
	break_rectangle= title_surface.get_rect(center= (3*WIDTH //4 +90, HEIGHT // 2-60))

	current_seconds = 0 #POMODORO_LENGTH
	current_break_seconds=0
	break_seconds=0
	break_minutes=0

	pygame.time.set_timer(pygame.USEREVENT, 1000) #starts keeping track of time
	started = False

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if START_PAUSE_BUTTON.check_for_input(pygame.mouse.get_pos()):
					if started:
						started = False
						current_break_seconds = -1
					else:
						started = True

				if END_BUTTON.check_for_input(pygame.mouse.get_pos()):
					started = False
					current_break_seconds=-1
					continuescreen(current_seconds*0.2)
					return

				if started:
					START_PAUSE_BUTTON.text_input = "PAUSE"
					START_PAUSE_BUTTON.text = pygame.font.Font("ArialRoundedMTBold.ttf", 20).render(
											START_PAUSE_BUTTON.text_input, True, START_PAUSE_BUTTON.base_color)
				else:
					START_PAUSE_BUTTON.text_input = "START"
					START_PAUSE_BUTTON.text = pygame.font.Font("ArialRoundedMTBold.ttf", 20).render(
											START_PAUSE_BUTTON.text_input, True, START_PAUSE_BUTTON.base_color)
			if event.type == pygame.USEREVENT and started:
				current_seconds +=1 # -= 1

		SCREEN.fill("#F0A996")
		SCREEN.blit(BACKDROP, BACKDROP.get_rect(center=(WIDTH/2, HEIGHT/2)))

		START_PAUSE_BUTTON.update(SCREEN)
		START_PAUSE_BUTTON.change_color(pygame.mouse.get_pos())

		END_BUTTON.update(SCREEN)
		END_BUTTON.change_color(pygame.mouse.get_pos())

		if current_seconds >= 0:
			display_seconds = current_seconds % 60
			display_minutes = int(current_seconds / 60) % 60
		work_text = FONT.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")
		SCREEN.blit(work_text, work_text_rect)

		if current_break_seconds == -1:
			current_break_seconds = int(current_seconds * 0.2)
			break_seconds = current_break_seconds % 60
			break_minutes = int(current_break_seconds / 60) % 60

		break_text = FONT.render(f"{break_minutes:02}:{break_seconds:02}", True, "white")
		SCREEN.blit(break_text, break_text_rect)

		SCREEN.blit(title_surface, title_rectangle)
		SCREEN.blit(work_surface, work_rectangle)
		SCREEN.blit(break_surface, break_rectangle)

		pygame.display.update()

def continuescreen(breaktime):
	# defines size of the screen
	pygame.init()
	WIDTH, HEIGHT = 900, 600
	SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

	CLOCK = pygame.time.Clock()  # clock

	# background and main button
	BACKDROP = pygame.image.load("backdrop3.png")
	WHITE_BUTTON = pygame.image.load("button.png")

	# configuring fonts
	FONT = pygame.font.Font("ArialRoundedMTBold.ttf", 90)
	FONT2 = pygame.font.Font("ArialRoundedMTBold.ttf", 80)


	RELAX_BUTTON = Button(WHITE_BUTTON, (WIDTH / 3, HEIGHT / 2), 170, 60, "RELAX",
								pygame.font.Font("ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")

	GAME_BUTTON = Button(WHITE_BUTTON, (2*WIDTH / 3, HEIGHT / 2), 170, 60, "GAME",
								pygame.font.Font("ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")

	work_surface = FONT2.render("Choose your break", 0, "black")
	work_rectangle = work_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 225))

	current_seconds = breaktime

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if GAME_BUTTON.check_for_input(pygame.mouse.get_pos()):
					startgame()
					print("game")

				if RELAX_BUTTON.check_for_input(pygame.mouse.get_pos()):
					meditationscreen(breaktime)


		SCREEN.fill("#A6B586")
		SCREEN.blit(BACKDROP, BACKDROP.get_rect(center=(WIDTH / 2, HEIGHT / 2)))

		GAME_BUTTON.update(SCREEN)
		GAME_BUTTON.change_color(pygame.mouse.get_pos())

		RELAX_BUTTON.update(SCREEN)
		RELAX_BUTTON.change_color(pygame.mouse.get_pos())


		SCREEN.blit(work_surface, work_rectangle)

		pygame.display.update()

def meditationscreen(breaktime):
	# defines size of the screen
	pygame.init()
	WIDTH, HEIGHT = 900, 600
	SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

	CLOCK = pygame.time.Clock()  # clock

	# background and main button
	BACKDROP = pygame.image.load("backdrop2.png")
	WHITE_BUTTON = pygame.image.load("button.png")

	# configuring look of time
	FONT = pygame.font.Font("ArialRoundedMTBold.ttf", 90)
	FONT2 = pygame.font.Font("ArialRoundedMTBold.ttf", 80)

	work_text = FONT.render("20:00", True, "white")
	work_text_rect = work_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 25))

	START_PAUSE_BUTTON = Button(WHITE_BUTTON, (WIDTH / 2, HEIGHT / 2 + 100), 170, 60, "START",
								pygame.font.Font("ArialRoundedMTBold.ttf", 20), "#c97676", "#9ab034")

	END_BUTTON = Button(None, (WIDTH / 2, HEIGHT / 2 + 140), 120, 30, "Back to Work",
						pygame.font.Font("ArialRoundedMTBold.ttf", 20), "#FFFFFF", "#9ab034")



	work_surface = FONT.render("Meditation Time", 0, "black")
	work_rectangle = work_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 225))



	current_seconds = breaktime
	break_seconds = 0
	break_minutes = 0

	pygame.time.set_timer(pygame.USEREVENT, 1000)  # starts keeping track of time
	started = False

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if START_PAUSE_BUTTON.check_for_input(pygame.mouse.get_pos()):
					if started:
						started = False
						current_break_seconds = -1
					else:
						started = True

				if END_BUTTON.check_for_input(pygame.mouse.get_pos()):
					started = False
					workperiod()

				if started:
					START_PAUSE_BUTTON.text_input = "PAUSE"
					START_PAUSE_BUTTON.text = pygame.font.Font("ArialRoundedMTBold.ttf", 20).render(
						START_PAUSE_BUTTON.text_input, True, START_PAUSE_BUTTON.base_color)
				else:
					START_PAUSE_BUTTON.text_input = "START"
					START_PAUSE_BUTTON.text = pygame.font.Font("ArialRoundedMTBold.ttf", 20).render(
						START_PAUSE_BUTTON.text_input, True, START_PAUSE_BUTTON.base_color)
			if event.type == pygame.USEREVENT and started:
				current_seconds -= 1

		SCREEN.fill("#bd9C74")
		SCREEN.blit(BACKDROP, BACKDROP.get_rect(center=(WIDTH / 2, HEIGHT / 2)))

		START_PAUSE_BUTTON.update(SCREEN)
		START_PAUSE_BUTTON.change_color(pygame.mouse.get_pos())

		END_BUTTON.update(SCREEN)
		END_BUTTON.change_color(pygame.mouse.get_pos())

		if current_seconds >= 0:
			display_seconds = int(current_seconds) % 60
			display_minutes = int(current_seconds / 60) % 60

		if current_seconds+1 <=0:
			frequency = 1000  # Set Frequency To 2500 Hertz
			duration = 1000  # Set Duration To 1000 ms == 1 second
			winsound.Beep(frequency, duration)

		work_text = FONT.render(f"{display_minutes:02}:{display_seconds:02}", True, "white")
		SCREEN.blit(work_text, work_text_rect)
		SCREEN.blit(work_surface, work_rectangle)


		pygame.display.update()

def gamescreen(breaktime):
	startgame()

def main():
	workperiod()

if __name__ == '__main__':
    main()

