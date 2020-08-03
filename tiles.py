from items import *
from enemies import *
from actions import *
from world import *
import random

class MapTile:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def intro_text(self):
		raise NotImplementedError()

	def modify_player(self, player):
		raise NotImplementedError()

	def adjacent_moves(self):
		moves = []
		if tile_exists(self.x + 1, self.y):
			moves.append(MoveEast())
		if tile_exists(self.x - 1, self.y):
			moves.append(MoveWest())
		if tile_exists(self.x, self.y - 1):
			moves.append(MoveNorth())
		if tile_exists(self.x, self.y + 1):
			moves.append(MoveSouth())
		return moves

	def available_actions(self):
		'''Returns all of the available actions in this room.'''
		moves = self.adjacent_moves()
		moves.append(ViewInventory())
		return moves

class StartingRoom(MapTile):
	def intro_text(self):
		return '''
		You find yourself in a cave with a flickering torch on the wall.
		You can make out four paths, each equally as dark and foreboding.
		'''

	def modify_player(self, player):
		# No action
		pass

class LootRoom(MapTile):
	def __init__(self, x, y, item):
		self.item = item
		super().__init__(x, y)

	def add_loot(self, player):
		player.inventory.append(self.item)

	def modify_player(self, player):
		self.add_loot(player)

class EnemyRoom(MapTile):
	def __init__(self, x, y, enemy):
		self.enemy = enemy
		super().__init__(x, y)

	def modify_player(self, player):
		if self.enemy.is_alive():
			player.health = player.health - self.enemy.damage
			print('{} does {} damage. You have {} health remaining.'.format(self.enemy.name, self.enemy.damage, player.health))

	def available_actions(self):
		if self.enemy.is_alive():
			return [Flee(tile=self), Attack(enemy=self.enemy)]

class EmptyCavePath(MapTile):
	def intro_text(self):
		return '''
		Another unremarkable part of the cave. You must forge onwards.
		'''

	def modify_player(self, player):
		# No action
		pass

class GiantSpiderRoom(EnemyRoom):
	def __init__(self, x, y):
		super().__init__(x, y, GiantSpider())

	def intro_text(self):
		if self.enemy.is_alive():
			return '''
			A giant spider jumps down from its web in front of you!
			'''
		else:
			return '''
			The corpse of a dead spider rots on the ground.
			'''

class FindDaggerRoom(LootRoom):
	def __init__(self, x, y):
		super().__init__(x, y, Dagger())

	def intro_text(self):
		return '''
		You notice something shiny in the corner.
		It's a dagger! You pick it up.
		'''

class OgreRoom(EnemyRoom):
	def __init__(self, x, y):
		super().__init__(x, y, Ogre())

	def intro_text(self):
		if self.enemy.is_alive():
			return '''
			You step into the room and notice a big ogre. It notices you too...
			'''
		else:
			return '''
			The bloody corpse of a big ogre is slowly rotting on the ground.
			'''

class GoldRoom(LootRoom):
	def __init__(self, x, y):
		self.gold = random.choice([10, 25, 50])
		self.looted = False
		super().__init__(x, y, Gold(self.gold))

	def intro_text(self):
		if not self.looted:
			self.looted = True
			return '''
			You walk into the room and notice a small pile of gold.
			You pick up {} gold.
			'''.format(self.gold)
		else:
			return '''
			All the gold in this room has been looted. Now it is just an empty room
			'''

class LeaveCaveRoom(MapTile):
	def intro_text(self):
		return '''
		You see a bright light in the distance...
		it grows as you get closer! It's sunlight!

		Victory is yours!
		'''

	def modify_player(self, player):
		player.victory = True