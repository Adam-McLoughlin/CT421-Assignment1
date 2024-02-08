import random
import matplotlib.pyplot as plt
import numpy as np

# Global parameters
population_size = 30
string_length = 30
elite_count = 3
mutation_rate = 0.1

# New parameter for the target string
target_string = '110110101001101010100100011111'

# Initialize population and fitness list
population = []
fitness_list = [0] * population_size

def calculate_fitnesses(strings):
    for i in range(population_size):
        fitness_list[i] = calc_fitness(strings[i])

def calc_fitness(string):
    # Fitness is the number of matching values with the target string
    return sum(1 for a, b in zip(string, target_string) if a == b)

def mutate(string):
    for i in range(string_length):
        if random.random() < mutation_rate:
            string = string[:i] + ('0' if string[i] == '1' else '1') + string[(i + 1):]
    return string

def crossover(parent1, parent2):
    crossover_point = random.randrange(1, string_length - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return [child1, child2]

def fitness_sort(strings):
    mockpop = list(enumerate(fitness_list))
    mockpop.sort(key=lambda e: e[1])
    return mockpop

def generate_new_pop(strings):
    new_population = []
    elite_strings = fitness_sort(strings)[-elite_count:]
    for i in range(elite_count):
        elite_strings[i] = strings[elite_strings[i][0]]
    for i in range(elite_count):
        new_population.extend(crossover(elite_strings[i], elite_strings[(i + 1) % elite_count]))
        new_population.extend(crossover(elite_strings[i], elite_strings[(i + 2) % elite_count]))
    for i in range(elite_count, population_size):
        new_population.append(mutate(random.choice(strings)))
    calculate_fitnesses(new_population)
    return new_population

# Generate initial population
for i in range(population_size):
    bit_str = ''.join(str(random.randint(0, 1)) for _ in range(string_length))
    population.append(bit_str)

calculate_fitnesses(population)

# File for saving average fitness
averages_filename = "Averages_Target.csv"
with open(averages_filename, "w") as averages_file:
    averages_file.write("generation,average\n")

    generations = 0
    metrics = [generations, sum(fitness_list) / population_size]
    averages_file.write("{},{}\n".format(metrics[0], metrics[1]))
    print("generation:\t{}".format(metrics[0]))
    print("fitness average:\t{}".format(metrics[1]))

    while True:
        population = generate_new_pop(population)
        generations += 1
        metrics = [generations, sum(fitness_list) / population_size]
        averages_file.write("{},{}\n".format(metrics[0], metrics[1]))
        print("generation:\t{}".format(metrics[0]))
        print("fitness average:\t{}".format(metrics[1]))

        champion = fitness_sort(population)[-1]
        if champion[1] == string_length:  
            print("Target string has been found: Index is: {}, String code: {}".format(champion[0], population[champion[0]]))
            break
        else:
            print("Target string not found yet!")

# Visualization
data = np.genfromtxt(averages_filename, delimiter=',', names=True)
plt.plot(data['generation'], data['average'], label='Average Fitness')
plt.xlabel('Generations')
plt.ylabel('Average Fitness')
plt.title('Genetic Algorithm - Target String Evolution')
plt.legend()
plt.savefig('averages_results_target', bbox_inches='tight')
plt.show()
