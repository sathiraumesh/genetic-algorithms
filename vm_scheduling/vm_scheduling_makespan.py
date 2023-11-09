from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import random
import array

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import vm_scheduling_problem as vmp
import elitism

# set the random seed for repeatable results
# RANDOM_SEED = 42
# random.seed(RANDOM_SEED)

# create the vm_scheduling make span optimization problem 
vm_list =  vm_list = [
        ("vm1", 1000, 9.9),
        ("vm2", 1000, 10),
        ("vm3", 1000, 10),
        ("vm4", 2000, 20),
        ("vm5", 2000, 20),
        ("vm6", 2000, 20),
        ("vm7", 3000, 30),
        ("vm8", 3000, 30),
        ("vm9", 3000, 30),
    ]

vmp = vmp.VMSchedulingProblem(vm_list)

# genetic algorithm constants:
POPULATION_SIZE = 500
MAX_GENERATIONS = 500
HALL_OF_FAME_SIZE = 30
P_CROSSOVER = 0.5  # probability for crossover
P_MUTATION = 0.4   # probability for mutating an individual

toolbox = base.Toolbox()

# define a single objective, minimizing fitness strategy:
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

# create the Individual class based on list of integers:
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)

# create an operator that generates randomly shuffled indices:
toolbox.register("randomOrder", np.random.randint, len(vmp.vm_list), size=len(vmp.task_list))

# create the individual creation operator to fill up an Individual instance with shuffled indices:
toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.randomOrder)

# create the population creation operator to generate a list of individuals:
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

# fitness calculation - compute the total distance of the list of cities represented by indices:
def vmMakespan(individual):
    return vmp.get_multiobjective(individual),  # return a tuple

toolbox.register("evaluate", vmMakespan)

# Genetic operators:
toolbox.register("select", tools.selTournament, tournsize=300)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=len(vm_list) - 1, indpb=1.0/100)

def main():
    # create initial population (generation 0):
    population = toolbox.populationCreator(n=POPULATION_SIZE)

    # prepare the statistics object:
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)

    # define the hall-of-fame object:
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    # perform the Genetic Algorithm flow with hof feature added:
    population, logbook = elitism.eaSimpleWithElitism(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

    # print best individual info:
    best = hof.items[0]
    
    print("-- Best Ever Individual = ", list(best[1:]))
    print("-- Best Ever Fitness = ", best.fitness.values[0])
    print(vmp.get_makespan(list(best[1:])))
    print(vmp.get_cost_fitness(list(best[1:])))
    
    with open('vm_scheduling/output.txt', 'w') as f: 
        for mapping in list(best[1:]):
            f.write(str(mapping))
            f.write('\n')
        f.close()
    
    # plot statistics:
    minFitnessValues, meanFitnessValues = logbook.select("min", "avg")
    plt.figure(2)
    sns.set_style("whitegrid")
    plt.plot(minFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Min / Average Fitness')
    plt.title('Min and Average fitness over Generations')

    # show both plots:
    plt.show()

if __name__ == "__main__":
    main()