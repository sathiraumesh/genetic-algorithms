from deap import base
from deap import creator
from deap import tools

import random

import matplotlib.pyplot as plt
import seaborn as sns

# problem constants:
ONE_MAX_LENGTH = 100  # length of bit string to be optimized

# Genetic Algorithm constants:
POPULATION_SIZE = 200
P_CROSSOVER = 0.9  # probability for crossover
P_MUTATION = 0.1   # probability for mutating an individual
MAX_GENERATIONS = 50


# set the random seed:
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

toolbox = base.Toolbox()

# create an operator that randomly returns 0 or 1:
toolbox.register("zeroOrOne", random.randint, 0, 1)

# define a single objective, maximizing fitness strategy:
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# create the Individual class based on list:
creator.create("Individual", list, fitness=creator.FitnessMax)
#creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMax)

# create the individual operator to fill up an Individual instance:
toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, ONE_MAX_LENGTH)

# create the population operator to generate a list of individuals:
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


# fitness calculation:
# compute the number of '1's in the individual
def oneMaxFitness(individual):
		return sum(individual),  # return a tuple


toolbox.register("evaluate", oneMaxFitness)

# genetic operators:

# Tournament selection with tournament size of 3:
toolbox.register("select", tools.selTournament, tournsize=3)

# Single-point crossover:
toolbox.register("mate", tools.cxOnePoint)

# Flip-bit mutation:
# indpb: Independent probability for each attribute to be flipped
toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/ONE_MAX_LENGTH)


# Genetic Algorithm flow:
def main():

	# create initial population (generation 0):
	population = toolbox.populationCreator(n=POPULATION_SIZE)
	generationCounter = 0

	# calculate fitness tuple for each individual in the population:
	fitnessValues = list(map(toolbox.evaluate, population))
	for individual, fitnessValue in zip(population, fitnessValues):
			print(fitnessValue)
			individual.fitness.values = fitnessValue
	
	fitnessValues = [individual.fitness.values[0] for individual in population]
				
	maxFitnessValues = []
	meanFitnessValues = []

	while max(fitnessValue) < ONE_MAX_LENGTH and generationCounter < MAX_GENERATIONS:
		generationCounter = generationCounter + 1

		offspring = toolbox.select(population, len(population))

		offspring = list(map(toolbox.clone, offspring))

		for child1, child2 in zip(offspring[::2], offspring[1::2]): 
			if random.random() < P_CROSSOVER:
				toolbox.mate(child1, child2)
				del child1.fitness.values
				del child2.fitness.values

		for mutant in offspring:
			if random.random() < P_MUTATION:
				toolbox.mutate(mutant)
				del mutant.fitness.values

		freshIndividuals = [ind for ind in offspring if not ind.fitness.valid]
		freshFitnessValues = list(map(toolbox.evaluate, freshIndividuals))

		for individual, fitnessValue in zip(freshIndividuals, freshFitnessValues):
			individual.fitness.values = fitnessValue

		population[:] = offspring

		fitnessValues = [ind.fitness.values[0] for ind in population]
		maxFitness = max(fitnessValues)
		meanFitness = sum(fitnessValues) / len(population)
		maxFitnessValues.append(maxFitness)
		meanFitnessValues.append(meanFitness)
		print("- Generation {}: Max Fitness = {}, Avg Fitness = {}".format(generationCounter, maxFitness, meanFitness))

		best_index = fitnessValues.index(max(fitnessValues))
		print("Best Individual = ", *population[best_index], "\n")

	sns.set_style("whitegrid")
	plt.plot(maxFitnessValues, color='red')
	plt.plot(meanFitnessValues, color='green')
	plt.xlabel('Generation')
	plt.ylabel('Max / Average Fitness')
	plt.title('Max and Average Fitness over Generations')
	plt.show()


if __name__ == '__main__':
		main()