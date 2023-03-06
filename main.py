import csv
import numpy as np
from random import randrange
import matplotlib.pyplot as plt
from collections import Counter
from Latex.latex import make_latex

var = 39
group = "РК6-85б"
n = 100
name = "Киселев Сергей Андреевич"
name_short = "Киселев С. А."
states = [i+1 for i in range(5)]


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
    for _ in range(n-1):
        per_ver = m[current_s-1]
        next_s = np.random.choice(states, p=per_ver)
        current_s = next_s
        states_tr.append(current_s)
    return dict(sorted(dict(Counter(states_tr)).items())), states_tr


def marginal_probabilities(P):
    A = P.T - np.eye(len(states), dtype=float)
    A[-1] = np.full(len(states), 1)
    b = np.zeros(len(states))
    b[-1] = 1.
    p = np.linalg.solve(A, b)
    return p, [list(p) for _ in range(len(states))], list(p).count(0)!=len(p)


if __name__ == "__main__":
    m = reader(var)
    p, pred_mat_per, erg=marginal_probabilities(m)

    # Markov iteration
    x = [i+1 for i in range(n)]
    dict_comp = []
    plt.figure(figsize=(8, 4))
    plt.grid()
    plt.ylabel("Состояния")
    plt.xlabel("Переходы")
    plt.yticks(np.arange(0, len(states)+1, step=1))
    for _ in range(20):
        myDictionary, tr = mark_iter(n, m, states)
        dict_comp.append(myDictionary)
        plt.plot(x, tr, '-', linewidth=0.7, markeredgewidth=0.1)

    # Latex file creation
    make_latex("{" + f"{var}" + "}", "{" + f"{group}" + "}", "{" + f"{name}" + "}", "{" + f"{name_short}" + "}", m, p, dict_comp)
    plt.savefig('Latex/res/Images/iter.png')
