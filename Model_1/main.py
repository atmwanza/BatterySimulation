import matplotlib.pyplot as plt

#Define some global constants
motor_voltage = 12 #volts
lead_wc_eff = 0.358
lead_bc_eff = 0.495
ball_eff = 0.838
nom_torq = 0.459
ang_velocity = [-10, -7.5, 2.5, 8, -5, -14, -16, -16, -14, -9, -1.25, 3.25, 7, 13, 14, 17, 17.5, 8, -2, -6.25 ]
torques = [1,2,3,4]
x_gait = []
y_power = []
#functions
def get_power_mech(torque,ang):
    return torque*ang

def ang_vel_cycle():
    x_gait.clear()
    y_power.clear()
    for i in range (0,len(ang_velocity)):
        print(i)
        x_gait.append(i*5)
        y_power.append(get_power_mech(nom_torq,ang_velocity[i-1]))
    return


#ignore thermal limits
#inputs: torque, angular velocity

#current_input = (torque * ang_velocity) / (motor_voltage * eff)


# just to test matplotlib works on vscode
#x = [1, 2, 3, 4, 5]
#y = [2, 5, 3, 7, 4]


# plt.plot(x, y)
ang_vel_cycle()
#plt.plot(x_gait, ang_velocity)
plt.plot(x_gait, y_power)


plt.xlabel('Gait Cycle')
plt.ylabel('Power Motorshaft')
plt.title('P_motorshaft vs time')

# Display the plot
plt.show()