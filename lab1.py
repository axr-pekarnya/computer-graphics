import numpy as np
import matplotlib.pyplot as plt

def PosFunc(x, a : float):
    return np.sqrt(x ** 3 / (a - x))

def NegFunc(x, a : float):
    return - np.sqrt(x ** 3 / (a - x))

if __name__ == "__main__":
    print("Input parametr a: ", end='')
    a = float(input())

    print("Input parametr B: ", end='')
    B = float(input())

    if a <= 0 or B <= 0:
        print("Invalid parameter")
        exit()

    title = "y^2 = x * 3 / (a - x)"
    x = np.arange(0, B, 0.01)

    yPos = []
    yNeg = []

    for elem in x:
        yPos.append(PosFunc(elem, a))
        yNeg.append(NegFunc(elem, a))

    plt.plot(x, yPos, 'b', label=r"$y = \sqrt{\frac{x^3}{a - x}}$")
    plt.plot(x, yNeg, 'g', label=r"$y = - \sqrt{\frac{x^3}{a - x}}$")
    plt.grid(True)

    plt.legend(title=r"$y^2 = \frac{x^3}{a - x}, \; 0 < x \leq B, \, a > 0$")

    plt.show() 

