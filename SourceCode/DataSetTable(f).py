import numpy as np

# Constants
g = 9.81  # gravity (m/s^2)
dt = 0.1  # time step in seconds

# Table header
print(f"{'ID':>4} | {'h0 (m)':>6} | {'A_tank (m²)':>10} | {'A_hole (m²)':>10} | {'Drain time (min)':>15}")
print("-" * 60)

# Generate 50 simulations with increasing drain time
for sim_id in range(1, 51):
    h0 = 0.5 + 0.05 * (sim_id - 1)     # initial height increases
    A_tank = 0.05 + 0.002 * (sim_id - 1)  # tank area increases
    A_hole = 0.0003 - 0.00001 * (sim_id - 1)  # hole area decreases

    # Initialize
    h = h0
    t = 0

    # Euler integration
    while h > 0:
        v = np.sqrt(2 * g * h)
        dh = (A_hole / A_tank) * v * dt
        h -= dh
        if h < 0:
            h = 0
        t += dt

    drain_time_min = round(t / 60, 2)
    print(f"{sim_id:>4} | {h0:>6.2f} | {A_tank:>10.3f} | {A_hole:>10.5f} | {drain_time_min:>15}")
