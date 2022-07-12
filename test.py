# ************************************
# Python Snake
# ************************************
import snake
from tkinter import *
import random
import os
import neat
import pickle
import visualize

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
FOOD_COLOR2 = "blue"
BACKGROUND_COLOR = "#000000"

# gen - snake - properties
global snakes, foods, directions, moves, nets, ge, count, lives
snakes = []
foods = []
directions = []
moves = []
nets = []
ge = []
count = []
lives = []

global fit, fit_id
fit = 0
fit_id = 0


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-64')
    winner = p.run(eval_genomes, 1)
    print('\nBest genome:\n{!s}'.format(winner))

    # winner_net = neat.nn.FeedForwardNetwork.create(winner, config_file)
    # visualize.plot_stats(stats, view=True)
    print("type winner: " + str(type(winner)))
    visualize.draw_net(config=config, genome=winner, view=True, filename='best_net.svg', show_disabled=False)

    # try:
    #     pickle.dump(winner_net, open("winner.pickle", "wb"))
    # except:
    #     print("SAVING BEST MODEL DIDNT WORK")
    # try:
    #     node_names = {-1: 'A', -2: 'B', 0: 'A XOR B'}
    #     visualize.draw_net(config, winner, True, node_names=node_names)
    #     visualize.draw_net(config, winner, True, node_names=node_names, prune_unused=True)
    #     visualize.plot_stats(stats, ylog=False, view=True)
    #     visualize.plot_species(stats, view=True)
    # except:
    #     print("visualization failed")


def initialize(genomes, config):
    print("initializing")
    global window, canvas, label
    window = Tk()
    window.title("Snake game")
    window.resizable(False, False)

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    label = Label(window, text="Score:{}".format(fit), font=('consolas', 40))
    label.pack()
    canvas.pack()
    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    snakes.clear()
    foods.clear()
    directions.clear()
    moves.clear()
    count.clear()
    lives.clear()

    for i, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        ge.append(genome)
    for i in range(len(genomes)):
        snakes.append(Snake(i))
        foods.append(Food(i))
        directions.append('down')
        moves.append(100)
        count.append(i)
        lives.append(True)


def eval_genomes(genomes, config):
    print("evaluating genomes...")
    initialize(genomes, config)
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
    canvas.create_oval(a, b, a + SPACE_SIZE, b + SPACE_SIZE, fill=FOOD_COLOR, tag="food" + str(num))

    for x, y in snakes[num].coordinates:
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR,
                                         tag="snake" + str(num))
        snakes[num].squares.append(square)


def main():
    global fit, fit_id
    pops = []
    for i in range(len(snakes)):
        if lives[i]:
            next_turn(i)
            fit = 0
            fit_id = 0
            for id, genome in enumerate(ge):
                if genome.fitness > fit:
                    fit_id = id
                    fit = genome.fitness
            label.config(text="Score:{}".format(fit))
            if i == fit_id:
                draw(i)
        if check_collisions(snakes[i]) or moves[i] == 0:
            lives[i] = False
            game_over(i)
            pops.append(i)
        else:
            try:
                output = nets[i].activate(state_of_game(i))
            except:
                print('index failed: ' + str(i))
                print('len nets: ' + str(len(nets)))
                print('len snakes: ' + str(len(snakes)))
            di = output.index(max(output))
            if di == 0:
                change_direction('down', i)
            elif di == 1:
                change_direction('up', i)
            elif di == 2:
                change_direction('right', i)
            elif di == 3:
                change_direction('left', i)

    if len(pops) != 0:
        pops.sort(reverse=True)
        for pop in pops:
            snakes.pop(pop)
            foods.pop(pop)
            directions.pop(pop)
            moves.pop(pop)
            count.pop(pop)
            lives.pop(pop)
            nets.pop(pop)
            ge.pop(pop)

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

    # square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"+str(num))
    # snakes[num].squares.insert(0, square)

    found_food = False
    for a, b in snakes[num].coordinates:
        if a == foods[num].coordinates[0] and b == foods[num].coordinates[1]:
            found_food = True
            moves[num] += 30
            ge[num].fitness += 5
            a = count[num]
            canvas.delete("food" + str(a))
            foods[num] = Food(a)

    if not found_food:
        del snakes[num].coordinates[-1]

        # canvas.delete(snakes[num].squares[-1])

        # del snakes[num].squares[-1]


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
    canvas.delete("snake" + str(a))
    canvas.delete("food" + str(a))


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

    w = int(GAME_WIDTH / SPACE_SIZE)
    h = int(GAME_HEIGHT / SPACE_SIZE)

    return [a - x, y - b, w - x, y - h]
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

# window.bind('<Left>', lambda event: change_direction('left', 0))
# window.bind('<Right>', lambda event: change_direction('right', 0))
# window.bind('<Up>', lambda event: change_direction('up', 0))
# window.bind('<Down>', lambda event: change_direction('down', 0))

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)
