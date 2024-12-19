from tkinter import *
import random

# Set up our window
root = Tk()
root.title("Spaced Invaders!!")
root.geometry("600x450")
root.config(bg="#1e1b1c")

# Add our images
bg_image = PhotoImage(file="images/starbg.png")
player_image = PhotoImage(file="images/ship.png") # 50x40
enemy_image = PhotoImage(file="images/enemy.png") # 30x30


# Create a canvas
canvas = Canvas(root, width=600, height=400, bg="black", highlightthickness=0)
canvas.pack()

# Add Background Image
canvas_bg = canvas.create_image(0,0, anchor=NW, image=bg_image)


# Game Variables
player_speed = 10
bullet_speed = -15 # negative is up
enemy_speed = 2
enemy_direction = 1 #1=right, -1=left


# Lists to hold bullets and enemies
bullets = []
enemies = []

# Track Score
score = 0
score_label = Label(root, text=f'Score: {score}', font=("Helvetica", 14), bg="#1e1b1c", fg="white")
score_label.pack()

# Create a player spaceship
#player = canvas.create_rectangle(275, 360, 325, 380, fill="blue")
player = canvas.create_image(300,360, anchor=CENTER, image=player_image) # Center position is 300,360
#x-from the left, y-from the top




# x1, y1, x2, y2
# Left Side(x1), Top(y1), Right Side(x2), Bottom(y2)
'''
-------y1--------
|               |
x1              x2
|               |
-------y2--------

'''


# Move the player
def move_player(event):
	x = 0
	# Get x coordinates and half width to find left edge
	player_x, player_y = canvas.coords(player) #[x,y]
	half_width = 25

	# center is 300, left edge is 300 - 25
	if event.keysym == "Left" and player_x - half_width > 0:
		x = -player_speed
	elif event.keysym == "Right" and player_x + half_width < 600:
		x = player_speed

	canvas.move(player, x, 0)
	# player, x-coor, y-coord


# Bind the keyboard
root.bind("<Left>", move_player)
root.bind("<Right>", move_player)

# Create some bullets
def fire_bullet(event):
	# Get player coords
	player_x, player_y = canvas.coords(player)

	bullet = canvas.create_rectangle(player_x - 2, player_y - 20, player_x + 2, player_y - 10, fill="yellow")
	# 4 corrdinates, (x1, y1, x2, y2)
    # 1: moves 22 to the right of the left side of player
    # 2: 350 y-cordinate of the top edge of the bullet, just above player 400
    # 3: 22 left of left edge of player
    # 4: 340 y-coordinate bottom edge of the bullet

    # Keep track of the bullets that have been fired
	bullets.append(bullet)


# Fire the bullets - bind the space key
root.bind("<space>", fire_bullet)


# Create rows of enemies
def create_enemies():
	for i in range(5):  # Rows
		for j in range(8):  # Columns
			# Create Enemies
			#enemy = canvas.create_rectangle(50 + j * 60, 50 + i * 30, 80 + j * 60, 80 + i * 30, fill="red")
			x = 50 + j * 60
			y = 50 + i * 40


			enemy = canvas.create_image(x,y, anchor=NW, image=enemy_image)
			# x1, y1, x2, y2
			# 110, 80, 140, 110
			# 170, 110, 200, 140

			# Add the enemy to the enemies list
			enemies.append(enemy)

# Create our enemines
create_enemies()

# Move our bullets
def move_bullets():
	for bullet in bullets:
		canvas.move(bullet, 0, bullet_speed)
		# bullet, x-coor, y-coord

		# Check to see if bullet reached the top of the screen and remove it.
		if canvas.coords(bullet)[1] < 0:
			# Delete from canvas/game
			canvas.delete(bullet)
			# Remove from bullets list
			bullets.remove(bullet)


# Move the enemies
def move_enemies():
	global enemy_direction	
	# Did we reach the end
	edge_reached = False

	for enemy in enemies:
		# Move the enemies horizontally
		canvas.move(enemy, enemy_speed * enemy_direction, 0)
		# enemy, x-coor, y-coord
		# if enemy direction is 1 = right, if -1 = left

		# canvas.coords(enemy) = [x1, y1, x2, y2]
		#x1, y1, x2, y2 = canvas.coords(enemy)
		x1, y1 = canvas.coords(enemy) #[x,y]
		x2 = x1 + 30 # Right Edge
		x1 = x1 # Left Edge



		# Check if any enemy reaches the edge
		if x2 >= 600 or x1 <=0:
			edge_reached = True

	# If the edge is reached, move all enemies down one row and change directions
	if edge_reached:
		# change direction left/right
		enemy_direction *= -1
		# Move them all down 20
		for enemy in enemies:
			canvas.move(enemy, 0, 20)
			# enemy, x-coor, y-coord



# Check for collisions
def check_collisions():
	global score
	for bullet in bullets:
		# grab our bullet coords
		bullet_coords = canvas.coords(bullet) #x1, y1, x2, y2

		for enemy in enemies:
			enemy_coords = canvas.coords(enemy) #x1, y1, x2, y2
			enemy_width, enemy_height = 30,30

			# Check if bullet and enemy overlap
			enemy_x1 = enemy_coords[0] # [x,y]
			enemy_y1 = enemy_coords[1]
			enemy_x2 = enemy_x1 + enemy_width
			enemy_y2 = enemy_y1 + enemy_height


			if (bullet_coords[2] > enemy_x1 and bullet_coords[0] < enemy_x2 and 
				bullet_coords[3] > enemy_y1 and bullet_coords[1] < enemy_y2):

				# remove bullet and enemy on collision
				canvas.delete(bullet)
				canvas.delete(enemy)
				# remove them from their lists
				bullets.remove(bullet)
				enemies.remove(enemy)

				# update the score
				score += 10
				score_label.config(text=f"Score: {score}")
				break







# Game loop
def game_loop():
	move_bullets()
	move_enemies()
	check_collisions()

	# Check to see if you won! And killed all the enemies
	if not enemies:
		canvas.create_text(300,200, text="You Win!", fill="white", font=("Helvetica", 24))
		# Ends the Game Loop
		return


	# Check if enemies reach the player area (game over condition)
	for enemy in enemies:
		enemy_x, enemy_y = canvas.coords(enemy)

		if enemy_y + 30 >= 360:
			# x1, y1, x2, y2
			canvas.create_text(300, 200, text="Game Over", fill="white", font=("Helvetica", 24))
			# Ends the Game Loop
			return



	# loop the game loop
	root.after(50, game_loop) # delay 50 miliseconds



game_loop()

root.mainloop()