class Enemy():
	def __init__(self, name, health, damage):
		self.name = name
		self.health = health
		self.damage = damage

	def is_alive(self):
		return self.health > 0

class GiantSpider(Enemy):
	def __init__(self):
		super().__init__(name='Giant Spider', health=10, damage=2)

class Ogre(Enemy):
	def __init__(self):
		super().__init__(name='Ogre', health=30, damage=15)