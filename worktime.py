
from button import Button
import sys
import pygame
import winsound


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
					pass
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


def main():
	breaktime=0
	breaktime=workperiod()
	#meditationscreen(breaktime)


if __name__ == '__main__':
    main()
