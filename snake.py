# ************************************
# Python Snake
# ************************************
import random
from tkinter import *

import numpy as np
from keras.layers import Dense, Activation
from keras.models import Sequential

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# generation
lives = []
snakes = []
food_s = []
directions = []
positions = [0] * 199

# machine learning
current_pool = []
fitness = []
total_models = 10

generation = 1
highest_fitness = 0
hf_index = 0
highest_score = -1
best_weights = []

INPUT_LAYER = 199;
SECOND_LAYER = 50;
OUTPUT_LAYER = 4;


def save_pool():
    for snake in range(total_models):
        current_pool[snake].save_weights("SavedModels/models_new" + str(snake) + ".keras")
    print("saved all models")


def create_model():
    model = Sequential()
    model.add(Dense(INPUT_LAYER, input_shape=(INPUT_LAYER,)))
    model.add(Activation('relu'))
    model.add(Dense(SECOND_LAYER, input_shape=(INPUT_LAYER,)))
    model.add(Activation('relu'))
    model.add(Dense(OUTPUT_LAYER, input_shape=(SECOND_LAYER,)))
    model.add(Activation('sigmoid'))

    model.compile(loss='mse', optimizer='adam')

    return model


def predict_action(model_num):
    global current_pool
    global positions

    for x,y in snakes[model_num].coordinates:
        print("a")
        rx = x/50
        ry = y/50
        print(str(rx) + "rx")
        print(str(ry) + "ry")
        print((14*rx) + ry)
        positions[int((14*rx) + ry)] = 0.5

    x = food_s[model_num].coordinates[0]
    y = food_s[model_num].coordinates[1]
    rx = x/50
    ry = y/50

    if directions[model_num] == 'down':
        positions[196] = -1
    elif directions[model_num] == 'up':
        positions[196] = 1
    elif directions[model_num] == 'right':
        positions[196] = 0.5
    elif directions[model_num] == 'left':
        positions[196] = -0.5

    positions[197] = int(rx)
    positions[198] = int(ry)

    neural_input = np.asarray(positions)
    neural_input = np.atleast_2d(neural_input)

    # TODO
    # do multiple outputs since we are working with a output layer of size 4
    output_prob = current_pool[model_num].predict(neural_input)
    print("output_prob" + str(output_prob))

    final_prob = [0, 0, 0, 0]

    if output_prob[0][0] >= .5:
        final_prob[0] = 1
    if output_prob[0][1] >= .5:
        final_prob[1] = 1
    if output_prob[0][2] >= .5:
        final_prob[2] = 1
    if output_prob[0][3] >= 0.5:
        final_prob[3] = 1
    print(final_prob)
    return final_prob


def model_crossover(parent1, parent2):
    global current_pool

    weight1 = current_pool[parent1].get_weights()
    weight2 = current_pool[parent2].get_weights()

    new_weight1 = weight1
    new_weight2 = weight2

    gene = random.randint(0, len(new_weight1) - 1)

    new_weight1[gene] = weight2[gene]
    new_weight2[gene] = weight1[gene]

    return np.asarray([new_weight1, new_weight2])


def model_mutate(weights):
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if random.uniform(0, 1) > 0.85:
                change = random.uniform(-0.5, 0.5)
                weights[i][j] += change

    return weights


