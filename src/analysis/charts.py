import numpy as np
import matplotlib.pyplot as plt

def plotSimResults(T, Y, X):
    fig, ax = plt.subplots()
    ax.plot(T, X[:, 1], label='Angular Velocity')
    ax.plot(T, X[:, 2], label='Angular Position')
    plt.xlabel('Time (s)')
    plt.ylabel('rad/s, rad')
    plt.legend()
    plt.title('DC Motor Simulation Results')
    plt.show()