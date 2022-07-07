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
SPEED = 600
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
total_models = 1

generation = 1
highest_fitness = 0
hf_index = 0
best_weights = []

INPUT_LAYER = 199;
SECOND_LAYER = 50;
OUTPUT_LAYER = 4;


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

        self.coordinates.clear()

        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

        canvas.create_rectangle(x,y,x+SPACE_SIZE, y+SPACE_SIZE, fill=BACKGROUND_COLOR)

        if draw:
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food" + str(num))
        else:
            canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR, tag="food" + str(num))

    def getBody(self):
        return self.coordinates

    def clean(self, num):
        x = self.coordinates[0]
        y = self.coordinates[1]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR, tag="food" + str(num))


class Snake:

    def __init__(self, num):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR, tag="snake" + str(num))
            self.squares.append(square)

    def getBody(self):
        return self.coordinates

    def restart(self, num):
        global BODY_PARTS
        directions[num] = 'down'

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

    for x, y in snakes[model_num].coordinates:
        rx = x / 50
        ry = y / 50
        positions[int((14 * rx) + ry)] = 0.5

    x = food_s[model_num].coordinates[0]
    y = food_s[model_num].coordinates[1]
    rx = x / 50
    ry = y / 50

    if directions[model_num] == 'down':
        positions[196] = 2
    elif directions[model_num] == 'up':
        positions[196] = 4
    elif directions[model_num] == 'right':
        positions[196] = 6
    elif directions[model_num] == 'left':
        positions[196] = 8

    positions[197] = int(rx)
    positions[198] = int(ry)

    neural_input = np.asarray(positions)
    neural_input = np.atleast_2d(neural_input)

    # TODO
    # do multiple outputs since we are working with a output layer of size 4
    output_prob = current_pool[model_num].predict(neural_input)

    final_prob = [0, 0, 0, 0]
    final_prob[0] = output_prob[0][0]
    final_prob[1] = output_prob[0][1]
    final_prob[2] = output_prob[0][2]
    final_prob[3] = output_prob[0][3]

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
    global hf_index
    global highest_fitness

    hf_index = 0
    highest_fitness = 0

    for i in range(total_models):
        lives.append(True)
        snake = Snake(i)
        snakes.append(snake)
        if i == hf_index:
            food = Food(i, True)
        else:
            food = Food(i, True)
        food_s.append(food)
        fitness.append(0)
        directions.append('down')
    # initialize_models()


def next_turns():
    global hf_index

    for i in range(total_models):
        if i == hf_index:
            next_turn(snakes[i], food_s[i], True, i)
        else:
            next_turn(snakes[i], food_s[i], True, i)


def next_turn(snake, food, draw, num):

    global lives
    global highest_fitness
    global hf_index

    x, y = snake.coordinates[0]

    action = predict_action(num)
    action_string = [''] * 4

    print(str(action))
    # if action[0] == 1:
    #     directions[num] = 'left'
    #     action_string[0] = 'left, '
    # if action[1] == 1:
    #     directions[num] = 'right'
    #     action_string[1] = 'right, '
    # if action[2] == 1:
    #     directions[num] = 'up'
    #     action_string[2] = 'up, '
    # if action[3] == 1:
    #     directions[num] = 'down'
    #     action_string[3] = 'down'
    direction_temp = 0
    for direction in range(len(action)):
        if action[direction] > action[direction_temp]:
            direction_temp = direction
    print(str(direction_temp))

    if direction_temp == 0:
        directions[num] = 'down'
    elif direction_temp == 1:
        directions[num] = 'up'
    elif direction_temp == 2:
        directions[num] = 'right'
    elif direction_temp == 3:
        directions[num] = 'left'
    print(str(directions[num]))

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
        food.restart(num, draw)

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]
    if check_collisions(snake) and lives[num]:
        lives[num] = False
        snakes_still_alive = False
        for life in lives:
            if life:
                snakes_still_alive = True
        if snakes_still_alive:
            game_over_bnr(num)
        else:
            game_over_bnr(num)
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
    global lives
    global highest_fitness
    global hf_index

    highest_fitness = 0
    hf_index = 0
    label.pack()

    print("initialized")
    for i in range(total_models):
        # canvas.delete("snake" + str(i))
        # canvas.delete("food" + str(i))
        lives[i] = True

        fitness[i] = 0
        directions[i] = 'down'
    for i in range(total_models):
        snakes[i].restart(i)
        if i == hf_index:
            food_s[i].restart(i, True)
        else:
            food_s[i].restart(i, True)


def game_over_bnr(num):
    print("bnr")
    snakes[num].clean()
    food_s[num].clean(num)

    canvas.delete("snake" + str(num))
    canvas.delete("food" + str(num))

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

# window.bind('<Left>', lambda event: change_direction('left', 0))
# window.bind('<Right>', lambda event: change_direction('right', 0))
# window.bind('<Up>', lambda event: change_direction('up', 0))
# window.bind('<Down>', lambda event: change_direction('down', 0))

initialize_game()
initialize_models()
next_turns()

window.mainloop()
