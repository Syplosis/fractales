import cmath
import numpy as np
import matplotlib.pyplot as plt

A = np.linspace(-1, 1, 300)
B = np.linspace(-1, 1, 300)
X = []
Y = []

for a in A:
    for b in B:
        z = complex(a, b)
        i = 0
        while abs(z) < 2 and i < 100:
            c = complex(-0.7927, 0.1609)
            z = z*z + c
            i += 1
        if i==30:
            X.append(a)
            Y.append(b)

plt.scatter(X, Y, s=1)
plt.show()