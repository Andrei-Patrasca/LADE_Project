import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon

G = 980.0                
SQRT_2G = np.sqrt(2 * G) 
EPSILON = 1e-6           

H_TOTAL = 50.0           
R_TOTAL = 30.0           
R_RATIO = R_TOTAL / H_TOTAL 

D_HOLE = 1.0             
R_HOLE = D_HOLE / 2.0    
A_HOLE = np.pi * R_HOLE**2 


def get_cross_sectional_area(h, tank_type):

    if h <= EPSILON:
        return 0.0 
        
    if tank_type == 'original':
        radius = R_RATIO * h
    elif tank_type == 'upside_down':
        radius = R_RATIO * max(0, H_TOTAL - h)
            
    area = np.pi * radius**2
    if area < EPSILON:
        return 0.0
    return area

def get_dh_dt(h, tank_type):

    if h <= EPSILON:
        return 0.0 

    A_h = get_cross_sectional_area(h, tank_type)
    
    v_out = SQRT_2G * np.sqrt(h)
    
    if A_h <= A_HOLE:
        dh_dt = -v_out
    else:
        dh_dt = (-A_HOLE * v_out) / A_h
    
    return dh_dt

DT = 0.01 
h_original = H_TOTAL
h_upside_down = H_TOTAL
time_elapsed = 0.0
history_time = [0]
history_h_original = [H_TOTAL]
history_h_upside_down = [H_TOTAL]

fig, (ax_tanks, ax_graph) = plt.subplots(1, 2, figsize=(14, 7))
fig.suptitle('Torricelli\'s Law: Conical Tank Drainage Simulation', fontsize=16)
fig.tight_layout(rect=[0, 0.03, 1, 0.92]) # Adjust layout for suptitle
fig.subplots_adjust(left=0.08)

ax_tanks.set_title('Tank Water Levels')
ax_tanks.set_xlim(-R_TOTAL * 2.5, R_TOTAL * 2.5)
ax_tanks.set_ylim(-5, H_TOTAL + 10)
ax_tanks.set_aspect('equal')
ax_tanks.set_xticks([])
ax_tanks.set_yticks([0, H_TOTAL/2, H_TOTAL])
ax_tanks.set_yticklabels(['0 cm', f'{H_TOTAL/2} cm', f'{H_TOTAL} cm'])
ORIGINAL_OFFSET = -R_TOTAL * 1.2
UPSIDE_DOWN_OFFSET = R_TOTAL * 1.2
original_tank_coords = [
    (ORIGINAL_OFFSET - R_TOTAL, H_TOTAL),
    (ORIGINAL_OFFSET, 0),
    (ORIGINAL_OFFSET + R_TOTAL, H_TOTAL)
]
ax_tanks.add_patch(Polygon(original_tank_coords, closed=False, color='black', linewidth=2))
ax_tanks.text(ORIGINAL_OFFSET, H_TOTAL + 5, 'Original', ha='center', fontsize=12)
upside_down_tank_coords = [
    (UPSIDE_DOWN_OFFSET - R_TOTAL, 0),
    (UPSIDE_DOWN_OFFSET, H_TOTAL),
    (UPSIDE_DOWN_OFFSET + R_TOTAL, 0)
]
ax_tanks.add_patch(Polygon(upside_down_tank_coords, closed=False, color='black', linewidth=2))
ax_tanks.text(UPSIDE_DOWN_OFFSET, H_TOTAL + 5, 'Upside-Down', ha='center', fontsize=12)
water_original = ax_tanks.add_patch(Polygon(np.empty((0, 2)), color='blue', alpha=0.6))
water_upside_down = ax_tanks.add_patch(Polygon(np.empty((0, 2)), color='cyan', alpha=0.6))
time_text = ax_tanks.text(-R_TOTAL * 2, -3, 'Time: 0.00 s', fontsize=12)

ax_graph.set_title('Height vs. Time')
ax_graph.set_xlabel('Time (s)')
ax_graph.set_ylabel('Height (cm)')
ax_graph.set_xlim(0, 650) 
ax_graph.set_ylim(0, H_TOTAL + 5)
ax_graph.grid(True)
line_original, = ax_graph.plot([], [], 'blue', label=f'Original (drains in ~{230:.0f} s)')
line_upside_down, = ax_graph.plot([], [], 'cyan', label=f'Upside-Down (drains in ~{613:.0f} s)')
ax_graph.legend()


def update_water_patches(h_orig, h_up):
    
    if h_orig > EPSILON:
        r_orig = R_RATIO * h_orig
        water_orig_coords = [
            (ORIGINAL_OFFSET, 0),
            (ORIGINAL_OFFSET - r_orig, h_orig),
            (ORIGINAL_OFFSET + r_orig, h_orig)
        ]
        water_original.set_xy(water_orig_coords)
    else:
        water_original.set_xy(np.empty((0, 2))) # Empty

    if h_up > EPSILON:
        r_up_bottom = R_TOTAL 
        r_up_top = R_RATIO * max(0, H_TOTAL - h_up) 
        water_up_coords = [
            (UPSIDE_DOWN_OFFSET - r_up_bottom, 0),
            (UPSIDE_DOWN_OFFSET + r_up_bottom, 0),
            (UPSIDE_DOWN_OFFSET + r_up_top, h_up),
            (UPSIDE_DOWN_OFFSET - r_up_top, h_up)
        ]
        water_upside_down.set_xy(water_up_coords)
    else:
        water_upside_down.set_xy(np.empty((0, 2))) # Empty

def init():
    update_water_patches(H_TOTAL, H_TOTAL)
    line_original.set_data([], [])
    line_upside_down.set_data([], [])
    time_text.set_text('Time: 0.00 s')
    
    return water_original, water_upside_down, line_original, line_upside_down, time_text

def animate(frame):
    global h_original, h_upside_down, time_elapsed, ani
    
    steps_per_frame = 50 
    
    is_still_running = False 
    
    for _ in range(steps_per_frame):
        
        is_running_this_iter = False 

        if h_original > EPSILON:
            dh_orig = get_dh_dt(h_original, 'original') * DT
            h_original = max(0, h_original + dh_orig)
            is_still_running = True 
            is_running_this_iter = True
        else:
            h_original = 0 
        
        
        if h_upside_down > EPSILON:
            dh_up = get_dh_dt(h_upside_down, 'upside_down') * DT
            h_upside_down = max(0, h_upside_down + dh_up)
            is_still_running = True 
            is_running_this_iter = True
        else:
            h_upside_down = 0 

        if is_running_this_iter:
             time_elapsed += DT
        else:
             break 
    
    history_time.append(time_elapsed)
    history_h_original.append(h_original)
    history_h_upside_down.append(h_upside_down)
    
    update_water_patches(h_original, h_upside_down)
    line_original.set_data(history_time, history_h_original)
    line_upside_down.set_data(history_time, history_h_upside_down)
    time_text.set_text(f'Time: {time_elapsed:.2f} s')
    
    if not is_still_running:
        if ani:
            print(f"Simulation complete. Final time: {time_elapsed:.2f} s")
            ani.event_source.stop()

    return water_original, water_upside_down, line_original, line_upside_down, time_text

ani = None 
ani = FuncAnimation(fig, animate, init_func=init, 
                    frames=None, interval=20, blit=True, save_count=1000)

plt.show()


