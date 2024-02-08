import random
import matplotlib.pyplot as plt
import numpy as np

# Global parameters for bin-packing
population_size = 30
num_items = 0
num_bins = 0
bins_capacity = []
items_weights = []
elite_count = 3
mutation_rate = 0.2

# Initialize population and fitness list
population = []
fitness_list = [0] * population_size

# Read data from a text file
def read_data_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def parse_problem_instances(text):
    instances = []
    lines = text.strip().split('\n')
    i = 0
    while i < len(lines):
        name = lines[i].strip().strip("'")
        i += 1
        m = int(lines[i].strip())
        i += 1
        capacity = int(lines[i].strip())
        i += 1
        items = []
        for _ in range(m):
            weight, count = map(int, lines[i].strip().split())
            items.append((weight, count))
            i += 1
        instances.append({'name': name, 'capacity': capacity, 'items': items})
    return instances


def parse_problem_instances_from_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        return parse_problem_instances(text)

def parse_bin_packing_data(problem_instances):
    global num_items, num_bins, bins_capacity, items_weights

    # Assume the first problem instance in the list
    first_instance = problem_instances[0]

    num_items = len(first_instance['items'])
    num_bins = first_instance['capacity']
    bins_capacity = [first_instance['capacity']]
    items_weights = [weight for weight, count in first_instance['items']]

    print("num_items:", num_items)
    print("num_bins:", num_bins)
    print("bins_capacity:", bins_capacity)
    print("items_weights:", items_weights)

# Initialize population for bin-packing
def initialize_population():
    population = []
    for _ in range(population_size):
        bin_assignment = [random.randint(0, num_bins - 1) for _ in range(num_items)]
        population.append(bin_assignment)
    return population

def calc_fitness(bin_assignment):
    bins_load = [0] * num_bins
    excess_load = 0

    for i, bin_index in enumerate(bin_assignment):
        bins_load[bin_index] += items_weights[i]

    for bin_index, load in enumerate(bins_load):
        if bin_index < len(bins_capacity):
            excess_load += max(0, load - bins_capacity[bin_index])

    return num_bins - excess_load

# Mutate for bin-packing
def mutate(bin_assignment):
    mutated_assignment = bin_assignment.copy()
    item_index = random.randint(0, num_items - 1)
    mutated_assignment[item_index] = random.randint(0, num_bins - 1)
    return mutated_assignment

# Crossover for bin-packing
def crossover(parent1, parent2):
    
    crossover_point = random.randrange(29)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return [child1, child2]

# Fitness sorting for bin-packing
def fitness_sort(population):
    mockpop = list(enumerate(fitness_list))
    mockpop.sort(key=lambda e: e[1])
    return mockpop

# Generate new population for bin-packing
def generate_new_pop(population):
    global fitness_list 
    new_population = []
    elite_strings = fitness_sort(population)[-elite_count:]

    for i in range(elite_count):
        elite_strings[i] = population[elite_strings[i][0]]

    for i in range(elite_count):
        new_population.extend(crossover(elite_strings[i], elite_strings[(i + 1) % elite_count]))
        new_population.extend(crossover(elite_strings[i], elite_strings[(i + 2) % elite_count]))

    for i in range(elite_count, population_size):
        new_population.append(mutate(random.choice(population)))

    calculate_fitnesses(new_population)
    return new_population

# Calculate fitness for bin-packing population
def calculate_fitnesses(population):
    for i in range(population_size):
        fitness_list[i] = calc_fitness(population[i])

# Visualization
def visualize_results(data):
    plt.plot(data['generation'], data['average'], label='Average Fitness')
    plt.xlabel('Generations')
    plt.ylabel('Average Fitness')
    plt.title('Genetic Algorithm - Bin Packing Problem')
    plt.legend()
    plt.savefig('bin_packing_results', bbox_inches='tight')
    plt.show()

# Main function
if __name__ == "__main__":
    file_path = "Binpacking.txt" 
    problem_instances = parse_problem_instances_from_file(file_path)

    # Parse data for the bin-packing problem
    parse_bin_packing_data(problem_instances)

    # Initialize population
    population = initialize_population()

    # Run the genetic algorithm with the new problem instance data
    averages_filename = "Averages_bin_packing.csv"
    with open(averages_filename, "w") as averages_file:
        averages_file.write("generation,average,bins_used\n")

        generations = 0
        metrics = [generations, sum(fitness_list) / population_size]
        averages_file.write("{},{},{}\n".format(metrics[0], metrics[1], num_bins))
        print("generation:\t{}".format(metrics[0]))
        print("fitness average:\t{}".format(metrics[1]))

        while True:
            population = generate_new_pop(population)
            generations += 1
            metrics = [generations, sum(fitness_list) / population_size]
            averages_file.write("{},{},{}\n".format(metrics[0], metrics[1], num_bins))
            print("generation:\t{}".format(metrics[0]))
            print("fitness average:\t{}".format(metrics[1]))

            champion = fitness_sort(population)[-1]
           # Check if a solution is found
            if champion[1] == num_bins:
                bins_used = set([champion[0]])
                print("Solution found! Bins used:", len(bins_used))
                break
            else:
                print("Solution not found yet!")

    # Visualization
    data = np.genfromtxt(averages_filename, delimiter=',', names=True)
    visualize_results(data)
