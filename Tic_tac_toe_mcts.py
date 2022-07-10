import pygame
from queue import PriorityQueue
import mcts
import sys
import time

pygame.init()
mediumFont = pygame.font.SysFont("arialblack", 28)
largeFont = pygame.font.SysFont("arialblack", 40)
moveFont = pygame.font.SysFont("arialblack", 60)
font = pygame.font.SysFont("arialblack", 40)
TEXT_COL = (255, 255, 255)
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TiC TaC ToE GaMe")
List_prev_pos = []
board = []

user = None
size = None
level = 0
ok = False
game_paused = False
menu_state = "main"

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def reset(self):
		self.color = WHITE

	def make_X(self):
		self.color = ORANGE


	def make_O(self):
		self.color = TURQUOISE


	def draw(self, win):
		button = pygame.Rect(self.x, self.y, self.width, self.width)
		content = ''
		color = WHITE
		if self.color == ORANGE:
			content = 'X'
			color = RED
		elif self.color == TURQUOISE:
			content = 'O'
			color = BLUE
		button_content = mediumFont.render(content, True, color)
		button_rect = button_content.get_rect()
		button_rect.center = button.center
		pygame.draw.rect(win, WHITE, button)
		win.blit(button_content, button_rect)
		#pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


	def __lt__(self, other):
		return False


#####################UI######################
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

################XO####################
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return col, row

def is_exist(item, List):
	for i in List:
		if(item == i):
			return True
	return False
def is_exist_point(item, List):
	for i in List:
		if(i[0] == item[0] and i[1] == item[1]):
			return True
	return False
def reset(width,ROWS,grid):
	grid.clear()
	List_prev_pos.clear()
	grid = make_grid(ROWS, width)
	List_prev_pos.clear()
	board.clear()
	for i in range(ROWS*ROWS):
		board.append(' ')
	return grid
def is_winner(board, size):
	if size == 3:
		winner = mcts.check_win_3x3(board)
	elif size == 5:
		winner = mcts.check_win_5x5(board)
	elif size == 7:
		winner = mcts.check_win_7x7(board)
	if (winner in ('X', 'O')):
		print("We have winner:",winner)
		return True, winner
		
	elif (is_exist(' ', board) == False):
		print("Draw")
		return True, 'draw'
	
	return False, ' '


