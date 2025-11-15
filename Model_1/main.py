import matplotlib.pyplot as plt

#Define some global constants
motor_voltage = 12 #volts
lead_wc_eff = 0.358
lead_bc_eff = 0.495
ball_eff = 0.838
angs = [1,4,9,16]
torques = [1,2,3,4]
x_gait = []
y_power = []
#functions
def get_power_mech(torque,ang):
    return torque*ang

def cycle():
    x_gait.clear()
    y_power.clear()
    for i in range (1,len(torques)+1):
        x_gait.append(i*5)
        y_power.append(get_power_mech(torques[i-1],angs[i-1]))



#ignore thermal limits
#inputs: torque, angular velocity

#current_input = (torque * ang_velocity) / (motor_voltage * eff)


# just to test matplotlib works on vscode
x = [1, 2, 3, 4, 5]
y = [2, 5, 3, 7, 4]


# plt.plot(x, y)
plt.plot(x_gait, y_power)


plt.xlabel('Gait Cycle')
plt.ylabel('Power Motorshaft')
plt.title('P_motorshaft vs time')

# Display the plot
plt.show()