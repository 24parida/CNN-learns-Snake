# ************************************
# Python Snake
# ************************************
import snake
from tkinter import *
import random
import neat
import os

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 1000
SPACE_SIZE = 140
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

global gen_count
gen_count = 1

# gen - snake - properties


# NEAT implementation
global nets, ge


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    # p.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # p.add_reporter(stats)

    winner = p.run(fitness, 5)

    # print('\nBest genome:\n{!s}'.format(winner))


def fitness(genomes, config):
    global nets, ge
    nets = []
    ge = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)

    # for i in range(gen_count):
    #     next_turn(i)

    # # window.after(SPEED, fitness, genomes, config)
    # window.after(SPEED, next_turns)


def get_action(num):
    global nets

    # output = nets[num].activate(state_of_game(num))
    output = nets[num].activate((0, 1))

    return output


# def initialize():
#
#     print("initializing")
#     snakes.clear()
#     foods.clear()
#     lives.clear()
#     moves.clear()
#     scores.clear()
#
#     for i in range(gen_count):
#         snakes.append(Snake(i))
#         foods.append(Food(i))
#         directions.append('down')
#         lives.append(True)
#         moves.append(30)
#         scores.append(0)
#
#
# def restart():
#     for i in range(gen_count):
#         snakes[i] = Snake(i)
#         foods[i] = Food(i)
#         directions[i] = 'down'
#         lives[i] = True
#         moves[i] = 30
#         scores[i] = 0
#     # label.config(text="Score:{}".format(scores[0]))
#
#
def snakes_still_alive(lives):
    for i in range(gen_count):
        if lives[i]:
            return True
    return False


class Snake:

    def __init__(self, num):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake" + str(num))
            self.squares.append(square)

    def restart(self):
        self.coordinates.clear()
        self.squares.clear()


class Food:

    def __init__(self, num):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"+str(num))

    def restart(self):
        self.coordinates.clear()


def next_turns():
    print("conducting next turn")
    # for i in range(gen_count):
    #     next_turn(i)
    window.after(SPEED, next_turns)


def eval_genomes(genomes, config):
    snakes = []
    foods = []
    directions = []
    lives = []
    moves = []

    nets = []
    ge = []

    # for _, g in genomes:
    for _ in range(genomes):
        # net = neat.nn.FeedForwardNetwork.create(g, config)
        # nets.append(net)
        # g.fitness = 0
        # ge.append(g)
        snakes.append(Snake(_))
        foods.append(Food(_))
        directions.append('down')
        lives.append(True)
        moves.append(30)

    print("conducting next turn")

    for a in range(len(moves)):
        if moves[a] == 0:
            lives[a] = False
            lives[a] = False
            snakes[a].restart()
            foods[a].restart()
            # nets.pop(num)
            # ge.pop(num)
            canvas.delete("snake" + str(a))
            canvas.delete("food" + str(a))

    run = True
    while run and snakes_still_alive(lives):
        for num in range(len(snakes)):
            if lives[num]:
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

                square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"+str(num))
                snakes[num].squares.insert(0, square)

                found_food = False
                for a, b in snakes[num].coordinates:
                    if a == foods[num].coordinates[0] and b == foods[num].coordinates[1]:

                        found_food = True
                        # ge[num].fitness += 5
                        moves[num] += 20

                        canvas.delete("food"+str(num))
                        foods[num] = Food(num)

                if not found_food:
                    del snakes[num].coordinates[-1]

                    canvas.delete(snakes[num].squares[-1])

                    del snakes[num].squares[-1]

                # AI BRAIN

                if check_collisions(snakes[num]):
                    # print("direction fucked up: " + str(directions[num]))
                    lives[num] = False
                    snakes[num].restart()
                    foods[num].restart()
                    canvas.delete("snake" + str(num))
                    canvas.delete("food" + str(num))

                else:
                    # outputs = get_action(num)
                    outputs = [0, 1, 0, 0]
                    h_val = 0
                    h_ind = 0
                    for x, i in enumerate(outputs):
                        if i > h_val:
                            h_ind = x
                            h_val = i

                    if h_ind == 0:
                        directions[num] = change_direction("up", num, directions[num])
                        print("moved up")

                    elif h_ind == 1:
                        directions[num] = change_direction("down", num, directions[num])
                        print("moved down")

                    elif h_ind == 2:
                        directions[num] = change_direction("right", num, directions[num])
                        print("moved right")

                    elif h_ind == 3:
                        directions[num] = change_direction("left", num, directions[num])
                        print("moved left")
            window.after(SPEED)



def change_direction(new_direction, num, current_dir):
    dir = ''
    if new_direction == 'left':
        if current_dir != 'right':
            dir = new_direction
    elif new_direction == 'right':
        if current_dir != 'left':
            dir = new_direction
    elif new_direction == 'up':
        if current_dir != 'down':
            dir = new_direction
    elif new_direction == 'down':
        if current_dir != 'up':
            dir = new_direction
    return dir


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        print("hit x")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("hit y")
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("hit body")
            return True

    return False


# def game_over(num):
#     lives[num] = False
#     snakes[num].restart()
#     foods[num].restart()
#     # nets.pop(num)
#     # ge.pop(num)
#     canvas.delete("snake"+str(num))
#     canvas.delete("food"+str(num))


def state_of_game(num):
    rows, cols = (int(GAME_HEIGHT/SPACE_SIZE), int(GAME_WIDTH/SPACE_SIZE))

    p1 = [0] * int(GAME_WIDTH/SPACE_SIZE) ** 2
    p1a = ([0] * int(GAME_WIDTH/SPACE_SIZE) ** 2) * 3
    p2 = [[0 for i in range(cols)] for j in range(rows)]

    # convert board to a 2d array
    index = 0
    for x, y in snakes[num].coordinates:
        if index == 0:
            p2[int(y/SPACE_SIZE)][int(x/SPACE_SIZE)] = 10
        else:
            p2[int(y/SPACE_SIZE)][int(x/SPACE_SIZE)] = 20
        index += 1

    p2[int(foods[num].coordinates[1]/SPACE_SIZE)][int(foods[num].coordinates[0]/SPACE_SIZE)] = 30

    # now flatten the data
    for i in range(len(p2)):
        for j in range(len(p2[0])):
            p1[int(((GAME_WIDTH/SPACE_SIZE) * i) + j)] = p2[i][j]

    # from flattened data convert into [head,body,food] for each pixel
    for i in range(len(p1)):
        val = p1[i]
        if val == 10:
            p1a[i*3] = 10
        elif val == 20:
            p1a[(i*3) + 1] = 10
        elif val == 30:
            p1a[(i*3) + 2] = 10
    return p1a


window = Tk()
window.title("Snake game")
window.resizable(False, False)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()


# label = Label(window, text="Score:{}".format(scores[0]), font=('consolas', 40))
# label.pack()
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left', 0))
window.bind('<Right>', lambda event: change_direction('right', 0))
window.bind('<Up>', lambda event: change_direction('up', 0))
window.bind('<Down>', lambda event: change_direction('down', 0))

local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-feedforward.txt')
# run(config_path)
# initialize()
genomes = 1
eval_genomes(genomes, config_path)
window.mainloop()
