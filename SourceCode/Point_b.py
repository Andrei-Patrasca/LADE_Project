# import all the libraries needed to plot, integrate, numerically solve ODEs
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np

# physical constants
g = 9.81          # gravity (m/s^2)
a = 5e-5          # hole area (m^2)
A = 1.0           # tank cross sectional area (m^2)

# differential equation from Torricelli's Law
def torricelli(h, t):
    dhdt = -(a/A) * np.sqrt(2 * g * h)
    return dhdt

# time array
t = np.linspace(0, 50, 500)

# prepare the figure
fig = plt.figure(num=1)
ax = fig.add_subplot(111)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 11
fig_size[1] = 11

# Create vector field in phase space (h, dh/dt)
H = np.linspace(0, 2.5, 20)   # water height range
dHdt = -(a/A) * np.sqrt(2 * g * H)
H_grid, dHdt_grid = np.meshgrid(H, dHdt)

# normalize vector field arrows for aesthetics
N = np.sqrt(1**2 + dHdt_grid**2)
U = 1 / N
V = dHdt_grid / N

# plot vector field with color
plt.quiver(H_grid, dHdt_grid, U, V, color='purple')

# solve ODE numerically for different initial heights
initial_heights = [2.0, 1.5, 1.0, 0.5]
colors = ['red', 'blue', 'green', 'orange']

for h0, c in zip(initial_heights, colors):
    sol = odeint(torricelli, h0, t)
    dhdt_sol = torricelli(sol[:,0], t)  # compute velocity dh/dt
    plt.plot(sol, dhdt_sol, color=c, linewidth=3, label=f"h(0)={h0} m")

plt.title("Phase Space of Torricelli's Law (h vs dh/dt)")
plt.xlabel("Height h(t) (m)")
plt.ylabel("Velocity dh/dt (m/s)")
plt.legend()
plt.grid(True)
plt.show()
