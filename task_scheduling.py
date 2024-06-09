import random
SIZE = 100
GENS = 300
M_RATE = 0.11

test_cases = [
    {
        'tasks': [
        {'id': 1, 'skills': 'A', 'time': 3, 'dependencies': []},
        {'id': 2, 'skills': 'C', 'time': 1, 'dependencies': [1]},
        {'id': 3, 'skills': 'B', 'time': 2, 'dependencies': [1]},
        {'id': 4, 'skills': 'A', 'time': 5, 'dependencies': [2]},
        {'id': 5, 'skills': 'B', 'time': 4, 'dependencies': [2, 3]},
        {'id': 6, 'skills': 'B', 'time': 7, 'dependencies': [4]},
        ],
        'workers':[
            {'id': 1, 'skills': ['A', 'B']},
            {'id': 2, 'skills': ['A']},
            {'id': 3, 'skills': ['B', 'C']},
            {'id': 4, 'skills': ['C']},
        ]
    },
    {
        'tasks': [
        {'id': 1, 'skills': 'A', 'time': 2, 'dependencies': []},
        {'id': 2, 'skills': 'B', 'time': 3, 'dependencies': [1]},
        {'id': 3, 'skills': 'A', 'time': 4, 'dependencies': [2]},
        {'id': 4, 'skills': 'C', 'time': 5, 'dependencies': [3]},
        {'id': 5, 'skills': 'B', 'time': 2, 'dependencies': [1]},
        {'id': 6, 'skills': 'C', 'time': 3, 'dependencies': [5]},
        ],

        'workers': [
            {'id': 1, 'skills': ['A', 'B']},
            {'id': 2, 'skills': ['A']},
            {'id': 3, 'skills': ['B', 'C']},
            {'id': 4, 'skills': ['C']},
        ]
    },
    {
        'tasks': [
        {'id': 1, 'skills': 'A', 'time': 1, 'dependencies': []},
        {'id': 2, 'skills': 'B', 'time': 4, 'dependencies': [1]},
        {'id': 3, 'skills': 'C', 'time': 3, 'dependencies': [2]},
        {'id': 4, 'skills': 'A', 'time': 2, 'dependencies': [3]},
        {'id': 5, 'skills': 'B', 'time': 1, 'dependencies': [4]},
        {'id': 6, 'skills': 'C', 'time': 6, 'dependencies': [5]},
        ],

        'workers': [
            {'id': 1, 'skills': ['A', 'B']},
            {'id': 2, 'skills': ['A']},
            {'id': 3, 'skills': ['B', 'C']},
            {'id': 4, 'skills': ['C']},
        ]
    },
]

def create_chromosome(tasks, workers):
    return [random.choice(workers) for task in tasks]

def selection(population):
    #Here we are sorting the population according to the fitness level and returns the best 2 chromosomes
    population.sort(key=lambda x: x['fitness'])
    return population[:2]

def create_population(cur_population, tasks, workers):
    #This function creates a population from an existing one
    parents = selection(cur_population)
    new_population = []
    while len(new_population) < SIZE:
        parent1, parent2 = parents[0]['chromosome'], parents[1]['chromosome']
        new_chromosome1, new_chromosome2 = crossover(parent1, parent2)
        new_population.append({'chromosome': mutate(new_chromosome1, workers), 'fitness': 0})
        new_population.append({'chromosome': mutate(new_chromosome2, workers), 'fitness': 0})
    for chromosome in new_population:
        chromosome['fitness'] = fitness(chromosome['chromosome'], tasks, workers)
    return new_population

def mutate(chromosome, workers):
    #This function generates a random number between 0 and 1 and if it's less than the mutation rate it will apply mutation to the chromosome
    random_num = random.random()
    if random_num < M_RATE:
        mutate_index = random.randint(0, len(chromosome) - 1)
        chromosome[mutate_index] = random.choice(workers)
    return chromosome


def crossover(chromosome1, chromosome2):
    #This function takes 2 chromosomes and apply crossover at a random point and returns the new chromosomes
    crossover_point = random.randint(1, len(chromosome1) - 1)
    new_chromosome1 = chromosome1[:crossover_point] + chromosome2[crossover_point:]
    new_chromosome2 = chromosome2[:crossover_point] + chromosome1[crossover_point:]
    return new_chromosome1, new_chromosome2


def fitness(chromosome, tasks, workers):
    #This function iterates over the chromosome and checks if it's valid 
    #(all tasks assigned to workers who have the skills and the dependencies) and it returns the time needed to finish all tasks.

    end = {task['id']: 0 for task in tasks}
    assignments = {worker['id']: [] for worker in workers}
    for task, worker in zip(tasks, chromosome):
        max_dependencies_time = max([end[dependencies] for dependencies in task['dependencies']], default=0)
        start_time = max(max_dependencies_time, sum(assignments[worker['id']]))
        # Check if the worker doesn't have the skills (invalid chromosome)
        if task['skills'] not in worker['skills']:
            return 99999
        assignments[worker['id']].append(task['time'])
        end[task['id']] = start_time + task['time']
    
    return max(sum(times) for times in assignments.values())


if __name__ == "__main__":
    for i, case in enumerate(test_cases):
        print()
        tasks = case['tasks']
        workers = case['workers']
        #Creating the initial_population
        initial_population = [{'chromosome': create_chromosome(tasks, workers), 'fitness': 0} for i in range(SIZE)]
        #Calculating the fitness for the initial_population
        for chromosome in initial_population:
            chromosome['fitness'] = fitness(chromosome['chromosome'], tasks, workers)

        cur_population = initial_population
        #A loop for creating generations
        for _ in range(GENS):
            cur_population = create_population(cur_population, tasks, workers)

        best_schedule = min(cur_population, key=lambda x: x['fitness'])
        print(f'Test case{i + 1}: ')
        for task, worker in zip(tasks, best_schedule['chromosome']):
            print(f'Task {task["id"]} by Worker {worker["id"]}')
        print(f'Total time required: {best_schedule['fitness']}')
