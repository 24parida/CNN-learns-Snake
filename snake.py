# ************************************
# Python Snake
# ************************************
import snake
from tkinter import *
import random
import os
import neat
from random import uniform
import visualize
import pickle


GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 400
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
FOOD_COLOR2 = "blue"
BACKGROUND_COLOR = "#000000"

global gen_count
gen_count = 1

# gen - snake - properties
global snakes, foods, directions, moves, nets, ge, count
snakes = []
foods = []
directions = []
moves = []
nets = []
ge = []
count = []

global winner


def initialize():
    global winner
    print("initializing")
    global window, canvas
    window = Tk()
    window.title("Snake game")
    window.resizable(False, False)

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack()
    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')

    winner = pickle.load(open("winner.pickle", "rb"))
    visualize.draw_net(config_path, )
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    for i in range(gen_count):
        snakes.append(Snake(i))
        foods.append(Food(i))
        directions.append('down')
        moves.append(30)
        count.append(i)


def eval_genomes():
    print("evaluating genomes...")
    initialize()
    main()


class Snake:

    def __init__(self, num):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.insert(0, [0, (SPACE_SIZE * i)])

    def restart(self):
        self.coordinates.clear()
        self.squares.clear()


class Food:

    def __init__(self, num):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

    def restart(self):
        self.coordinates.clear()


def draw(num):
    canvas.delete(ALL)

    a = foods[num].coordinates[0]
    b = foods[num].coordinates[1]
    canvas.create_oval(a, b, a + SPACE_SIZE, b + SPACE_SIZE, fill=FOOD_COLOR, tag="food"+str(num))

    for x, y in snakes[num].coordinates:
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR,
                                         tag="snake" + str(num))
        snakes[num].squares.append(square)


def main():
    global winner
    pops = []
    for i in range(len(snakes)):
        next_turn(i)
        if i == 0:
            draw(i)
        if check_collisions(snakes[i]) or moves[i] == 0:
            game_over(i)
            pops.append(i)
        else:
            output = winner.activate(state_of_game(i))
            di = output.index(max(output))
            if di == 0:
                change_direction('down', i)
            elif di == 1:
                change_direction('up', i)
            elif di == 2:
                change_direction('right', i)
            elif di == 3:
                change_direction('left', i)
            # window.bind('<Left>', lambda event: change_direction('left', 0))
            # window.bind('<Right>', lambda event: change_direction('right', 0))
            # window.bind('<Up>', lambda event: change_direction('up', 0))
            # window.bind('<Down>', lambda event: change_direction('down', 0))
            #
            # window.bind('<a>', lambda event: change_direction('left', 1))
            # window.bind('<d>', lambda event: change_direction('right', 1))
            # window.bind('<w>', lambda event: change_direction('up', 1))
            # window.bind('<s>', lambda event: change_direction('down', 1))
            # print(state_of_game(i))
        #     di = output.index(max(output))
        #     if di == 0:
        #         change_direction('down', i)
        #     elif di == 1:
        #         change_direction('up', i)
        #     elif di == 2:
        #         change_direction('right', i)
        #     elif di == 3:
        #         change_direction('left', i)

    if len(pops) != 0:
        pops.sort(reverse=True)
        for pop in pops:
            snakes.pop(pop)
            foods.pop(pop)
            directions.pop(pop)
            moves.pop(pop)
            count.pop(pop)

    if len(snakes) != 0:
        window.after(SPEED, main)
        window.mainloop()
    else:
        canvas.delete(ALL)
        window.destroy()
        return


def next_turn(num):
    moves[num] -= 1

    x, y = snakes[num].coordinates[0]
    if directions[num] == "up":
        y -= SPACE_SIZE
    elif directions[num] == "down":
        y += SPACE_SIZE
    elif directions[num] == "left":
        x -= SPACE_SIZE
    elif directions[num] == "right":
        x += SPACE_SIZE

    snakes[num].coordinates.insert(0, (x, y))

    found_food = False
    for a, b in snakes[num].coordinates:
        if a == foods[num].coordinates[0] and b == foods[num].coordinates[1]:

            found_food = True
            moves[num] += 20
            # ge[num].fitness += 5
            # if ge[num].fitness > 50:
            #     pickle.dump(nets[num], open("best.pickle", "wb"))
            #     break
            a = count[num]
            canvas.delete("food"+str(a))
            foods[num] = Food(a)

    if not found_food:
        del snakes[num].coordinates[-1]


def change_direction(new_direction, num):
    if new_direction == 'left':
        if directions[num] != 'right':
            directions[num] = new_direction
    elif new_direction == 'right':
        if directions[num] != 'left':
            directions[num] = new_direction
    elif new_direction == 'up':
        if directions[num] != 'down':
            directions[num] = new_direction
    elif new_direction == 'down':
        if directions[num] != 'up':
            directions[num] = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over(num):
    snakes[num].restart()
    foods[num].restart()
    a = count[num]
    canvas.delete("snake"+str(a))
    canvas.delete("food"+str(a))


def state_of_game(num):
    a = foods[num].coordinates[0]
    b = foods[num].coordinates[1]
    x, y = snakes[num].coordinates[0]
    a /= SPACE_SIZE
    a = int(a)
    b /= SPACE_SIZE
    b = int(b)
    x /= SPACE_SIZE
    x = int(x)
    y /= SPACE_SIZE
    y = int(y)

    w = int(GAME_WIDTH/SPACE_SIZE)
    h = int(GAME_HEIGHT/SPACE_SIZE)


    return[a-x, y-b, w-x, y-h]
    # rows, cols = (int(GAME_HEIGHT/SPACE_SIZE), int(GAME_WIDTH/SPACE_SIZE))
    #
    # p1 = [0] * int(GAME_WIDTH/SPACE_SIZE) ** 2
    # p1a = ([0] * int(GAME_WIDTH/SPACE_SIZE) ** 2) * 3
    # p2 = [[0 for i in range(cols)] for j in range(rows)]
    #
    # # convert board to a 2d array
    # index = 0
    # for x, y in snakes[num].coordinates:
    #     if index == 0:
    #         p2[int(y/SPACE_SIZE)][int(x/SPACE_SIZE)] = 10
    #     else:
    #         p2[int(y/SPACE_SIZE)][int(x/SPACE_SIZE)] = 20
    #     index += 1
    #
    # p2[int(foods[num].coordinates[1]/SPACE_SIZE)][int(foods[num].coordinates[0]/SPACE_SIZE)] = 30
    #
    # # now flatten the data
    # for i in range(len(p2)):
    #     for j in range(len(p2[0])):
    #         p1[int(((GAME_WIDTH/SPACE_SIZE) * i) + j)] = p2[i][j]
    #
    # # from flattened data convert into [head,body,food] for each pixel
    # for i in range(len(p1)):
    #     val = p1[i]
    #     if val == 10:
    #         p1a[i*3] = 10
    #     elif val == 20:
    #         p1a[(i*3) + 1] = 10
    #     elif val == 30:
    #         p1a[(i*3) + 2] = 10
    # return p1a


global window
global canvas


if __name__ == '__main__':
    eval_genomes()


