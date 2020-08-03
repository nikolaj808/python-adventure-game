from items import *
from world import *
import random

class Player():
	def __init__(self):
		self.inventory = [Gold(15), Rock()]
		self.health = 100
		self.location_x, self.location_y = load_tiles()
		self.victory = False

	def is_alive(self):
		return self.health > 0

	def print_inventory(self):
		for item in self.inventory:
			print(item)

	def move(self, dx, dy):
		self.location_x += dx
		self.location_y += dy
		print(tile_exists(self.location_x, self.location_y).intro_text())

	def move_north(self):
		self.move(dx=0, dy=-1)

	def move_south(self):
		self.move(dx=0, dy=1)

	def move_east(self):
		self.move(dx=1, dy=0)

	def move_west(self):
		self.move(dx=-1, dy=0)

	def attack(self, enemy):
		best_weapon = None
		max_dmg = 0
		for i in self.inventory:
			if isinstance(i, Weapon()):
				if i.damage > max_dmg:
					max_dmg = i.damage
					best_weapon = i

		print('You use your {} against {}!'.format(best_weapon.name, enemy.name))
		enemy.health -= best_weapon.damage
		if not enemy.is_alive():
			print('You killed {}!'.format(enemy.name))
		else:
			print('{} has {} health left'.format(enemy.name, enemy.health))

	def do_action(self, action, **kwargs):
		action_method = getattr(self, action.method.__name__)
		if action_method:
			action_method(**kwargs)

	def flee(self, tile):
		available_moves = tile.adjacent_moves()
		r = random.randint(0, len(available_moves) - 1)
		self.do_action(available_moves[r])

	