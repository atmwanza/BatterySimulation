import matplotlib.pyplot as plt
import csv
import math


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

def angle_plot():
    plt.figure(4)
    plt.plot(temp_time, joint_angles)
    plt.axhline(y=0, color="grey", linestyle='-', linewidth='1')
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('Angle')
    plt.title('Angle  vs Time')
    plt.show()

get_csv_data()
get_csv_joint_data()
#mechanical_plots()
#current_plot()
angle_plot()
