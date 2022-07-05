# ************************************
# Python Snake
# ************************************
from tkinter import *
import random
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 500
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# machine learning
current_pool = []
fitness = []
total_models = 10

generation = 1
highest_fitness = -1
best_weights = []

INPUT_LAYER = 1;
SECOND_LAYER = 1;
OUTPUT_LAYER = 1;


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


def predict_action(positions, model_num):
    global current_pool

    # TODO
    # map positions into a 1d array
    neural_input = np.asarray(positions)
    neural_input = np.atleast_2d(neural_input)

    # TODO
    # do multiple outputs since we are working with a output layer of size 4
    output_prob = current_pool[model_num].predict(neural_input, 1)[0]

    if output_prob[0] <= .5:
        return 1
    return 2


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
    global best_weights
    updated = False

    # get total fitness / highest fitness
    for select in range(total_models):
        total_fitness += fitness[select]

        if fitness[select] >= highest_fitness:
            updated = True
            highest_fitness = fitness[select]
            best_weights = current_pool[select].get_weights()

    # get top two parents
    parent1 = random.randint(0, total_models-1)
    parent2 = random.randint(0, total_models-1)

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
    for i in range(total_models):
        model = create_model()
        current_pool.append(model)
        fitness.append(-100)



class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR, tag="snake")
            self.squares.append(square)

    def getBody(self):
        return self.cordinates


class Food:
    def __init__(self, num):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"+num)


def next_turn(snake, food, draw, WASD, num):
    x, y = snake.coordinates[0]
    if WASD:
        if direction2 == "up":
            y -= SPACE_SIZE
        elif direction2 == "down":
            y += SPACE_SIZE
        elif direction2 == "left":
            x -= SPACE_SIZE
        elif direction2 == "right":
            x += SPACE_SIZE
    else:
        if direction == "up":
            y -= SPACE_SIZE
        elif direction == "down":
            y += SPACE_SIZE
        elif direction == "left":
            x -= SPACE_SIZE
        elif direction == "right":
            x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    if draw == True:
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    else:
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1
        label.config(text="Score:{}".format(score))

        canvas.delete("food" + num)

        food = Food(num)

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food, draw, WASD, num)


def change_direction(new_direction, WASD):
    global direction
    global direction2

    if WASD:
        if new_direction == 'left':
            if direction2 != 'right':
                direction2 = new_direction
        elif new_direction == 'right':
            if direction2 != 'left':
                direction2 = new_direction
        elif new_direction == 'up':
            if direction2 != 'down':
                direction2 = new_direction
        elif new_direction == 'down':
            if direction2 != 'up':
                direction2 = new_direction
    else:
        if new_direction == 'left':
            if direction != 'right':
                direction = new_direction
        elif new_direction == 'right':
            if direction != 'left':
                direction = new_direction
        elif new_direction == 'up':
            if direction != 'down':
                direction = new_direction
        elif new_direction == 'down':
            if direction != 'up':
                direction = new_direction


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
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")


window = Tk()
window.title("Snake game")
window.resizable(False, False)

#score
score = 0
direction = 'down'
direction2 = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
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

window.bind('<Left>', lambda event: change_direction('left', False))
window.bind('<Right>', lambda event: change_direction('right', False))
window.bind('<Up>', lambda event: change_direction('up', False))
window.bind('<Down>', lambda event: change_direction('down', False))

window.bind('<a>', lambda event: change_direction('left', True))
window.bind('<d>', lambda event: change_direction('right', True))
window.bind('<w>', lambda event: change_direction('up', True))
window.bind('<s>', lambda event: change_direction('down', True))

# const outputs=NeuralNetwork.feedForward(offsets,this.brain);
# this.controls.forward=outputs[0];
# this.controls.left=outputs[1];
# this.controls.right=outputs[2];
# this.controls.reverse=outputs[3];

snake = Snake()
snake2 = Snake()
# snake3 = Snake()
# snake4 = Snake()
# snake5 = Snake()


food1 = Food('1')
food2 = Food('2')

next_turn(snake, food1, True, False, '1')
next_turn(snake2, food2, True, True, '2')

window.mainloop()
