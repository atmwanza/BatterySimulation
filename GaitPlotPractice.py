import matplotlib.pyplot as plt
import csv
import math

#read file data to list
time_data = []
joint_power_data = []

#grab data from this file and make two lists
with open('kneeJointPower.csv', 'r', newline='') as power_file:
    file_reader = csv.reader(power_file)
    header = next(file_reader)
    time_col_idx = 0
    power_col_idx = 1
    for row in file_reader:
        if len(row) > power_col_idx:
            time_data.append(float(row[time_col_idx]))
            joint_power_data.append(float(row[power_col_idx]))
print(len(time_data))
print(len(joint_power_data))
#Define some global constants
motor_voltage = 12.0 #volts
lead_wc_eff = 0.358
lead_bc_eff = 0.495
ball_eff = 0.838
assumed_weight = 80 #kg
R_phase = 0.06882 # 

#ignore thermal limits
#inputs: torque, angular velocity

#current_input = (torque * ang_velocity) / (motor_voltage * eff)
joint_power_data_assuming_weight = [x * assumed_weight for x in joint_power_data]

# get P_motor
motor_power_data = [ x * ball_eff for x in joint_power_data_assuming_weight]
#assume P_motor == P_elec
# P_motor = V * I(t) + I^2(t)*R
#find the current (assumed to take the "plus" solution to the quadratic equation), gotta double check the current being negative.
current_data = [ -(-motor_voltage + math.sqrt(motor_voltage**2 + 4 * R_phase * p_motor))/(2*R_phase) for p_motor in motor_power_data]

# plt.plot(time_data, joint_power_data_assuming_weight)

plt.plot(time_data, current_data)

# plt.xlabel('Time (sec)')
# plt.ylabel('Power per kg (W/kg)')
# plt.title('Knee Joint Mechanical Power')
plt.xlabel('Time (sec)')
plt.ylabel('Current (A)')
plt.title('Current output in the Gait Cycle')
# Display the plot
plt.show()
