import random
import statistics

import numpy as np


def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)


def func(x):
    return x * x + 2 * x - 3


def bin_to_int(str):
    num = 0
    for i in range(len(str)):
        num = num * 2
        num = num + int(str[i])
    return num


class GeneticAlgorithm:
    def __init__(self):
        self.population_count = 10
        self.cross_probability = 0.4
        self.mutation_probability = 0
        self.values = self.generate_initial_numbers()
        self.population = self.generate_population()

    def generate_initial_numbers(self):
        return [random.randint(0, 127) for _ in range(self.population_count)]

    def generate_population(self):
        result = []
        for i in range(self.population_count):
            result.append((bin(int(self.values[i]))[2:].zfill(7)))
        return result

    def evaluate_fitness(self):
        fitter = []
        for i in range(self.population_count):
            fitter.append(func(bin_to_int(self.population[i])))
        return fitter

    def roulette_selection(self):
        roulette = []
        eval = self.evaluate_fitness()
        for i in range(self.population_count):
            roulette.append((eval[i] / sum(eval) * 100))
        return roulette

    def spin_the_wheel(self):
        result = []
        roulette = self.roulette_selection()
        random_nums = [random.randint(0, 100) for _ in range(self.population_count)]
        cumsum = list(np.ndarray.tolist(np.cumsum(roulette)))
        cumsum[len(cumsum) - 1] = np.ceil(cumsum[len(cumsum) - 1])
        for i in range(self.population_count):
            for j in range(self.population_count):
                if random_nums[i] <= cumsum[j]:
                    result.append(j)
                    break
        return result

    def crossbreed(self):
        spin_result = self.spin_the_wheel()
        new_pop = []
        pairs = []
        while len(spin_result) > 1:
            rand1 = pop_random(spin_result)
            rand2 = pop_random(spin_result)
            pair = rand1, rand2
            pairs.append(pair)
        generated_crosspoints = [random.randint(0, 6) for _ in range(len(pairs))]
        for i in range(len(pairs)):
            if random.random() < self.cross_probability:
                first_part = self.population[pairs[i][0]][generated_crosspoints[i]:]
                second_part = self.population[pairs[i][1]][generated_crosspoints[i]:]
                new_pop.append(self.population[pairs[i][0]].replace(first_part, second_part))
                new_pop.append(self.population[pairs[i][1]].replace(second_part, first_part))
            else:
                new_pop.append(self.population[pairs[i][0]])
                new_pop.append(self.population[pairs[i][1]])
        self.population = new_pop

    def mutate(self):
        for i in range(self.population_count):
            if random.random() < self.mutation_probability:
                mutated_gene = random.randint(0, 6)
                if self.population[i][mutated_gene] == '1':
                    self.population[i] = self.population[i][:mutated_gene] + '0' + self.population[i][mutated_gene + 1:]
                else:
                    self.population[i] = self.population[i][:mutated_gene] + '1' + self.population[i][mutated_gene + 1:]


num_of_iterations = 100
gen = GeneticAlgorithm()
int_list = []
for k in range(num_of_iterations):
    gen.crossbreed()
    gen.mutate()

for i in range(gen.population_count):
     print(str(gen.population[i]) + " - " + str(bin_to_int(gen.population[i])))
     int_list.append(bin_to_int(gen.population[i]))

print("average value: " + str(statistics.mean(int_list)))