def showGameOverScreen():
    global current_pool
    global fitness
    global generation

    new_weights = []
    total_fitness = 0

    global highest_fitness
    global hf_index
    global best_weights
    updated = False

    # get total fitness / highest fitness
    for select in range(total_models):
        total_fitness += fitness[select]

        if fitness[select] > highest_fitness:
            updated = True
            highest_fitness = fitness[select]
            hf_index = select
            best_weights = current_pool[select].get_weights()

    # get top two parents
    parent1 = random.randint(0, total_models - 1)
    parent2 = random.randint(0, total_models - 1)

    for i in range(total_models):
        if fitness[i] >= fitness[parent1]:
            parent1 = i

    for j in range(total_models):
        if j != parent1:
            if fitness[j] > fitness[parent2]:
                parent2 = j
    # getting crossover weights

    for select in range(total_models // 2):
        cross_over_weights = model_crossover(parent1, parent2)
        if not updated:
            cross_over_weights[1] = best_weights
        mutated1 = model_mutate(cross_over_weights[0])
        mutated2 = model_mutate(cross_over_weights[1])

        new_weights.append(mutated1)
        new_weights.append(mutated2)

        for select in range(len(new_weights)):
            fitness[select] = -100
            current_pool[select].set_weights(new_weights[select])
        save_pool()

        generation += 1
        return


def initialize_models():
    global total_models
    global fitness
    for i in range(total_models):
        model = create_model()
        current_pool.append(model)
        fitness.append(-100)


def initialize_game():
    global lives
    global snakes
    global food_s

    for i in range(total_models):
        lives.append(True)
        snake = Snake(i)
        snakes.append(snake)
        if i == hf_index:
            food = Food(i, True)
        else:
            food = Food(i, False)
        food_s.append(food)
        fitness.append(0)
        directions.append('down')
    # initialize_models()


def next_turns():
    for i in range(total_models):
        if i == hf_index:
            next_turn(snakes[i], food_s[i], True, i)

        else:
            next_turn(snakes[i], food_s[i], False, i)


class Snake:

    def __init__(self, num):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR,
                                             tag="snake" + str(num))
            self.squares.append(square)

    def getBody(self):
        return self.coordinates

    def restart(self, num):
        global BODY_PARTS
        for i in range(total_models):
            directions[i] = 'down'

        self.body_size = BODY_PARTS
        self.coordinates.clear()
        self.squares.clear()

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR,
                                             tag="snake" + str(num))
            self.squares.append(square)

    def clean(self):
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR)


class Food:
    def __init__(self, num, draw):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        if draw:
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food" + str(num))
        else:
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR, tag="food" + str(num))

    def restart(self, num, draw):

        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE

        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

        if draw:
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food" + str(num))
        else:
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR, tag="food" + str(num))

    def getBody(self):
        return self.coordinates


def next_turn(snake, food, draw, num):
    global lives
    global highest_fitness
    global hf_index

    x, y = snake.coordinates[0]

    action = predict_action(num)
    if action[0] == 1:
        directions[num] = 'left'
        print("went left")
    if action[1] == 1:
        directions[num] = 'right'
        print("went right")
    if action[2] == 1:
        directions[num] = 'up'
        print("went up")
    if action[3] == 1:
        directions[num] = 'down'
        print("went down")

    if directions[num] == "up":
        y -= SPACE_SIZE
    elif directions[num] == "down":
        y += SPACE_SIZE
    elif directions[num] == "left":
        x -= SPACE_SIZE
    elif directions[num] == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    if draw:
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    else:
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        fitness[num] += 1
        if fitness[num] > highest_fitness:
            highest_fitness = fitness[num]
            hf_index = num
        label.config(text="High Score:{}".format(highest_fitness))

        canvas.delete("food" + str(num))
        food = Food(num, draw)

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]
    if check_collisions(snake):
        lives[num] = False
        snakes_still_alive = False
        for life in lives:
            if life:
                snakes_still_alive = True
        if snakes_still_alive:
            game_over_bnr(num)
        else:
            game_over()

    window.after(SPEED, next_turn, snake, food, draw, num)


def change_direction(new_direction, num):
    global directions

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


def game_over():
    global hf_index
    for i in range(total_models):
        snakes[i].clean()
        canvas.delete("snake" + str(i))
        canvas.delete("food" + str(i))
    for i in range(total_models):
        snakes[i].restart(i)
        if i == hf_index:
            food_s[i].restart(i, True)
        else:
            food_s[i].restart(i, True)
    showGameOverScreen()


def game_over_bnr(num):
    snakes[num].clean
    canvas.delete('snake' + str(num))
    canvas.delete('food' + str(num))


window = Tk()
window.title("Snake game")
window.resizable(False, False)

label = Label(window, text="High Score:{}".format(highest_fitness), font=('consolas', 30))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

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


initialize_game()
initialize_models()
actions = predict_action(0)
next_turns()

window.mainloop()
