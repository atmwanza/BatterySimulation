import matplotlib.pyplot as plt

#Define some global constants
motor_voltage = 12 #volts
lead_wc_eff = 0.358
lead_bc_eff = 0.495
ball_eff = 0.838

#ignore thermal limits
#inputs: torque, angular velocity

#current_input = (torque * ang_velocity) / (motor_voltage * eff)


# just to test matplotlib works on vscode
x = [1, 2, 3, 4, 5]
y = [2, 5, 3, 7, 4]


plt.plot(x, y)


plt.xlabel('X')
plt.ylabel('Y')
plt.title('X vs Y')

# Display the plot
plt.show()