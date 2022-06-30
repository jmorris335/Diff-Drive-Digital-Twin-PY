import numpy as np
import matplotlib.pyplot as plt
from src.objects.DC_Motor import DC_Motor

def simulateMotors():
    motor = DC_Motor()
    time = np.arange(0, 5, 0.03).T
    v_s = np.zeros_like(time) + 18
    T_L = np.zeros_like(time) + -0.5
    T, Y, X = motor.simulateMotor(time, v_s, T_L)
    return T, Y, X

def plotSimResults(T, Y, X):
    fig, ax = plt.subplots()
    ax.plot(T, X[:, 1], label='Angular Velocity')
    ax.plot(T, X[:, 2], label='Angular Position')
    plt.xlabel('Time (s)')
    plt.ylabel('rad/s, rad')
    plt.legend()
    plt.title('DC Motor Simulation Results')
    plt.show()

def test_primary():
    T, Y, X = simulateMotors()
    plotSimResults(T, Y, X)

