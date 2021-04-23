from simanneal import Annealer
import random
import csv
from collections import defaultdict
class ClinicFinder(Annealer):
	def __init__(self, state, distance_matrix,population,risk,clinic_amount):
		self.distance_matrix = distance_matrix
		self.population = population
		self.risk = risk
		self.clinic_amount = clinic_amount
		super(ClinicFinder, self).__init__(state)

	def move(self):
		a = random.randint(0, self.clinic_amount - 1)
		b = random.randint(self.clinic_amount, len(self.state) - 1)
		self.state[a], self.state[b] = self.state[b], self.state[a]


	def energy(self):
		e = 0
		for i in range(self.clinic_amount,len(self.state)):
			min = 1000000000.0
			for j in range(self.clinic_amount):
				if self.distance_matrix[self.state[i]][self.state[j]] >  min:
					min = self.distance_matrix[self.state[i]][self.state[j]]
			e += min/(self.population[self.state[i]] * self.risk[self.state[i]])
		return e




if __name__ == '__main__':
	file = open('monroe_tracts.csv','r')
	reader = csv.DictReader(file)
	line_count = 0
	risk = {}
	population = {}
	tracts = []
	for row in reader:
		if line_count != 0:
			risk[row['tract']] =  float(row['ccvi'])
			population[row['tract']] =  float(row['pop_est'])
			tracts.append(row['tract'])
		line_count+=1
	file2 = open('monroe_tract_dists.csv','r')
	reader2 = csv.DictReader(file2)
	distance_matrix = defaultdict(dict)
	for row in reader2:
		if line_count != 0:
			distance_matrix[row['tract1']][row['tract2']] = float(row['mi_to_tract'])
		line_count += 1
	random.shuffle(tracts)

	CF = ClinicFinder(tracts,distance_matrix,population,risk,30)
	CF.Tmax = 50000.0
	states, utility = CF.anneal()

	print(states)
	print(utility)
