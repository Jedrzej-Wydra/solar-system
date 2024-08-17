import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import math

x_data1 = []
y_data1 = []

x_data2 = []
y_data2 = []

x_data3 = []
y_data3 = []

x_data4 = []
y_data4 = []

fig, ax = plt.subplots()
t_range = np.linspace(0,20*math.pi,1000)

for value in t_range:
    cosx = math.cos(value)
    siny = math.sin(value)
    x_data1.append(cosx)
    y_data1.append(siny)
    
for value in t_range:
    cosx = 2*math.cos(value/2)
    siny = 2*math.sin(value/2)
    x_data2.append(cosx)
    y_data2.append(siny)
    
for value in t_range:
    cosx = 4*math.cos(value/3)
    siny = 4*math.sin(value/3)
    x_data3.append(cosx)
    y_data3.append(siny)
    
for value in t_range:
    cosx = 0.2*math.cos(12*value) + 2*math.cos(value/2)
    siny = 0.2*math.sin(12*value) + 2*math.sin(value/2)
    x_data4.append(cosx)
    y_data4.append(siny)

x_axis1 = []
y_axis1 = []

x_axis2 = []
y_axis2 = []

x_axis3 = []
y_axis3 = []

x_axis4 = []
y_axis4 = []


def animate(i):
    y_coordinate = y_data1[i]
    x_coordinate = x_data1[i]
    x_axis1.append(x_coordinate)
    y_axis1.append(y_coordinate)
    
    y_coordinate = y_data2[i]
    x_coordinate = x_data2[i]
    x_axis2.append(x_coordinate)
    y_axis2.append(y_coordinate)
    
    y_coordinate = y_data3[i]
    x_coordinate = x_data3[i]
    x_axis3.append(x_coordinate)
    y_axis3.append(y_coordinate)
    
    y_coordinate = y_data4[i]
    x_coordinate = x_data4[i]
    x_axis4.append(x_coordinate)
    y_axis4.append(y_coordinate)
    
    ax.clear()
    ax.plot(x_axis1, y_axis1, color = "pink")
    ax.plot(x_axis2, y_axis2, color = "blue")
    ax.plot(x_axis3, y_axis3, color = "orange")
    ax.plot(x_axis4, y_axis4, color = "black")
    ax.scatter(0, 0, s=25, color = "red")
    ax.set_xlim([-5,5])
    ax.set_ylim([-5,5])

ani = FuncAnimation(fig, animate, frames=1000, interval=1, repeat=True)

plt.style.use('dark_background')
plt.show()
    
