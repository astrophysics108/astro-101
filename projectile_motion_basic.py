import numpy as np  
import matplotlib.pyplot as plt  
from matplotlib.widgets import Slider  

g = 9.81  

def projectile_motion(v0, angle, h0):  
    angle_rad = np.radians(angle)  
    t_flight = (v0 * np.sin(angle_rad) + np.sqrt((v0 * np.sin(angle_rad))**2 + 2 * g * h0)) / g  
    t = np.linspace(0, t_flight, num=500)  
    x = v0 * np.cos(angle_rad) * t  
    y = h0 + v0 * np.sin(angle_rad) * t - (0.5 * g * t**2)  
    return x, y  

fig, ax = plt.subplots(figsize=(10, 5))  
plt.subplots_adjust(bottom=0.25)  

initial_velocity = 50  
launch_angle = 45      
initial_height = 0     

x, y = projectile_motion(initial_velocity, launch_angle, initial_height)  
line, = ax.plot(x, y, lw=2)  
ax.set_xlim(0, 300)  
ax.set_ylim(0, 100)  
ax.axhline(0, color='black', linewidth=0.5)  
ax.grid()  
ax.set_title('Projectile Motion Simulation')  
ax.set_xlabel('Distance (m)')  
ax.set_ylabel('Height (m)')  

ax_velocity = plt.axes([0.1, 0.1, 0.65, 0.03])  
slider_velocity = Slider(ax_velocity, 'Initial Velocity (m/s)', 0, 100, valinit=initial_velocity)  

ax_angle = plt.axes([0.1, 0.06, 0.65, 0.03])  
slider_angle = Slider(ax_angle, 'Launch Angle (degrees)', 0, 90, valinit=launch_angle)  

def update(val):  
    v0 = slider_velocity.val  
    angle = slider_angle.val  
    x, y = projectile_motion(v0, angle, initial_height)  
    line.set_xdata(x)  
    line.set_ydata(y)  
    ax.set_ylim(0, max(y) * 1.1)  
    ax.set_title(f'Projectile Motion: v0={v0} m/s, angle={angle}°')  
    fig.canvas.draw_idle()  

slider_velocity.on_changed(update)  
slider_angle.on_changed(update)  

plt.show()
