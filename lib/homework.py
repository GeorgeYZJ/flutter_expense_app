import numpy as np

#This program would turn the sentence into acsii code so that the revolution of the string would turn into evolving of the number. 

#basic setup
target_sentence = 'To be, or not to be, that is the question.'       
popSize = 900                      # how many entities in the generation
crossoverR = 0.8                    # the pobability of mating within the generation
mutationR = 0.001                # the probability of mutation in the generation
numGen = 1000                       # limit number of generations 

# the basic information about the target sentence
target_size = len(target_sentence)
target_acsii = np.fromstring(target_sentence, dtype=np.uint8)  # convert string to number
# turning all the possible letters and punctuations into the acsii code which is number and put them into the list
letter_acs = list(range(65,91)) + list(range(97,123)) #uppercase and lowecase of the letter
#acsii number of comma, finished mark and space
letter_acs.append(44)                                  
letter_acs.append(46)
letter_acs.append(32)

# make a class to store all the methods needed for the evolving. 
class GA(object):
    def __init__(self, gene_size, gene_range, crossoverR, mutationR, popSize):

         self.gene_size = gene_size
         self.gene_range = gene_range
         self.crossoverR = crossoverR
         self.mutationR = mutationR
         self.popSize = popSize
         self.pop = np.random.choice(gene_range, size=(popSize, gene_size)).astype(np.int8) #create the poplation accroding to the population size and the target sentence length.

    def count_fitness(self):
        correct_num = (self.pop == target_acsii).sum(axis=1) # this method count how many characters matches within the target sentence 
        return correct_num

    def crossover(self,parent,pop):  # pick a random entity's gene in the pop and mate it with the parent's gene provided
        if np.random.rand() < self.crossoverR:
            ram_entity = np.random.randint(0, self.popSize, size=1) # the ramdom parent
            mate_points = np.random.randint(0, 2, size = self.gene_size).astype(np.bool) # the points of the gene that would mate with the other parent, replace the gene when true.
            parent[mate_points] = pop[ram_entity, mate_points] # mate the provided parents with the chosen one on the mate points of the gene.
        return parent
    
    def mutate(self, child):
        for point in range(self.gene_size):
            if np.random.rand() < self.mutationR:
                child[point] = np.random.choice(self.gene_range)  # replace the original gene point with the ramdom gene point 
        return child

    def select(self):
        fitness = self.count_fitness() + 1e-4 # in case of all the fitnesses are zero.  
        index = np.random.choice(np.arange(self.popSize), size=self.popSize, replace=True, p=fitness/fitness.sum()) #replace attribute is allowing or not allowing the same object shows again
        return self.pop[index]

    def expressGene(self, gene):   # translate the acsii codes into a letter
        return gene.tostring().decode('ascii')
        
    def evolve(self):
        pop = self.select()
        pop_copy = pop.copy()
        for parent in pop:  # for every parent
            child = self.crossover(parent, pop_copy)
            child = self.mutate(child)
            parent[:] = child
        self.pop = pop

if __name__ == '__main__':
    ga = GA(gene_size=target_size, gene_range=letter_acs, crossoverR=crossoverR, mutationR=mutationR, popSize=popSize)
    for generation in range(numGen):
        fitness = ga.count_fitness()
        best_Gene = ga.pop[np.argmax(fitness)]
        best_sentence = ga.expressGene(best_Gene)
        print('Gen', generation, ': ', best_sentence)
        if best_sentence == target_sentence:
            break
        ga.evolve()