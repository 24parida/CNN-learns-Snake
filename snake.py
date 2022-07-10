# # ************************************
# # Python Snake
# # ************************************
# import random
# from tkinter import *
#
# import numpy as np
# from keras.layers import Dense, Activation
# from keras.models import Sequential
#
# GAME_WIDTH = 700
# GAME_HEIGHT = GAME_WIDTH
# SPEED = 600
# SPACE_SIZE = 140
# BODY_PARTS = 3
# SNAKE_COLOR = "#00FF00"
# FOOD_COLOR = "#FF0000"
# BACKGROUND_COLOR = "#000000"
# BACKGROUND_COLOR1 = "white"
#
# # machine learning
# current_pool = []
# fitness = []
# total_models = 20
#
# # generation
# lives = []
# snakes = []
# scores = []
# food_s = []
# directions = []
# highest_score = 0
# moves = [20] * total_models
# positions = [0] * (int((GAME_WIDTH/SPACE_SIZE) ** 2) + 3)
#
#
# generation = 1
# highest_fitness = 0
# hf_index = 0
# best_weights = []
#
# INPUT_LAYER = (int((GAME_WIDTH/SPACE_SIZE) ** 2) + 3)
# SECOND_LAYER = 50
# OUTPUT_LAYER = 4
#
#
# class Food:
#     def __init__(self, num, draw):
#
#         x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
#         y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
#
#         self.coordinates = [x, y]
#         if draw:
#             canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food" + str(num))
#         else:
#             canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, tag="food" + str(num))
#
#     def restart(self, num, draw):
#
#         self.coordinates.clear()
#
#         x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
#         y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
#         self.coordinates = [x, y]
#
#         if draw:
#             canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food" + str(num))
#         else:
#             canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, tag="food" + str(num))
#
#     def clean(self, num):
#         x = self.coordinates[0]
#         y = self.coordinates[1]
#         canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = BACKGROUND_COLOR1, tag="food" + str(num))
#
#
# class Snake:
#
#     def __init__(self, num, draw):
#         self.body_size = BODY_PARTS
#         self.coordinates = []
#         self.squares = []
#
#         for i in range(0, BODY_PARTS):
#             self.coordinates.append([0, 0])
#
#         for x, y in self.coordinates:
#             if draw:
#                 square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake" + str(num))
#             else:
#                 square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, tag="snake" + str(num))
#             self.squares.append(square)
#
#     def restart(self, num, draw):
#         global BODY_PARTS
#         directions[num] = 'down'
#
#         self.body_size = BODY_PARTS
#         self.coordinates.clear()
#         self.squares.clear()
#
#         for i in range(0, BODY_PARTS):
#             self.coordinates.append([0, 0])
#
#         for x, y in self.coordinates:
#             if draw:
#                 square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake" + str(num))
#             else:
#                 square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, tag="snake" + str(num))
#             self.squares.append(square)
#
#     def clean(self):
#         for x, y in self.coordinates:
#             canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BACKGROUND_COLOR1)
#
#
# def save_pool():
#     for snake in range(total_models):
#         current_pool[snake].save_weights("SavedModels/models_new" + str(snake) + ".keras")
#     print("saved all models")
#
#
# def create_model():
#     model = Sequential()
#     model.add(Dense(INPUT_LAYER, input_shape=(INPUT_LAYER,)))
#     model.add(Activation('relu'))
#     model.add(Dense(SECOND_LAYER, input_shape=(INPUT_LAYER,)))
#     model.add(Activation('relu'))
#     model.add(Dense(OUTPUT_LAYER, input_shape=(SECOND_LAYER,)))
#     model.add(Activation('sigmoid'))
#
#     model.compile(loss='mse', optimizer='adam')
#
#     return model
#
#
# def predict_action(model_num):
#     global current_pool
#     global positions
#
#     for i in range(len(positions)):
#         positions[i] = 0
#
#     for x, y in snakes[model_num].coordinates:
#         rx = x / 50
#         ry = y / 50
#         try:
#             if x == snakes[model_num].coordinates[0][0] and y == snakes[model_num].coordinates[0][1]:
#                 positions[int((5 * rx) + ry)] = 10
#             else:
#                 positions[int((5 * rx) + ry)] = 5
#         except IndexError:
#             print("fucked up Index")
#             print("rx: " + str(rx) + " ry: " + str(ry))
#
#     x = food_s[model_num].coordinates[0]
#     y = food_s[model_num].coordinates[1]
#     rx = x / 50
#     ry = y / 50
#
#     if directions[model_num] == 'down':
#         positions[(int(GAME_WIDTH/SPACE_SIZE) ** 2)] = 2
#     elif directions[model_num] == 'up':
#         positions[(int(GAME_WIDTH/SPACE_SIZE) ** 2)] = 4
#     elif directions[model_num] == 'right':
#         positions[(int(GAME_WIDTH/SPACE_SIZE) ** 2)] = 6
#     elif directions[model_num] == 'left':
#         positions[(int(GAME_WIDTH/SPACE_SIZE) ** 2)] = 8
#
#     positions[int(GAME_WIDTH/SPACE_SIZE) + 1] = int(rx)
#     positions[int(GAME_WIDTH/SPACE_SIZE) + 2] = int(ry)
#
#     neural_input = np.asarray(positions)
#     neural_input = np.atleast_2d(neural_input)
#
#     output_prob = current_pool[model_num].predict(neural_input)
#
#     final_prob = [0, 0, 0, 0]
#     final_prob[0] = output_prob[0][0]
#     final_prob[1] = output_prob[0][1]
#     final_prob[2] = output_prob[0][2]
#     final_prob[3] = output_prob[0][3]
#
#     return final_prob
#
#
# def model_crossover(parent1, parent2):
#     global current_pool
#
#     weight1 = current_pool[parent1].get_weights()
#     weight2 = current_pool[parent2].get_weights()
#
#     new_weight1 = weight1
#     new_weight2 = weight2
#
#     gene = random.randint(0, len(new_weight1) - 1)
#
#     new_weight1[gene] = weight2[gene]
#     new_weight2[gene] = weight1[gene]
#
#     return np.asarray([new_weight1, new_weight2])
#
#
# def model_mutate(weights):
#     for i in range(len(weights)):
#         for j in range(len(weights[i])):
#             if random.uniform(0, 1) > 0.85:
#                 change = random.uniform(-0.5, 0.5)
#                 weights[i][j] += change
#
#     return weights
#
#
# def new_generation():
#     global current_pool
#     global scores
#     global moves
#     global generation
#     global highest_fitness
#     global best_weights
#
#     new_weights = []
#     total_fitness = 0
#     updated = False
#
#     #calculate fitness
#     for score in range(len(scores)):
#         fitness[score] = (8 * scores[score])
#
#     # get total fitness / highest fitness
#
#     for select in range(total_models):
#         total_fitness += fitness[select]
#
#         if fitness[select] > highest_fitness:
#             updated = True
#             highest_fitness = fitness[select]
#             best_weights = current_pool[select].get_weights()
#
#     # get top two parents
#     parent1 = random.randint(0, total_models - 1)
#     parent2 = random.randint(0, total_models - 1)
#
#     for i in range(total_models):
#         if fitness[i] >= fitness[parent1]:
#             parent1 = i
#
#     for j in range(total_models):
#         if j != parent1:
#             if fitness[j] >= fitness[parent2]:
#                 parent2 = j
#     print("best parent: " + str(parent1) + " second best: " + str(parent2))
#
#     # getting crossover weights
#     for select in range(total_models // 2):
#         cross_over_weights = model_crossover(parent1, parent2)
#         # if not updated:
#         #     print("not updated")
#         #     cross_over_weights[1] = best_weights
#         mutated1 = model_mutate(cross_over_weights[0])
#         mutated2 = model_mutate(cross_over_weights[1])
#
#         new_weights.append(mutated1)
#         new_weights.append(mutated2)
#
#     for select in range(len(new_weights)):
#         current_pool[select].set_weights(new_weights[select])
#
#     for fit in range(len(fitness)):
#         fitness[fit] = 0
#     # save_pool()
#
#     generation += 1
#     return
#
#
# def initialize_models():
#     global total_models
#     for i in range(total_models):
#         model = create_model()
#         current_pool.append(model)
#
#
# def initialize_game():
#     global lives
#     global snakes
#     global food_s
#     global hf_index
#     global scores
#     global fitness
#     global highest_fitness
#     global highest_score
#
#     hf_index = 0
#     highest_fitness = 0
#     highest_score = 0
#
#     for i in range(total_models):
#         lives.append(True)
#         if i == hf_index:
#             snake = Snake(i, True)
#             food = Food(i, True)
#         else:
#             snake = Snake(i, True)
#             food = Food(i, True)
#         fitness.append(0)
#         snakes.append(snake)
#         food_s.append(food)
#         scores.append(0)
#         directions.append('down')
#     initialize_models()
#
#
# def next_turns():
#     global hf_index
#     global total_models
#
#     for i in range(total_models):
#         if i == hf_index:
#             next_turn(snakes[i], food_s[i], True, i)
#         else:
#             next_turn(snakes[i], food_s[i], True, i)
#
#
# def next_turn(snake, food, draw, num):
#     global lives
#     global highest_score
#     global hf_index
#     global moves
#     global scores
#
#     if lives[num]:
#         try:
#             moves[num] -= 1
#         except:
#             print("moves " + str(moves))
#             print("moves type " + str(type(moves)))
#             print("moves[num] " + str(moves[num]))
#
#         x, y = snake.coordinates[0]
#         action = predict_action(num)
#
#         direction_temp = 0
#         for direction in range(len(action)):
#             if action[direction] > action[direction_temp]:
#                 direction_temp = direction
#
#         if direction_temp == 0:
#             change_direction('down', num)
#         elif direction_temp == 1:
#             change_direction('up', num)
#         elif direction_temp == 2:
#             change_direction('right', num)
#         elif direction_temp == 3:
#             change_direction('left', num)
#
#         if directions[num] == "up":
#             y -= SPACE_SIZE
#         elif directions[num] == "down":
#             y += SPACE_SIZE
#         elif directions[num] == "left":
#             x -= SPACE_SIZE
#         elif directions[num] == "right":
#             x += SPACE_SIZE
#
#         snake.coordinates.insert(0, (x, y))
#         if draw:
#             square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
#         else:
#             square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = BACKGROUND_COLOR1)
#
#         snake.squares.insert(0, square)
#         if x == food.coordinates[0] and y == food.coordinates[1]:
#             scores[num] += 1
#             moves[num] += 8
#             if scores[num] >= highest_score and lives[num]:
#                 highest_score = scores[num]
#
#             label.config(text="High Score:{}".format(highest_score))
#
#             canvas.delete("food" + str(num))
#             food.restart(num, draw)
#
#         else:
#
#             del snake.coordinates[-1]
#
#             canvas.delete(snake.squares[-1])
#
#             del snake.squares[-1]
#         if check_collisions(snake) or moves[num] <= 0:
#             lives[num] = False
#             snakes_still_alive = False
#             # updated = False
#             # # if num == hf_index:
#             # #     for i in range(total_models):
#             # #         if lives[i] and not updated:
#             # #             hf_index = i
#             # #             updated = True
#             # # print("hf index + " + str(hf_index))
#             for life in lives:
#                 if life:
#                     snakes_still_alive = True
#             if snakes_still_alive:
#                 game_over_bnr(num)
#             else:
#                 game_over_bnr(num)
#                 game_over()
#
#     window.after(SPEED, next_turn, snake, food, draw, num)
#
#
# def change_direction(new_direction, num):
#     global directions
#
#     if new_direction == 'left':
#         if directions[num] != 'right':
#             directions[num] = new_direction
#     elif new_direction == 'right':
#         if directions[num] != 'left':
#             directions[num] = new_direction
#     elif new_direction == 'up':
#         if directions[num] != 'down':
#             directions[num] = new_direction
#     elif new_direction == 'down':
#         if directions[num] != 'up':
#             directions[num] = new_direction
#
#
# def check_collisions(snake):
#     x, y = snake.coordinates[0]
#
#     if x < 0 or x >= GAME_WIDTH:
#         return True
#     elif y < 0 or y >= GAME_HEIGHT:
#         return True
#
#     for body_part in snake.coordinates[1:]:
#         if x == body_part[0] and y == body_part[1]:
#             return True
#
#     return False
#
#
# def game_over():
#     print("game over")
#     global lives
#     global hf_index
#     global generation
#     global highest_score
#     global moves
#
#     generation += 1
#     highest_score = 0
#     hf_index = 0
#     label.config(text="High Score:{}".format(highest_score))
#     label2.config(text="Generation:{}".format(generation))
#
#     new_generation()
#
#     for i in range(total_models):
#         lives[i] = True
#         scores[i] = 0
#         moves[i] = 20
#         directions[i] = 'down'
#     for i in range(total_models):
#
#         if i == hf_index:
#             food_s[i].restart(i, True)
#             snakes[i].restart(i, True)
#         else:
#             food_s[i].restart(i, True)
#             snakes[i].restart(i, True)
#
#
# def game_over_bnr(num):
#     global hf_index
#
#     print("direction fucked up: " + str(directions[num]) + " num: " + str(num))
#
#     canvas.delete("snake" + str(num))
#     canvas.delete("food" + str(num))
#     snakes[num].clean()
#     food_s[num].clean(num)
#
#
# window = Tk()
# window.title("Snake game")
# window.resizable(False, False)
#
# label = Label(window, text="High Score:{}".format(highest_score), font=('consolas', 20))
# label2 = Label(window, text="Generation:{}".format(generation), font=('consolas', 20))
#
# label.pack()
# label2.pack()
#
# canvas = Canvas(window, bg=BACKGROUND_COLOR1, height=GAME_HEIGHT, width=GAME_WIDTH)
# canvas.pack()
#
# window.update()
#
# window_width = window.winfo_width()
# window_height = window.winfo_height()
# screen_width = window.winfo_screenwidth()
# screen_height = window.winfo_screenheight()
#
# x = int((screen_width / 2) - (window_width / 2))
# y = int((screen_height / 2) - (window_height / 2))
#
# window.geometry(f"{window_width}x{window_height}+{x}+{y}")
#
# # window.bind('<Left>', lambda event: change_direction('left', 0))
# # window.bind('<Right>', lambda event: change_direction('right', 0))
# # window.bind('<Up>', lambda event: change_direction('up', 0))
# # window.bind('<Down>', lambda event: change_direction('down', 0))
# #
# # initialize_game()
# # next_turns()
# # window.mainloop()
# print("ran wrong snake")