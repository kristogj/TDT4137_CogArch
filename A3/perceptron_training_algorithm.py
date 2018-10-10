from random import random


class Perceptron:

    def __init__(self,num_inputs):
        self.weights = [random() - 0.5 for _ in range(num_inputs)]
        self.threshold = random() - 0.5
        self.output = []
        self.learning_rate = 0.1

        """
        Example values from the book
        
        self.weights = [0.3, -0.1]
        self.threshold = 0.2
        self.output = []
        self.learning_rate = 0.1
        """

    def one_epoch(self, input, desired_out):
        out = []
        i = 0
        while i < len(input[0]):
            # Calculate output
            temp_out = sum(input[x][i] * self.weights[x] for x in range(len(input))) - self.threshold
            temp_out = step(temp_out)
            out.append(temp_out)

            # Update weights
            error = desired_out[i] - temp_out
            for y in range(len(input)):
                delta = self.learning_rate * input[y][i] * error
                self.weights[y] = self.weights[y] + delta
            print("WEIGHT MID EPOCH: ",self.weights)
            # Check next
            i += 1
        self.output = out
        return out


def step(value):
    return 1 if value >= 0 else 0


# Loop testing for several Perceptrons
desired_AND = [0, 0, 0, 1]
desired_OR = [0, 1, 1, 1]
match = 0
for x in range(1000):
    input = [
        [0, 0, 1, 1],
        [0, 1, 0, 1]]
    p = Perceptron(len(input))

    res = []
    counter = 20
    while res != desired_AND and counter != 0:
        res = p.one_epoch(input, desired_AND)
        print(f"Out: {res}; Weights:{p.weights}; Thresh:{p.threshold}")
        counter -= 1
    if res == desired_AND:
        match += 1
    print()
print(f"MATCHES: {match}")





