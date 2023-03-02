import csv
import numpy as np
from random import randrange
import matplotlib.pyplot as plt


def mark_iter(n, m, states, print):
    states_dict = {}
    states_tr = []
    s = randrange(5)
    per_ver = m[s]
    for iter in range(1, n+1):
        if print:
            print(f"After iteration №{iter-1} state is {states[s-1]}.")
        x = np.random.random(1)[0]
        finder = 0.
        next_state = 0
        while finder < x:
            finder = finder + per_ver[next_state]
            next_state = next_state + 1
        if states[next_state-1] in states_dict.keys():
            states_dict[states[next_state-1]] = states_dict[states[next_state-1]] + 1
        else:
            states_dict[states[s-1]] = 1
        states_tr.append(next_state-1)

        if print:
            print(f"Transition if {states[s-1]}{states[next_state-1]} with probability of {per_ver[next_state-1]}")
        s = next_state
        per_ver = m[s-1]
    if print:
        print(f"After iteration №{iter} state is {states[s - 1]}.")
    return dict(sorted(states_dict.items())), states_tr


# Put variant
var = 25
n = 100

# States and transitions
states = ["A", "B", "C", "D", "E"]
transitionName = [["AA", "AB", "AC", "AD", "AE"],
                  ["BA", "BB", "BC", "BD", "BE"],
                  ["CA", "CB", "CC", "CD", "CE"],
                  ["DA", "DB", "DC", "DD", "DE"],
                  ["EA", "EB", "EC", "ED", "EE"]]

# Transition matrix
m = np.full((0, 5), 0)
i = 5

# CSV reading and storing info int m matrix
with open('input/Task1.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='\n')
    for row in spamreader:
        if i < 5:
            i = i + 1
            m = np.vstack([m, row])
        if row:
            if row[0] == f"#{var}":
                i = 0
m = m.astype(float)

# Approval of ergodicity
A = m.T - np.eye(5, dtype=float)
A[4] = np.full(5, 1)

b = np.zeros(5)
b[4] = 1.

p = np.linalg.solve(A, b)
print(f"Конечные вероятности не нулевые, а равны {p}. Цепь маркова эргодична.\n")

# Предельная матрица переходов
pred_mat_per = np.full((0, 5), 0)
for i in range(0, 5):
    pred_mat_per = np.vstack([pred_mat_per, p])

print("Предельная матрица переходов выглядит следующим образом:")
print(pred_mat_per)

f = open('output/table.csv', 'w', encoding="utf-8")
f.write(f"{p[0]}, {p[1]}, {p[2]}, {p[3]}, {p[4]}\n")


# Markov iteration
x=[i+1 for i in range(100)]
for i in range(0, 20):
    # myDictionary,  =
    myDictionary, pl = mark_iter(n, m, states, False)
    f.write(f"{myDictionary['A']}, {myDictionary['B']}, {myDictionary['C']}, {myDictionary['D']}, {myDictionary['E']}\n")
    plt.plot(x, pl)
    # print(myDictionary)
    # plt.bar(myDictionary.keys(), myDictionary.values(), 1, color='g')
    # plt.show()

plt.show()
f.close()









