import numpy as np
import matplotlib.pyplot as plt

# Constants
g = 9.81  # gravity (m/s^2)
A_tank = 0.05  # tank area in m^2
A_hole = 0.0003  # hole area in m^2 (adjusted to get ~5.8 min)
h0 = 1.0  # initial water height in m
dt = 0.1  # time step in seconds

# Initialize
h = h0
t = 0
times = []
heights = []

# Euler integration loop
while h > 0:
    v = np.sqrt(2 * g * h)
    dh = (A_hole / A_tank) * v * dt
    h -= dh
    if h < 0:
        h = 0
    times.append(t / 60)  # convert time to minutes
    heights.append(h)
    t += dt

# Plotting
plt.figure(figsize=(8, 5))
plt.plot(times, heights)
plt.title("Water Height vs Time (Tank Draining Simulation)")
plt.xlabel("Time (minutes)")
plt.ylabel("Water Height (m)")
plt.grid(True)

# Annotate with simulation parameters
info_text = (
    f"Initial height: {h0} m\n"
    f"Tank area: {A_tank} m²\n"
    f"Hole area: {A_hole} m²\n"
    f"Total drain time: {round(t/60, 2)} min"
)
plt.text(
    0.95, 0.95, info_text,
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment='top',
    horizontalalignment='right',
    bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray')
)

plt.show()
