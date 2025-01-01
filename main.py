import pygame as py

py.init()
py.font.init()

import assets.initialization as init

import assets.config as config
import assets.sprits as sprits
from assets.classes.class_button import *

def main_loop():
	clock = py.time.Clock()

	while config.running:
		#проверка на соответствие размеров дисплея
		window_width, window_height = py.display.get_surface().get_size()
		if window_width != config.window_size[0] or window_height != config.window_size[1]:
			difference_width = config.window_size[0] - window_width
			difference_height = config.window_size[1] - window_height
			config.zero_coordinate[0] -= difference_width // 2
			config.zero_coordinate[1] -= difference_height // 2

			config.window_size = [window_width, window_height]
			init.scripts.buttons_init()
			init.player.start_position = [config.window_size[0]//2, config.window_size[1]//2]
			init.player.rect.center = init.player.start_position
			init.board.map.map_translation()

		#в зависимости от состояния игры, запускает новый цикл
		if config.is_console_open:
			init.console.opened()
		else:
			if config.state_of_the_game["main menu"]:
				main_menu_loop()
			elif config.state_of_the_game["statistics"]:
				statistics_loop()
			elif config.state_of_the_game["settings"]:
				settings_loop()
			elif config.state_of_the_game["game mode selection"]:
				game_mode_selection_loop()
			elif config.state_of_the_game["editor"]:
				editor_loop()
			elif config.state_of_the_game["level selection"]:
				level_selection_loop()
			elif config.state_of_the_game["menu"]:
				menu_loop()
			elif config.state_of_the_game["game"]:
				if config.moving["cut scene"]:
					dialogue_loop()
				else:
					game_loop()

		#отрисовка текста на экране
		for text in init.texts:
			text.draw()

		py.display.update()
		clock.tick(config.FPS)
		#print("FPS: ", clock.get_fps())

	for chit in init.settings["chits"]:
		init.settings["chits"][chit] = False
	init.scripts.save_settings()
	init.save["statistics"]["time in game"] += py.time.get_ticks() - config.last_time_update
	init.scripts.save_save()

def main_menu_loop(): #цикл, когда игрок находиться в главном меню
	init.screen.fill(config.COLOR_GREY)

	clicked = False

	for event in py.event.get():
		if event.type == py.QUIT:
			config.running = False
		if event.type == py.MOUSEBUTTONDOWN:
			if event.button == 1:
				clicked = True
		if event.type == py.KEYDOWN:
			if event.key == py.K_CARET:
				if config.is_console_open:
					config.is_console_open = False
				else:
					config.is_console_open = True
	
	for button in init.buttons_on_main_menu:
		button.draw()
		if clicked:
			if button.rect.collidepoint(py.mouse.get_pos()):
				button.click()

def statistics_loop(): #цикл для показа статистики игрока
	init.screen.fill(config.COLOR_GREY)

	clicked = False

	for event in py.event.get():
		if event.type == py.QUIT:
			config.running = False
		if event.type == py.MOUSEBUTTONDOWN:
			if event.button == 1:
				clicked = True
	
	for button in init.buttons_statistics:
		button.draw()
		if clicked:
			if button.rect.collidepoint(py.mouse.get_pos()):
				button.click()

def settings_loop(): #цикл, когда игрок находиться в настройках
	init.screen.fill(config.COLOR_GREY)

	clicked = False

	for event in py.event.get():
		if event.type == py.QUIT:
			config.running = False
		if event.type == py.MOUSEBUTTONDOWN:
			if event.button == 1:
				clicked = True
	
	for button in init.buttons_settings:
		button.draw()
		if clicked:
			if button.rect.collidepoint(py.mouse.get_pos()):
				button.click()

def game_mode_selection_loop(): #цикл, когда игрок выбирает режим игры
	init.screen.fill(config.COLOR_GREY)

	clicked = False

	for event in py.event.get():
		if event.type == py.QUIT:
			config.running = False
		elif event.type == py.MOUSEBUTTONDOWN:
			if event.button == 1:
				clicked = True
		elif event.type == py.KEYDOWN:
			if event.key == py.K_CARET:
				if config.is_console_open:
					config.is_console_open = False
				else:
					config.is_console_open = True
	
	for button in init.buttons_game_mode_selection:
		button.draw()
		if clicked:
			if button.rect.collidepoint(py.mouse.get_pos()):
				button.click()

def editor_loop(): #редактор карт
	init.screen.fill(config.COLOR_GREY)

	clicked = False

	init.obstacles.update()
	init.obstacles.draw(init.screen)

	init.markers.update()
	init.markers.draw(init.screen)

	init.enemies.update()
	init.enemies.draw(init.screen)

	init.enemies_tied_to_the_script.update()
	init.enemies_tied_to_the_script.draw(init.screen)
	
	init.allies.update()
	init.allies.draw(init.screen)

	events = py.event.get()

	for event in events:
		if event.type == py.QUIT:
			config.running = False
		elif event.type == py.MOUSEBUTTONDOWN:
			if event.button == 1:
				clicked = True
			elif event.button == 4: #прокрутка вверх
				if init.buttons_level_selection[0].position[1] < 0:
					init.scripts.move_group(init.buttons_editor, 0, config.CELL_SIZE//4)
			elif event.button == 5: #прокрутка вниз
				last_button = init.buttons_level_selection[-1]
				if last_button.position[1]+last_button.heidht > config.window_size[1]:
					init.scripts.move_group(init.buttons_editor, 0, -config.CELL_SIZE//4)
		elif event.type == py.KEYDOWN:
			if event.key == py.K_ESCAPE:
				if config.state_of_editor["main location"]:
					config.state_of_the_game["editor"] = False
					config.state_of_the_game["main menu"] = True
					init.editor.close()
				else:
					init.editor.back_to_main_location()
				return
	
	for button in init.buttons_editor:
		button.draw()
		if clicked:
			if button.rect.collidepoint(py.mouse.get_pos()):
				button.click()
	
	init.editor.update_editor(events)

def level_selection_loop(): #цикл, когда игрок выбирает уровень
	init.screen.fill(config.COLOR_GREY)

	clicked = False

	for event in py.event.get():
		if event.type == py.QUIT:
			config.running = False
		if event.type == py.MOUSEBUTTONDOWN:
			if event.button == 1: #ЛКМ
				clicked = True
			elif event.button == 4: #прокрутка вверх
				if init.buttons_level_selection[0].position[1] < 0:
					init.scripts.move_group(init.buttons_level_selection, 0, config.CELL_SIZE//4)
			elif event.button == 5: #прокрутка вниз
				last_button = init.buttons_level_selection[-1]
				if last_button.position[1]+last_button.heidht > config.window_size[1]:
					init.scripts.move_group(init.buttons_level_selection, 0, -config.CELL_SIZE//4)
			elif event.key == py.K_CARET:
				if config.is_console_open:
					config.is_console_open = False
				else:
					config.is_console_open = True
	
	for button in init.buttons_level_selection:
		button.draw()
		if clicked:
			if button.rect.collidepoint(py.mouse.get_pos()):
				button.click()

def menu_loop(): #цикл, когда игрок во время игры открыл меню
	clicked = False

	for event in py.event.get():
		if event.type == py.QUIT:
			config.running = False
		if event.type == py.MOUSEBUTTONDOWN:
			if event.button == 1:
				clicked = True
		elif event.type == py.KEYDOWN:
			#выход из меню
			if event.key == py.K_ESCAPE and not init.player.dead:
				config.state_of_the_game["game"] = True
				config.state_of_the_game["menu"] = False
				return
			elif event.key == py.K_CARET:
				if config.is_console_open:
					config.is_console_open = False
				else:
					config.is_console_open = True
		
	for button in init.buttons_menu:
		if not (button.contents == "CONTINIU" and init.player.dead) and not (button.contents == "RESTART" and not init.player.dead): #кнопка продолжить должна показываться только если игрок жив, а кнопка рестарт только если игрок мертв
			button.draw()
			if clicked:
				if button.rect.collidepoint(py.mouse.get_pos()):
					button.click()

def dialogue_loop(): #цикл, когда идёт диалог
	init.screen.fill(config.COLOR_DIRT)

	init.obstacles.update()
	init.obstacles.draw(init.screen)

	init.player_group.update()
	init.player_group.draw(init.screen)

	init.enemies.update()
	init.enemies.draw(init.screen)

	init.enemies_tied_to_the_script.update()
	init.enemies_tied_to_the_script.draw(init.screen)

	init.allies.update()
	init.allies.draw(init.screen)

	init.bullets.update()
	init.bullets.draw(init.screen)

	init.gui.update()
	init.gui.draw()

	init.dialogue
	init.dialogue.draw()

	for event in py.event.get():
		#Нажатие
		if event.type == py.QUIT:
			config.running = False

		elif event.type == py.KEYDOWN:
			#выход в меню
			if event.key == py.K_ESCAPE:
				config.state_of_the_game["game"] = False
				config.state_of_the_game["menu"] = True
				return
			elif event.key == py.K_SPACE:
				init.dialogue.next()
			elif event.key == py.K_LEFT:
				init.dialogue.last()
			elif event.key == py.K_CARET:
				if config.is_console_open:
					config.is_console_open = False
				else:
					config.is_console_open = True
	
def game_loop(): #игровой цикл
	init.screen.fill(config.COLOR_DIRT)

	init.obstacles.update()
	init.obstacles.draw(init.screen)

	init.items.update()
	init.items.draw(init.screen)

	init.player_group.update()
	init.player_group.draw(init.screen)

	init.enemies.update()
	init.enemies.draw(init.screen)

	init.enemies_tied_to_the_script.update()
	init.enemies_tied_to_the_script.draw(init.screen)

	init.allies.update()
	init.allies.draw(init.screen)

	init.bullets.update()
	init.bullets.draw(init.screen)

	init.gui.update()
	init.gui.draw()

	for event in py.event.get():
		#Нажатие
		if event.type == py.QUIT:
			config.running = False

		elif event.type == py.KEYDOWN:
			#выход в меню
			if event.key == py.K_ESCAPE:
				config.state_of_the_game["game"] = False
				config.state_of_the_game["menu"] = True
				return
			elif event.key == py.K_CARET:
				if config.is_console_open:
					config.is_console_open = False
				else:
					config.is_console_open = True

			#отслеживание начала движения
			check_movement(event, True)
			
			#активности игрока
			if event.key == py.K_g:
				init.player.grenade()
			if event.key == py.K_e:
				init.scripts.player_action()
			if event.key == py.K_r:
				init.player.reload()
			if event.key in [py.K_LSHIFT, py.K_RSHIFT]:
				config.moving["run"] = True
			if event.key == py.K_1:
				init.player.active_weapon = init.player.main_weapon
				init.player.load_animations()
				print(init.player.active_weapon)
			elif event.key == py.K_2:
				init.player.active_weapon = init.player.second_weapon
				init.player.load_animations()
				print(init.player.active_weapon)
			if event.key == py.K_c and init.player.active_weapon.name == "Plasmagun":
				init.player.change_weapon_mode()
		
		elif event.type == py.MOUSEBUTTONDOWN:
			if event.button == 1: #ЛКМ
				if config.moving["taking aim"]:
					init.player.shoot()
				else:
					init.player.melee_atack()
				config.moving["fire"] = True
			if event.button == 3: #ПКМ
				config.moving["taking aim"] = True
			
		#отжатие
		elif event.type == py.KEYUP:
			if event.type == py.KEYUP:
				#отслеживание прекращения движения
				check_movement(event, False)

				#активности игрока
				if event.key in [py.K_LSHIFT, py.K_RSHIFT]:
					config.moving["run"] = False

		elif event.type == py.MOUSEBUTTONUP:
			if event.button == 1: #ЛКМ
				config.moving["fire"] = False
			if event.button == 3: #ПКМ
				config.moving["taking aim"] = False
	
	init.board.update_board()

	if config.has_tracked_enemys:
		init.scripts.tied_to_the_script_handler()
	init.scripts.player_tracking()

def check_movement(event: py.event, value: bool):
	'''
	проверяет нажатие на кнопки движения и присваевает соответствующие value в случае истины в списке moving
	@event ивент; event.key от pygame
	'''
	if event.key == py.K_w:
		config.moving["forward"] = value
	if event.key == py.K_s:
		config.moving["back"] = value
	if event.key == py.K_a:
		config.moving["left"] = value
	if event.key == py.K_d:
		config.moving["right"] = value

def start_the_game():
	init.scripts.buttons_init()

	main_loop()

start_the_game()