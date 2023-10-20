import turtle
import random

SCREEN_SIZE = 400
GRID_SIZE = 4
CELL_SIZE = SCREEN_SIZE // GRID_SIZE

def draw_grid():
    for i in range(GRID_SIZE + 1):
        t.penup()
        t.goto(-SCREEN_SIZE // 2, -SCREEN_SIZE // 2 + i * CELL_SIZE)
        t.pendown()
        t.forward(SCREEN_SIZE)
        t.left(90)
        t.forward(SCREEN_SIZE)
        t.backward(SCREEN_SIZE)
        t.right(90)

def draw_tile(x, y, number):
    t.penup()
    t.goto(x + CELL_SIZE/2, y - CELL_SIZE/2)
    t.fillcolor("orange")
    t.begin_fill()
    t.setheading(45)
    t.circle(CELL_SIZE * 0.3, steps=4) 
    t.end_fill()
    t.pendown()
    t.goto(t.xcor() - CELL_SIZE*0.15, t.ycor())
    if number != 0:
        t.write(number, align="center", font=("Arial", 24, "bold"))



def draw_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            draw_tile(-SCREEN_SIZE // 2 + j * CELL_SIZE, SCREEN_SIZE // 2 - i * CELL_SIZE, board[i][j])

def start_game():
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for _ in range(2):
        place_random_tile(board)
    return board

def place_random_tile(board):
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def slide(row):

    new_row = [tile for tile in row if tile != 0]
    while len(new_row) < GRID_SIZE:
        new_row.append(0)
    return new_row

def merge(row):
   
    for i in range(GRID_SIZE - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0
    return row

def move_left(board):
    new_board = []
    for row in board:
        row = slide(row)
        row = merge(row)
        new_board.append(slide(row))
    return new_board

def move_right(board):
    new_board = []
    for row in board:
        row = slide(row[::-1])
        row = merge(row)
        new_board.append(slide(row)[::-1])
    return new_board

def move_up(board):
    new_board = [list(row) for row in zip(*board)]
    for i in range(GRID_SIZE):
        new_board[i] = slide(new_board[i])
        new_board[i] = merge(new_board[i])
        new_board[i] = slide(new_board[i])
    new_board = [list(row) for row in zip(*new_board)]
    return new_board

def move_down(board):
    new_board = [list(row) for row in zip(*board)]
    for i in range(GRID_SIZE):
        new_board[i] = slide(new_board[i][::-1])
        new_board[i] = merge(new_board[i])
        new_board[i] = slide(new_board[i])[::-1]
    new_board = [list(row) for row in zip(*new_board)]
    return new_board

def on_up():
    global board
    new_board = move_up(board)
    if new_board != board:
        board = new_board
        place_random_tile(board)
        draw_game()

def on_down():
    global board
    new_board = move_down(board)
    if new_board != board:
        board = new_board
        place_random_tile(board)
        draw_game()

def on_left():
    global board
    new_board = move_left(board)
    if new_board != board:
        board = new_board
        place_random_tile(board)
        draw_game()

def on_right():
    global board
    new_board = move_right(board)
    if new_board != board:
        board = new_board
        place_random_tile(board)
        draw_game()
def check_win(board):
    for row in board:
        for tile in row:
            if tile == 2048:
                return True
    return False

def check_game_over(board):
    if any(0 in row for row in board): 
        return False
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if i > 0 and board[i][j] == board[i-1][j]:  
                return False
            if j > 0 and board[i][j] == board[i][j-1]:  
                return False
    return True

def draw_message(message):
    t.penup()
    t.goto(0, 0)
    t.color('red')
    t.write(message, align="center", font=("Arial", 36, "bold"))
    screen.update()  

def draw_game():
    t.clear()
    draw_grid()
    draw_board(board)

    if check_win(board):
        draw_message("YOU WON!")
        return

    if check_game_over(board):
        draw_message("Game Over!")
        return

    screen.update()  


if __name__ == "__main__":
    screen = turtle.Screen()
    screen.setup(SCREEN_SIZE, SCREEN_SIZE)
    screen.title("2048")
    screen.bgcolor("azure")
    screen.tracer(0)
    t = turtle.Turtle()
    t.speed(0)
    t.hideturtle()

    board = start_game()
    draw_game()

    screen.listen()
    screen.onkeypress(on_up, "Up")
    screen.onkeypress(on_down, "Down")
    screen.onkeypress(on_left, "Left")
    screen.onkeypress(on_right, "Right")

    turtle.mainloop()
