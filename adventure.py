from world import *
from player import Player
import os

def play():
	player = Player()
	print(starting_position)
	room = tile_exists(player.location_x, player.location_y)
	print(room.intro_text())
	while player.is_alive() and not player.victory:
		room = tile_exists(player.location_x, player.location_y)
		room.modify_player(player)
		if player.is_alive() and not player.victory:
			print('Choose an action:\n')
			available_actions = room.available_actions()
			for action in available_actions:
				print(action)
			action_input = input('Action: ')
			print('\n\n')
			for action in available_actions:
				if action_input == action.hotkey:
					player.do_action(action, **action.kwargs)
					break

play()