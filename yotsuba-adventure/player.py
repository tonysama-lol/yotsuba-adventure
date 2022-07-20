import pygame 
from settings import *
from support import import_folder 

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,groups,obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/player_Yotsuba.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-2,-4)
	
		#graphics setup
		self.import_player_assets()
		self.status = 'right'
		self.frame_index = 0
		self.animation_speed = 0.05
	
		#move setup
		self.direction = pygame.math.Vector2()
		self.speed = 9.5
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None

		self.obstacle_sprites = obstacle_sprites

	def import_player_assets(self):
		character_path = 'graphics/player/player_'
		self.animations = {'left_idle':[],
		'right_idle':[],
		'left_walk':[],
		'right_walk':[]
		}
		
		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
		keys = pygame.key.get_pressed()

		#movement input
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			self.direction.y = -1
			if 'idle' in self.status:
				self.status = self.status.replace('_idle', '_walk')
			if 'walk' not in self.status:
				self.status += '_walk'
		elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self.direction.y = 1
			if 'idle' in self.status:
				self.status = self.status.replace('_idle', '_walk')
			if 'walk' not in self.status:
				self.status += '_walk'
		else:
			self.direction.y = 0

		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.direction.x = 1
			self.status = 'right_walk'
		elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.direction.x = -1
			self.status = 'left_walk'
		else:
			self.direction.x = 0
		
		#attack input
		if keys[pygame.K_k] and not self.attacking:
			self.attacking = True
			self.attack_time = pygame.time.get_ticks()
			print("attack")
		
	def get_status(self):
		#idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				if 'walk' in self.status:
					self.status = self.status.replace('_walk','_idle')
				else:
					self.status = self.status + '_idle'
				
		if self.attacking:
			#stop player while attacking
			#self.direction.x = 0
			#self.direction.y = 0
			#do attack
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')
			
	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def collision(self,direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom
	def cooldown(self):
		current_time = pygame.time.get_ticks()
		
		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False

	def animate(self):
		animation = self.animations[self.status]
		#loop
		self.frame_index += self.animation_speed
		if self.frame_index > len(animation):
			self.frame_index = 0
			
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def update(self):
		self.input()
		self.cooldown()
		self.get_status()
		self.animate()
		self.move(self.speed)
