import matplotlib.pyplot as plt

#Define some global constants
motor_voltage = 12 #volts
lead_wc_eff = 0.358
lead_bc_eff = 0.495
ball_eff = 0.838
nom_torq_ms = 0.459
nom_torq_j = 50

ang_velocity = [-10, -7.5, 2.5, 8, -5, -14, -16, -16, -14, -9, -1.25, 3.25, 7, 13, 14, 17, 17.5, 8, -2, -6.25 ]
torques = [1,2,3,4]
x_gait = []
y_current = []
y_power_ms = []
y_power_j = []
#functions
def get_power_mech(torque,ang):
    return torque*ang

def p_motoroshaft_cycle():
    x_gait.clear()
    y_power_ms.clear()
    for i in range (0,len(ang_velocity)):
        print(i)
        x_gait.append(i*5)
        y_power_ms.append(get_power_mech(nom_torq_ms ,ang_velocity[i]))
    return

def p_joint_cycle():
    x_gait.clear()
    y_power_j.clear()
    for i in range (0,len(ang_velocity)):
        print(i)
        x_gait.append(i*5)
        y_power_j.append(get_power_mech(nom_torq_j ,ang_velocity[i]))
    return


def get_current(p_motor):
    return p_motor/motor_voltage

#i(t) = PJoint/
def i_cycle():
    x_gait.clear()
    y_current.clear()
    return

#ignore thermal limits
#inputs: torque, angular velocity

#current_input = (torque * ang_velocity) / (motor_voltage * eff)


# just to test matplotlib works on vscode
#x = [1, 2, 3, 4, 5]
#y = [2, 5, 3, 7, 4]

p_motoroshaft_cycle()
p_joint_cycle()

plt.figure(1)
plt.plot(x_gait, y_power_ms)
plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
plt.xlabel('Gait Cycle %')
plt.ylabel('Power Motorshaft W')
plt.title('P_motorshaft vs time')

plt.figure(2)
plt.plot(x_gait,y_power_j)
plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
plt.xlabel('Gait Cycle %')
plt.ylabel('Power Joint W')
plt.title('P_joint vs time')

plt.show()
