import csv
import numpy as np
from random import randrange
import matplotlib.pyplot as plt

var = 82
n = 100
states = [i+1 for i in range(5)]

def print_matr(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            m[i][j] = round(m[i][j], 3)
    print(m)

def reader(var):
    m = np.full((0, len(states)), 0)
    i = len(states)
    # CSV reading and storing info int m matrix
    with open('input/Task1.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\n')
        for row in spamreader:
            if i < len(states):
                i = i + 1
                m = np.vstack([m, row])
            if row:
                if row[0] == f"#{var}":
                    i = 0
    return m.astype(float)

def mark_iter(n, m, states):
    current_s = randrange(1,6)
    states_tr = [current_s]
    n_entry=[0 for _ in range(len(states))]
    for _ in range(n-1):
        per_ver = m[current_s-1]
        n_entry[current_s-1]+=1
        next_s = np.random.choice(states, p=per_ver)
        current_s=next_s
        states_tr.append(current_s)
    return n_entry, states_tr

def marginal_probabilities(P):
    A = P.T - np.eye(len(states), dtype=float)
    A[-1] = np.full(len(states), 1)
    b = np.zeros(len(states))
    b[-1] = 1.
    p = np.linalg.solve(A, b)
    return p, [list(p) for _ in range(len(states))], list(p).count(0)!=len(p)

m = reader(var)
p, pred_mat_per, erg=marginal_probabilities(m)
# print("Предельная матрица переходов выглядит следующим образом:")
# print_matr(pred_mat_per)
print(p)

x=[i+1 for i in range(n)]
n_entry_exp=[[0 for _ in range(20)] for _ in range(len(states))]

plt.grid()
plt.ylabel("Состояния")
plt.xlabel("Переходы")
plt.yticks(np.arange(0, len(states)+1, step=1))
for i in range(20):
    myDictionary, tr = mark_iter(n, m, states)
    
    for j in range(len(states)):
        n_entry_exp[j][i] = myDictionary[j]/n

    # для частот
    print(i+1
          , "& ",myDictionary[0]/n
          , "& ",myDictionary[1]/n
          , "& ",myDictionary[2]/n
          ,"& ",myDictionary[3]/n
          ,"& ",myDictionary[4]/n, "\\\\")
    plt.plot(x, tr, 'o--',linewidth = 0.7,markeredgewidth = 0.1)

# для отклонений
for i in range(len(states)):
    print('%.3f'%np.sqrt(20*np.var(n_entry_exp[i])/(20-1)), "& ")
# plt.show()
