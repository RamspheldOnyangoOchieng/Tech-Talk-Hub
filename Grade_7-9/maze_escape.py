"""
🎮 MAZE ESCAPE GAME - EXTREME EDITION 🎮
Uses Turtle Graphics (supported by EduBlocks)
Simple functions - no classes!
"""

import turtle
import random
import time

# Game settings
cell_size = 28  # Resized to fit screen better
moves = 0
games_won = 0
best_score = None

# A much tighter, more complex maze (15x15)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Player starting position
player_row = 1
player_col = 1

# Centering constants for 15x15 grid
START_X = -210
START_Y = 210

# Set up the screen
screen = turtle.Screen()
screen.title("Maze Escape Game - Extreme Edition")
screen.bgcolor("#1a1a2e") # Darker background for more intensity
screen.setup(width=580, height=650)
screen.tracer(0)

# Create turtles for drawing
wall_turtle = turtle.Turtle()
wall_turtle.hideturtle()
wall_turtle.speed(0)

player_turtle = turtle.Turtle()
player_turtle.shape("circle")
player_turtle.color("#00ff41") # Matrix green
player_turtle.penup()

treasure_turtle = turtle.Turtle()
treasure_turtle.shape("circle")
treasure_turtle.color("gold")
treasure_turtle.penup()

# Text turtle for displaying info
text_turtle = turtle.Turtle()
text_turtle.hideturtle()
text_turtle.penup()
text_turtle.color("white")

def place_random_treasure():
    """Place the treasure in a random empty spot far from start"""
    global maze
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 2:
                maze[row][col] = 0
    
    empty_spots = []
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 0 and not (row == 1 and col == 1):
                distance = abs(row - 1) + abs(col - 1)
                if distance >= 12: # Farther for 15x15
                    empty_spots.append((row, col))
    
    if empty_spots:
        treasure_row, treasure_col = random.choice(empty_spots)
        maze[treasure_row][treasure_col] = 2

def draw_square(x, y, color):
    """Draw a square at the given position"""
    wall_turtle.penup()
    wall_turtle.goto(x, y)
    wall_turtle.pendown()
    wall_turtle.fillcolor(color)
    wall_turtle.begin_fill()
    for _ in range(4):
        wall_turtle.forward(cell_size)
        wall_turtle.right(90)
    wall_turtle.end_fill()

def draw_maze():
    """Draw the entire maze"""
    wall_turtle.clear()
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            x = START_X + (col * cell_size)
            y = START_Y - (row * cell_size)
            if maze[row][col] == 1:
                draw_square(x, y, "#e94560") # Sleek red walls
            else:
                draw_square(x, y, "#16213e") # Dark path

def update_player_position():
    """Move the player turtle"""
    x = START_X + (player_col * cell_size) + (cell_size / 2)
    y = START_Y - (player_row * cell_size) - (cell_size / 2)
    player_turtle.goto(x, y)

def update_treasure_position():
    """Move the treasure turtle"""
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == 2:
                x = START_X + (col * cell_size) + (cell_size / 2)
                y = START_Y - (row * cell_size) - (cell_size / 2)
                treasure_turtle.goto(x, y)

def update_display():
    """Update the text display"""
    text_turtle.clear()
    text_turtle.goto(0, 270)
    text_turtle.write(f"Moves: {moves}  |  Games: {games_won}  |  Best: {best_score if best_score else '--'}", 
                     align="center", font=("Arial", 14, "bold"))

def check_win():
    return maze[player_row][player_col] == 2

def show_win_message():
    global games_won, best_score
    games_won += 1
    if best_score is None or moves < best_score:
        best_score = moves
        msg = f"ESCAPE SUCCESSFUL!\n{moves} MOVES - NEW BEST!"
    else:
        msg = f"ESCAPE SUCCESSFUL!\n{moves} MOVES"
    
    text_turtle.goto(0, 0)
    text_turtle.color("#00ff41")
    text_turtle.write(msg, align="center", font=("Arial", 20, "bold"))
    text_turtle.color("white")
    screen.update()
    time.sleep(2)
    restart_game()

def move_up():
    global player_row, moves
    if maze[player_row - 1][player_col] != 1:
        player_row -= 1
        moves += 1
        update_player_position()
        update_display()
        screen.update()
        if check_win(): show_win_message()

def move_down():
    global player_row, moves
    if maze[player_row + 1][player_col] != 1:
        player_row += 1
        moves += 1
        update_player_position()
        update_display()
        screen.update()
        if check_win(): show_win_message()

def move_left():
    global player_col, moves
    if maze[player_row][player_col - 1] != 1:
        player_col -= 1
        moves += 1
        update_player_position()
        update_display()
        screen.update()
        if check_win(): show_win_message()

def move_right():
    global player_col, moves
    if maze[player_row][player_col + 1] != 1:
        player_col += 1
        moves += 1
        update_player_position()
        update_display()
        screen.update()
        if check_win(): show_win_message()

def restart_game():
    global player_row, player_col, moves
    player_row, player_col, moves = 1, 1, 0
    place_random_treasure()
    draw_maze()
    update_player_position()
    update_treasure_position()
    update_display()
    screen.update()

# Input binding
screen.listen()
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")
screen.onkey(restart_game, "r")
screen.onkey(restart_game, "R")

# Init
restart_game()
turtle.done()
