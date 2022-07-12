# CNN learns Snake
AI learns how to play snake!

# Project overview
a) create game of snake that can be simulated with over 1000 snakes, and keeps track of fitness for each one
b) implement NEAT algorithm

# Snake Game
The base code is taken from a tutorial from bro code - https://www.youtube.com/watch?v=bfRwxS5d0SI&t=368s&ab_channel=BroCode
After this we have to implement: initialize funciton to make x amount of snakes, only draw highiest fitness, check collisions for each snake, and alot of bug fixes

# NEAT
NEAT stands for Neuro-Evolution of Augmenting Topoligies, which was researched in this paper by Dr. Stanley, from MIT - https://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf

Essentially you define a pre-existing input and output layer, and it randomly 'augments the topology' or in simpler terms - changes the structure of the neural network by adding random neurons in hidden layers, and uses a genetic algorithm to find the winners of each generation until it converges on the best solution.
   
# Visualizaton
 
![Visualization of neural net](https://github.com/24parida/CNN-learns-Snake/blob/main/net.png?raw=true)

# End result

Fitness of 105, or 20 apples.

# Opportunities to expand

expand inputs, the model was only trained on head position and food position, meaning it would hit it's own body

would run into a problem where max_recursion was met after a certain amount of calls, meaning that it would be physicaly impossible to get a score of over 200, maybe switch from tkinter to pygame where recursion wouldn't be neccesary

more epochs
