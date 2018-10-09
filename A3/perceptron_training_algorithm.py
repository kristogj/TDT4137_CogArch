from random import random


class Perceptron:

    def __init__(self,num_inputs, length_input):
        self.weights = [[round(random() - 0.5,1)for _ in range(length_input)] for _ in range(num_inputs)]
        self.threshold = round(random() - 0.5,1)
        self.output = []
        self.learning_rate = 0.1

    def step(self,value):
        return 1 if value > 0 else 0

    def one_iteration(self, input, desired_out):
        out = []
        i = 0
        while i < len(input[0]):
            # Calculate output
            temp = 0
            for x in range(len(input)):
                temp += input[x][i] * self.weights[x][i]
            temp -= self.threshold
            temp = self.step(temp)
            out.append(temp)

            # Update weights
            error = desired_out[i] - temp
            for y in range(len(input)):
                delta = self.learning_rate * input[y][i] * error
                self.weights[y][i] = round(self.weights[y][i] + delta, 2)

            # Next value in input
            i += 1
        self.output = out
        return out

input = [
    [0,0,1,1],
    [0,1,0,1]]
p = Perceptron(len(input),len(input[0]))
desired_AND = [0,0,0,1]
desired_OR = [0,1,1,1]

times = 5
for x in range(times):
    res = p.one_iteration(input,desired_AND)
    print(res)