def draw_text(win, text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  win.blit(img, (x, y))

def draw_button(win,content, left, top, width, height, color):
	button = pygame.Rect(left, top, width , height)
	button_content = mediumFont.render(content, True, color)
	button_rect = button_content.get_rect()
	button_rect.center = button.center
	pygame.draw.rect(win, WHITE, button)
	win.blit(button_content, button_rect)
	return button
###################MAIN##################
def main(win, width):
	global user
	global size
	global level
	global ok
	run = True
	while run:
		for event in pygame.event.get():	
			if event.type == pygame.QUIT:
				sys.exit()

		win.fill(ORANGE)

		# Let user choose a player.
		if user is None:
			draw_text(win, "PLAY TIC-TAC-TOE", font, TEXT_COL, width / 4, 50 )
			
			draw_text(win, "CHOOSE PLAYER", font, TEXT_COL, width / 4, 200 )
			# Draw buttons
			playXButton = draw_button(win,"Play as X", (width / 8), (width / 2), width / 4, 50, BLACK)
			playOButton = draw_button(win,"Play as O",5 * (width / 8), (width / 2), width / 4, 50, BLACK)
			

			#Get user
			click, _, _ = pygame.mouse.get_pressed()
			if click == 1:
				mouse = pygame.mouse.get_pos()
				if playXButton.collidepoint(mouse):
					time.sleep(0.2)
					user = "X"
				elif playOButton.collidepoint(mouse):
					time.sleep(0.2)
					user = "O"
		
		
		# Let user choose size of board.
		elif size is None:
			#draw
			draw_text(win, "PLAY TIC-TAC-TOE", font, TEXT_COL, width / 4, 50 )
			draw_text(win, "CHOOSE SIZE", font, TEXT_COL, width / 4 + 30, 150 )
			size3 = draw_button(win,"BOARD 3X3 ",3 * (width / 8), 2.5 * (width / 8), width / 4, 50, BLACK)
			size5 = draw_button(win,"BOARD 5x5 ",3 * (width / 8), 3.5 * (width / 8), width / 4, 50, BLACK)
			size7 = draw_button(win,"BOARD 7x7 ",3 * (width / 8), 4.5 * (width / 8), width / 4, 50, BLACK)
			#get size
			click, _, _ = pygame.mouse.get_pressed()
			if click == 1:
				mouse = pygame.mouse.get_pos()
				if size3.collidepoint(mouse):
					time.sleep(0.2)
					size = 3
				elif size5.collidepoint(mouse):
					time.sleep(0.2)
					size = 5
				elif size7.collidepoint(mouse):
					time.sleep(0.2)
					size = 7
		elif ok == False:
			draw_text(win, "PLAY TIC-TAC-TOE", font, TEXT_COL, width / 4, 50 )
			
			draw_text(win, "CHOOSE LEVEL", font, TEXT_COL, width / 4 + 20, 200 )
			# Draw buttons
			levelButton = draw_button(win,"LEVEL",3 * (width / 8), (width / 2), width / 4, 50, BLACK)
			okButton = draw_button(win,"OK",3 * (width / 8), 1.5 * (width / 2), width / 4, 50, BLACK)
			draw_text(win, str(level), font, TEXT_COL, width / 2 - 20, 300 )
			#Get user
			click, _, _ = pygame.mouse.get_pressed()
			if click == 1:
				mouse = pygame.mouse.get_pos()
				if levelButton.collidepoint(mouse):
					time.sleep(0.2)
					level += 1
				elif okButton.collidepoint(mouse):
					time.sleep(0.2)
					ok = True
		else:
			game(WIN, WIDTH)
		pygame.display.update()
	pygame.quit()

def game(win, width):
	ROWS = size
	if(ROWS == 3):
		check_win = mcts.check_win_3x3
	elif(ROWS == 5):
		check_win = mcts.check_win_5x5
	elif(ROWS == 7):
		check_win = mcts.check_win_7x7
	
	for i in range(ROWS*ROWS):
		board.append(' ')
	
	grid = make_grid(ROWS, width)
	run = True
	while run:
		#draw board
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					print("SPACE")
					grid = reset(width,ROWS,grid)
		#user is O
		if user == "O":
			#AI move first
			check, winner = is_winner(board, ROWS)
			if(check == True):
				if(winner == 'draw'):
					draw_text(win, "--          DRAW         --" , font, GREEN, width / 4, 50 )
					draw_text(win, "PRESS SPACE TO PLAY AGAIN", font, GREEN, width / 8, 200 )
				else:
					draw_text(win, "WE HAVE WINNER: " + winner, font, GREEN, width / 4, 50 )
					draw_text(win, "PRESS SPACE TO PLAY AGAIN", font, GREEN, width / 8, 200 )

			if mcts.player(board) == 'X' and check == False:
				print("please wait ...")
				move = mcts.ai_move(board,'X',check_win,ROWS,ROWS, level)
				row = move // ROWS
				col = move % ROWS
				spot = grid[col][row]
				
				if( is_exist_point((col ,row), List_prev_pos) != True):	
					X = spot
					X.make_X()
					List_prev_pos.append(X.get_pos())
					board[ROWS * row + col] = 'X'
					
			else:
				if(check == False):
					if pygame.mouse.get_pressed()[0]: # LEFT
						pos = pygame.mouse.get_pos()
						row, col = get_clicked_pos(pos, ROWS, width)
						spot = grid[col][row]
						if( is_exist_point((col,row), List_prev_pos) != True):
								O = spot
								O.make_O()
								board[ROWS * row + col] = 'O'
								List_prev_pos.append(O.get_pos())
		#User is X		
		else:
			# user move first
			check, winner = is_winner(board, ROWS)
			if(check == True):
				if(winner == 'draw'):
					draw_text(win, "--          DRAW         --" , font, GREEN, width / 4, 50 )
					draw_text(win, "PRESS SPACE TO PLAY AGAIN", font, GREEN, width / 8, 200 )
				else:
					draw_text(win, "WE HAVE WINNER: " + winner, font, GREEN, width / 4, 50 )
					draw_text(win, "PRESS SPACE TO PLAY AGAIN", font, GREEN, width / 8, 200 )
			if mcts.player(board) == 'X' and check == False:
				if pygame.mouse.get_pressed()[0]: # LEFT
					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS, width)
					spot = grid[col][row]
					if( is_exist_point((col,row), List_prev_pos) != True):
						X = spot
						X.make_X()
						board[ROWS * row + col] = 'X'
						List_prev_pos.append(X.get_pos())
				check, winner = is_winner(board, ROWS)
			else:
				if(check == False):
					print("please wait ...")
					move = mcts.ai_move(board,'O',check_win,ROWS,ROWS, level)
					row = move // ROWS
					col = move % ROWS
					spot = grid[col][row]
					
					if( is_exist_point((col ,row), List_prev_pos) != True):	
						O = spot
						O.make_O()
						List_prev_pos.append(O.get_pos())
						board[ROWS * row + col] = 'O'

		
		pygame.display.update()			
	pygame.quit()

main(WIN, WIDTH)


