import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv
import math
import numpy as np



#Define some global constants

#read file data to list
time_data = []
joint_power_data = []
joint_angles = []
temp_time = []
weighted_joint_power_data = []

motor_voltage = 12 #volts
lead_wc_eff = 0.358
lead_bc_eff = 0.495
ball_eff = 0.838
nom_torq_ms = 0.459
nom_torq_j = 50

assumed_weight = 80 #kg
R_phase = 0.06882 # Ohms
battery_capacity = 15 #Ah

ang_velocity = [-10, -7.5, 2.5, 8, -5, -14, -16, -16, -14, -9, -1.25, 3.25, 7, 13, 14, 17, 17.5, 8, -2, -6.25 ]
torques = [1,2,3,4]
x_gait = []
y_current = []
y_power_ms = []
y_power_j = []

sts_torque_x = []
sts_torque_y = []
x_power_elec = []
y_power_elec = []
#functions

#****************sit to stand stuff****************#
def angular_velocity_sts(x):
    return 107.478*((1/np.cosh((x-1.85)/0.37))**2)

def get_csv_torque_data():
    sts_torque_x.clear()
    sts_torque_y.clear()
    with open('sts_torque.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)
        time_col_idx = 0
        tor_col_idx = 1
        for row in file_reader:
            if len(row) > tor_col_idx:
                sts_torque_x.append(float(row[time_col_idx]))
                sts_torque_y.append(float(row[tor_col_idx]))
    return

get_csv_torque_data()
a, b, c = np.polyfit(sts_torque_x, sts_torque_y, 2)
print(a)
print(b)
print(c)
def torque_function(x):
    return a*(x**2) + (b*x) + c

def power_sts(x):
    t = torque_function(x)
    av = angular_velocity_sts(x)
    return t*av

def sts_cycle():
    values = np.linspace(0.0,3.0,100)
    for i in values:
        y_power_elec.append(power_sts(i))
        x_power_elec.append(i)

def sit_to_stand_plots():
    sts_cycle()
    plt.figure(6)
    plt.plot(x_power_elec, y_power_elec)
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Time')
    plt.ylabel('Power Electrical W')
    plt.title('P_Electrical In Sitting To Standing')
    plt.savefig("my_plot.png", dpi=300, bbox_inches="tight")
    #plt.show()
    return
def test_plot():
    temp_x = []
    temp_y = []
    for i in range(100):
        temp_x.append(i)
        temp_y.append(torque_function(i))
    plt.figure(7)
    plt.plot(temp_x, temp_y)
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Time')
    plt.ylabel('Torque Nm')
    plt.title('Torque Plot')
    plt.savefig("torque.png", dpi=300, bbox_inches="tight")
    return
#****************sit to stand stuff****************#
print("hi")
def get_power_mech(torque,ang):
    return torque*ang

def p_motorshaft_cycle():
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

def get_weighted_list(data):
    return [x * assumed_weight for x in data]

def get_motor_power(data):
    return [ x * ball_eff for x in get_weighted_list(data)]

def get_csv_data():
    time_data.clear()
    joint_power_data.clear()
    with open('kneeJointPower_final.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)
        time_col_idx = 0
        power_col_idx = 1
        for row in file_reader:
            if len(row) > power_col_idx:
                time_data.append(float(row[time_col_idx]))
                joint_power_data.append(float(row[power_col_idx]))
    return

#gets sit to stand angular data from csv
def get_csv_joint_data():
    temp_time.clear()
    joint_angles.clear()
    with open('SitToStandAngles.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)
        time_col_idx = 0
        angle_col_idx = 1
        for row in file_reader:
            if len(row) > angle_col_idx:
                temp_time.append(float(row[time_col_idx]))
                joint_angles.append(float(row[angle_col_idx]))
    return



def mechanical_plots():
    p_motorshaft_cycle()
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
    plt.title('P_joint vs Time')

    plt.show()
    return

def current_plot():
    current_data = [(-motor_voltage + math.sqrt(motor_voltage ** 2 + 4 * R_phase * p_motor)) / (2 * R_phase) for p_motor in get_motor_power(joint_power_data)]
    plt.figure(3)
    plt.plot(time_data, current_data)
    plt.axhline(y=0, color="grey", linestyle='-', linewidth='1')
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.title('Current vs Time')
    plt.show()
    return

def angle_plot():
    plt.figure(4)
    plt.plot(temp_time, joint_angles)
    plt.axhline(y=0, color="grey", linestyle='-', linewidth='1')
    plt.axvline(x=0, color='grey', linestyle='-', linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('Angle')
    plt.title('Angle  vs Time')
    plt.show()
    return

def average_current():
    current_data = [(-motor_voltage + math.sqrt(motor_voltage ** 2 + 4 * R_phase * p_motor)) / (2 * R_phase) for p_motor in get_motor_power(joint_power_data)]
    avg_current = np.mean(current_data)
    print("Average Current (A): ", avg_current)
    return avg_current

def average_power_gait():
    motor_power = get_motor_power(joint_power_data)
    avg_power_gait = np.mean(motor_power)
    print("Average Power (W): ", avg_power_gait)
    return avg_power_gait

def braking_torque():
    gait_cycle_time = time_data[-1] - time_data[0]
    #used phys teams data for torque doc
    #6 degree change in 0.1 sec from heel strike to foot flat
    delta_theta = 6 * (math.pi/180) #radians
    delta_t = 0.1 #sec
    ang_velocity_braking = delta_theta / delta_t #rad/sec

    motor_power = get_motor_power(joint_power_data)
    min_power = min(motor_power[0:int(len(motor_power)/2)]) #mininum power from the first half of the gait cycle
    braking_torque = min_power / ang_velocity_braking
    print("Braking Torque (Nm): ", braking_torque)
    return braking_torque

def cum_avg_plot():
    P_in = get_motor_power(joint_power_data)
    P_in = [ x * 0.7 for x in P_in] #walking weighted at 70% 
    # standing accounts for 20% but power is negligible at this phase
    # sitting accounts for 10% but power is negligible at this phase
    plt.figure(5)
    plt.plot(temp_time, P_in)
    plt.axhline(y=0, color="grey", linestyle='-', linewidth='1')
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('P_in (W)')
    plt.title('Power Input vs Time')
    plt.show()
    return P_in
def battery_life_estimate():
    # assume we aren't capable of regenerative braking for this model
    current_data = [(-motor_voltage + math.sqrt(motor_voltage ** 2 + 4 * R_phase * p_motor)) / (2 * R_phase) for p_motor in get_motor_power(joint_power_data)]  
    positive_current_data = current_data.copy()
    for i in range(len(current_data)): # set all negative currents to zero
        if positive_current_data[i] < 0:
            positive_current_data[i] = 0
    avg_current = np.mean(positive_current_data)
    print("Average Positive Current (A): ",avg_current)
    battery_life_hours = battery_capacity / avg_current
    print("Estimated Battery Life (hours): ", battery_life_hours)
    return

#def plot_sts_torque():


get_csv_data()
#get_csv_joint_data() 
# mechanical_plots()
# current_plot()
#angle_plot()
average_current()
average_power_gait()
braking_torque()
#cum_avg_plot()
battery_life_estimate()
#sit_to_stand_plots()
test_plot()



