import pygame, sys, os
from settings import *
from level import Level

main_music = pygame.mixer.Sound("main_theme.mp3")

class Game:
	def __init__(self):
		  
		# general setup
		os.environ['SDL_VIDEO_CENTERED'] = '1' 
		pygame.init()
		pygame.mixer.init()
		fullscreen = pygame.display.Info()
		
		pygame.mixer.set_num_channels(10)
		screen_w, screen_h = fullscreen.current_w, fullscreen.current_h
		self.screen = pygame.display.set_mode((screen_w, screen_h))
		pygame.display.set_caption('Yotsuba')
		self.clock = pygame.time.Clock()

		self.level = Level()
	
	def run(self):
		pygame.mixer.Sound.play(main_music)
		while True:
			keys = pygame.key.get_pressed()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()
			self.screen.fill(green)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()
	
#pygame.quit()