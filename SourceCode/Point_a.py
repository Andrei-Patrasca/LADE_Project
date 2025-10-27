#import all the libraries needed
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np

# constants
g = 9.81          # gravity m/s^2
h0 = 50           # initial height in meters
v0 = 0            # initial velocity

# system of first-order ODEs
def gravity_system(y, t):
    h, v = y
    dhdt = v
    dvdt = -g
    return [dhdt, dvdt]

# time vector
t = np.linspace(0, np.sqrt(2*h0/g), 200)

# initial conditions
y0 = [h0, v0]

# solve ODE
sol = odeint(gravity_system, y0, t)
h = sol[:,0]
v = sol[:,1]

# Plot height and velocity
fig = plt.figure(num=1)
plt.subplot(2,1,1)
plt.plot(t, h, linewidth=3)
plt.title("Object Falling Under Gravity")
plt.ylabel("Height h(t) (m)")

plt.subplot(2,1,2)
plt.plot(t, v, 'r', linewidth=3)
plt.xlabel("Time (s)")
plt.ylabel("Velocity v(t) (m/s)")
plt.grid(True)
plt.show()

# Print final velocity
print(f"Final velocity at impact: v = {v[-1]:.2f} m/s,  Theoretical = {-np.sqrt(2*g*h0):.2f} m/s")
