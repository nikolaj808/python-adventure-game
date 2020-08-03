world_ = {}
starting_position = (0, 0)

def load_tiles():
	with open('resources/map.txt', 'r') as f:
		rows = f.readlines()
	x_max = len(rows[0].split('\t'))
	for y in range(len(rows)):
		cols = rows[y].split('\t')
		for x in range(x_max):
			tile_name = cols[x].replace('\n', '')
			if tile_name == 'StartingRoom':
				global starting_position
				starting_position = (x, y)
			world_[(x, y)] = None if tile_name == '' else getattr(__import__('tiles'), tile_name)(x, y)
	return starting_position

def tile_exists(x, y):
	return world_.get((x, y))