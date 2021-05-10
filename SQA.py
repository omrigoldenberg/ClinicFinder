import numpy as np
import csv
from pyqubo import Array, Add
import openjij as oj
import time
#PLEASE NOTE THE REQUIRED PACKAGES ABOVE TO RUN THIS PROGRAM

ccvi_dict = {}

with open('monroe_tracts.csv', mode='r') as inp:
    reader1 = csv.reader(inp)
    next(reader1)
    ccvi_dict = {rows[0]:rows[1] for rows in reader1}

#Number of clinics N
N = 65
n = len(ccvi_dict)

W = np.zeros((n,n))
with open('monroe_tract_dists.csv', mode='r') as inp:
    reader2 = csv.reader(inp)
    next(reader2)
    for row in reader2:
        t1_index = list(ccvi_dict.keys()).index(row[0])
        t2_index = list(ccvi_dict.keys()).index(row[2])
        edge_weight = 1/((float(ccvi_dict[row[0]])-float(ccvi_dict[row[2]]))*float(row[1]))
        W[t1_index, t2_index] = edge_weight

#Array of Tract Spins
T = Array.create('T', shape=n, vartype='SPIN')

#Sum of all Spins
sumT = T[0]
for i in range(1, len(T)):
    sumT = Add(sumT, T[i])

#Constraint Function
conFun = (sumT - (N - (n - N)))**2

#Objective Function
objFun = 0
for i in range(n):
    for j in range(n):
        objFun += W[i][j]*T[i]*T[j]

#Hamiltonian
H = objFun + conFun

#Create Ising Model
model = H.compile()
linear, quadratic, offset = model.to_ising()

#print(linear)
#print('\n')
#print(quadratic)

#OpenJij Simulated Quantum Annealing

#Spin reactions
h = linear

#Pair-wise couplings
J = quadratic

start_time = time.time()
# Simulated quantum annealing (quantum simulation) 8000 times
response = oj.SQASampler(iteration=8000).sample_ising(h, J)
# show the lowest energy solution in 8000 times
#print(time.time() - start_time)
print('\n')

#print("SQA results: \n", response.min_samples)

print('\n')

#Report which tracts get clinics
print('Tracts to be assigned clinics:')
for key in response.min_samples:
    if response.min_samples[key] == 1:
        ind = int(str(key)[2:-1])
        print(list(ccvi_dict.keys())[ind])
    
