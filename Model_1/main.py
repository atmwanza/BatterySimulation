import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for saving figures

import matplotlib.pyplot as plt
import csv
import math
import numpy as np
from scipy.interpolate import CubicSpline


# ============================================================
#  GLOBAL CONSTANTS & PARAMETERS
# ============================================================

# Electrical / motor constants
motor_voltage   = 12        # V
R_phase         = 0.06882   # Ohms
battery_capacity = 15       # Ah

# Efficiencies
lead_wc_eff = 0.358
lead_bc_eff = 0.495
ball_eff    = 0.838

# Nominal torques
nom_torq_ms = 0.459         # N·m (motor shaft)
nom_torq_j  = 50            # N·m (joint)

# Human / biomech parameters
assumed_weight = 80         # kg

# Sit-to-stand S-curve scaling (for ~2 seconds)
time_scale = 3.0 / 2.0

# Example gait angular velocity samples (deg/s or rad/s depending on your convention)
ang_velocity = [
    -10, -7.5, 2.5, 8, -5, -14, -16, -16, -14, -9,
    -1.25, 3.25, 7, 13, 14, 17, 17.5, 8, -2, -6.25
]

torques = [1, 2, 3, 4]


# ============================================================
#  GLOBAL DATA ARRAYS (CONTAINERS)
# ============================================================

# Gait / power CSV data
time_data              = []
joint_power_data       = []
joint_angles           = []
temp_time              = []
weighted_joint_power_data = []

# Gait-based power plots
x_gait     = []
y_current  = []
y_power_ms = []
y_power_j  = []

# Sit-to-stand (STS) torque & power data
sts_torque_x   = []
sts_torque_y   = []
x_power_elec   = []
y_power_elec   = []
max_torque     = None

# Theta_2 (another joint angle) data
theta2_t = []
theta2_y = []

# Spline inputs for torque & angle (from better_*.csv)
t_x = []
t_y = []
a_x = []
a_y = []

# Inputs for dataset 3
subject_mass = 80
subject_height = 1.84

#sit to stand
a3_x = []
a3_y = []
t3_x = []
t3_y = []

total_time = 2.0
#stand to sit
a3_xn = []
a3_yn = []
t3_xn = []
t3_yn = []

total_timen = 1

# ============================================================
#  CSV LOADING FUNCTIONS (TORQUE, ANGLE, THETA2, GAIT, etc.)
# ============================================================

def get_torque_data():
    """
    Load torque vs time data from better_torque.csv into t_x, t_y.
    """
    t_x.clear()
    t_y.clear()
    with open('better_torque.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)  # skip header
        time_col_idx = 0
        tor_col_idx  = 1
        for row in file_reader:
            if len(row) > tor_col_idx:
                t_x.append(float(row[time_col_idx]))
                t_y.append(float(row[tor_col_idx]))


def get_angle_data():
    """
    Load angle vs time data from better_angle.csv into a_x, a_y.
    """
    a_x.clear()
    a_y.clear()
    with open('better_angle.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)
        time_col_idx = 0
        ang_col_idx  = 1
        for row in file_reader:
            if len(row) > ang_col_idx:
                a_x.append(float(row[time_col_idx]))
                a_y.append(float(row[ang_col_idx]))


def get_theta_2_joint_data():
    """
    Load theta2 joint angle vs time from theta2_plot.csv into theta2_t, theta2_y.
    """
    theta2_t.clear()
    theta2_y.clear()
    with open('theta2_plot.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)
        time_col_idx  = 0
        angle_col_idx = 1
        for row in file_reader:
            if len(row) > angle_col_idx:
                theta2_t.append(float(row[time_col_idx]))
                theta2_y.append(float(row[angle_col_idx]))


def get_csv_torque_data():
    """
    Load sit-to-stand torque from sts_torque.csv into sts_torque_x, sts_torque_y.
    Also sets max_torque.
    """
    global max_torque
    sts_torque_x.clear()
    sts_torque_y.clear()
    with open('sts_torque.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)
        time_col_idx = 0
        tor_col_idx  = 1
        for row in file_reader:
            if len(row) > tor_col_idx:
                sts_torque_x.append(float(row[time_col_idx]))
                sts_torque_y.append(float(row[tor_col_idx]))
    max_torque = max(sts_torque_x)


def get_csv_data():
    """
    Load knee joint power vs time from kneeJointPower_final.csv.
    """
    time_data.clear()
    joint_power_data.clear()
    with open('kneeJointPower_final.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)
        time_col_idx  = 0
        power_col_idx = 1
        for row in file_reader:
            if len(row) > power_col_idx:
                time_data.append(float(row[time_col_idx]))
                joint_power_data.append(float(row[power_col_idx]))


def get_csv_joint_data():
    """
    Load sit-to-stand angle vs time from SitToStandAngles.csv.
    """
    temp_time.clear()
    joint_angles.clear()
    with open('SitToStandAngles.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)
        time_col_idx  = 0
        angle_col_idx = 1
        for row in file_reader:
            if len(row) > angle_col_idx:
                temp_time.append(float(row[time_col_idx]))
                joint_angles.append(float(row[angle_col_idx]))

def get_csv_angle3_data():
    """
    Load sit-to-stand angle vs time from SitToStandAngles.csv.
    """
    a3_x.clear()
    a3_y.clear()
    with open('sittostand_angles3.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)
        time_col_idx  = 0
        angle_col_idx = 1
        for row in file_reader:
            if len(row) > angle_col_idx:
                a3_x.append(float(row[time_col_idx]))
                a3_y.append(180.0 - float(row[angle_col_idx]))
                #a3_y.append(((180.0 - float(row[angle_col_idx]))*math.pi)/180.0)

def get_csv_torque3_data():
    """
    Load sit-to-stand torque vs time from SitToStandAngles.csv.
    """
    t3_x.clear()
    t3_y.clear()
    with open('sittostand_torque3.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)
        time_col_idx  = 0
        angle_col_idx = 1
        for row in file_reader:
            if len(row) > angle_col_idx:
                t3_x.append(float(row[time_col_idx]))
                t3_y.append(float(row[angle_col_idx]))

def get_csv_angle3n_data():
    """
    Load sit-to-stand angle vs time from SitToStandAngles.csv.
    """
    a3_xn.clear()
    a3_yn.clear()
    with open('standtosit_angles.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)
        time_col_idx  = 0
        angle_col_idx = 1
        for row in file_reader:
            if len(row) > angle_col_idx:
                a3_xn.append(float(row[time_col_idx]))
                a3_yn.append(180.0 - float(row[angle_col_idx]))
def get_csv_torque3n_data():
    """
    Load sit-to-stand torque vs time from SitToStandAngles.csv.
    """
    t3_xn.clear()
    t3_yn.clear()
    with open('standtosit_torque.csv', 'r', newline='') as power_file:
        file_reader = csv.reader(power_file)
        header = next(file_reader)
        time_col_idx  = 0
        angle_col_idx = 1
        for row in file_reader:
            if len(row) > angle_col_idx:
                t3_xn.append(float(row[time_col_idx]))
                t3_yn.append(float(row[angle_col_idx]))

# ============================================================
#  SPLINE SETUP FOR TORQUE / ANGLE / THETA2
# ============================================================

# Load data for torque & angle splines
get_angle_data()
get_torque_data()

cs_tor = CubicSpline(t_x, t_y)         # torque vs time
cs_ang = CubicSpline(a_x, a_y)         # angle vs time
dcs_ang = cs_ang.derivative()          # d(angle)/dt (deg/s if angle is in degrees)


def tor(t):
    return cs_tor(t)

def ang(t):
    return cs_ang(t)

def angv(t):
    """
    Angular velocity from spline derivative, converted to rad/s.
    """
    deg_per_sec = dcs_ang(t)
    return deg_per_sec * (math.pi / 180.0)


# Theta2 spline
get_theta_2_joint_data()
cs_theta_2 = CubicSpline(theta2_t, theta2_y)

def f_theta_2(t):
    return cs_theta_2(t)

# ============================================================
#  SPLINE SETUP FOR THIRD DATASET
# ============================================================
get_csv_angle3_data()
get_csv_torque3_data()

get_csv_angle3n_data()
get_csv_torque3n_data()

cs_ang3 = CubicSpline(a3_x,a3_y)
cs_tor3 = CubicSpline(t3_x,t3_y)

cs_ang3n = CubicSpline(a3_xn,a3_yn)
cs_tor3n = CubicSpline(t3_xn,t3_yn)

dcs_ang3 = cs_ang3.derivative()
dcs_ang3n = cs_ang3n.derivative()


def omega3_phase(p):
    """
    Angular velocity (rad/s) as a function of *phase* p in [0,1].
    Converts derivative wrt phase into derivative wrt time.
    """
    deg_per_phase = dcs_ang3(p)              # dθ/dphase (deg per 1.0)
    deg_per_sec   = deg_per_phase  / total_time
    return deg_per_sec * (math.pi / 180.0)   # convert to rad/s


def omega3_time(t):
    """
    Angular velocity (rad/s) as a function of real time t.
    """
    p = t / total_time
    return omega3_phase(p)
def omega3n_phase(p):
    """
    Angular velocity (rad/s) as a function of *phase* p in [0,1].
    Converts derivative wrt phase into derivative wrt time.
    """
    deg_per_phase = dcs_ang3n(p)              # dθ/dphase (deg per 1.0)
    deg_per_sec   = deg_per_phase  / total_timen
    return deg_per_sec * (math.pi / 180.0)   # convert to rad/s


def omega3n_time(t):
    """
    Angular velocity (rad/s) as a function of real time t.
    """
    p = t / total_timen
    return omega3n_phase(p)


def torque3_phase(p):
    """
    Real torque (N·m) from normalized torque curve digitized from the paper.
    """
    tau_norm = cs_tor3(p)  # normalized torque (N·m/(kg·m))
    return tau_norm * subject_height * subject_mass


def torque3_time(t):
    """
    Real torque (N·m) as a function of time.
    """
    p = t / total_time
    return torque3_phase(p)
def torque3n_phase(p):
    """
    Real torque (N·m) from normalized torque curve digitized from the paper.
    """
    tau_norm = cs_tor3n(p)  # normalized torque (N·m/(kg·m))
    return tau_norm * subject_height * subject_mass


def torque3n_time(t):
    """
    Real torque (N·m) as a function of time.
    """
    p = t / total_timen
    return torque3n_phase(p)


def power3(t):
    return torque3_time(t)*omega3_time(t)
def power3n(t):
    return torque3n_time(t)*omega3n_time(t)


# ============================================================
#  PLOTTING: TORQUE, POWER, ANGLES
# ============================================================

def torque_plot():
    """
    Plot torque vs time (from better_torque.csv spline data).
    """
    plt.figure(6)
    plt.plot(t_x, t_y)
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('Torque (Nm)')
    plt.title('Torque')
    plt.savefig("torque_test.png", dpi=300, bbox_inches="tight")


def t_and_a_plot():
    """
    Plot mechanical power = torque * angular velocity over STS interval.
    """
    time_vals = np.linspace(0.0, 2.0, 300)
    pow_vals  = [angv(t) * tor(t) for t in time_vals]

    plt.figure(9)
    plt.plot(time_vals, pow_vals)
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('Power (W)')
    plt.title('Power In Sitting to Standing')
    plt.savefig("stsplot.png", dpi=300, bbox_inches="tight")


def angle_plots():
    """
    Plot theta2 vs time over a [0, 3] s interval using cs_theta_2.
    """
    plt.figure(9)
    plt.plot(a3_x, a3_y)
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.title('Theta2')
    plt.savefig("angle3.png", dpi=300, bbox_inches="tight")

def powerelec3_plots():
    """
    Plot angular velocity * torque, with both as functions of time to get the equivalent electrical Power.
    """
    time_vals   = np.linspace(0.0, total_time, 200)
    power_vals = [power3(t) for t in time_vals]
    plt.figure(10)
    plt.plot(time_vals, power_vals)
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.title('Power_Electrical from Sit to Stand (80kg 1.84m)')
    plt.xlabel('Time (s)')
    plt.ylabel('Power (W)')
    plt.savefig("power.png", dpi=300, bbox_inches="tight")

    time2_vals   = np.linspace(0.0, total_timen, 200)
    power2_vals = [abs(power3n(t)) for t in time2_vals]
    plt.figure(11)
    plt.plot(time2_vals, power2_vals)
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.title('Power_Electrical from Stand to Sit (80kg 1.84m)')
    plt.xlabel('Time (s)')
    plt.ylabel('Power (W)')
    plt.savefig("power2.png", dpi=300, bbox_inches="tight")
# ============================================================
#  ANALYTIC SIT-TO-STAND MODEL (TANH-BASED ANGLE)
# ============================================================

def angular_velocity_sts(x):
    """
    Analytic angular velocity for STS based on tanh fit, scaled to 2 seconds.
    Returns rad/s.
    """
    # time scaling for 2-second STS
    t_old = (3.0 / 2.0) * x

    # sech^2() term
    u = (t_old - 1.85) / 0.37

    # derivative of 39.77 * tanh(u) -> (39.77 / 0.37) * sech^2(u)
    omega_deg = (39.77 / 0.37) * (1 / np.cosh(u))**2  # deg/s

    # convert to rad/s and apply chain rule (dt_old/dt = 3/2)
    omega_rad = omega_deg * (math.pi / 180.0)
    return (3.0 / 2.0) * omega_rad


def angle_sts_fast(t):
    """
    Analytic tanh-based STS angle vs time (deg).
    """
    t_old = time_scale * t
    return 141.33 + 39.77 * np.tanh((t_old - 1.85) / 0.37)


# ============================================================
#  STS TORQUE FIT (POLYFIT) & POWER
# ============================================================

# Load STS torque data and fit a quadratic torque(x)
get_csv_torque_data()
a, b, c = np.polyfit(sts_torque_x, sts_torque_y, 2)

def torque_function(x):
    """
    Quadratic fit for STS torque vs time (or vs x).
    """
    if max_torque is None:
        raise ValueError("max_torque threshold is not set!")
    return a * (x**2) + (b * x) + c  # optional clipping at max_torque if desired


def power_sts(x):
    """
    Mechanical power during STS from analytic ω and quadratic τ(x).
    """
    t_val = torque_function(x)
    av    = angular_velocity_sts(x)
    return t_val * av


def sts_cycle():
    """
    Populate x_power_elec, y_power_elec with STS power over [0, 2] s.
    """
    x_power_elec.clear()
    y_power_elec.clear()
    values = np.linspace(0.0, 2.0, 100)
    for i in values:
        y_power_elec.append(power_sts(i))
        x_power_elec.append(i)


def sit_to_stand_plots():
    """
    Plot electrical/mechanical power over STS cycle.
    """
    sts_cycle()
    plt.figure(6)
    plt.plot(x_power_elec, y_power_elec)
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('Power Electrical (W)')
    plt.title('P_Electrical In Sitting To Standing')
    plt.savefig("my_plot.png", dpi=300, bbox_inches="tight")


def test_plot():
    """
    Debug plot for angular_velocity_sts over [0, 3]s.
    """
    get_csv_torque_data()
    t_vals   = np.linspace(0.0, 3.0, 20)
    tau_vals = [angular_velocity_sts(t) for t in t_vals]

    plt.figure(7)
    plt.plot(t_vals, tau_vals, marker='o')
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Time')
    plt.ylabel('Torque Nm')  # NOTE: actually plotting angular velocity here
    plt.title('Torque Plot')
    plt.savefig("torque.png", dpi=300, bbox_inches="tight")


# ============================================================
#  GAIT-BASED POWER (MOTOR SHAFT & JOINT)
# ============================================================

def get_power_mech(torque, ang):
    return torque * ang


def p_motorshaft_cycle():
    """
    Compute power at motor shaft over the gait cycle.
    """
    x_gait.clear()
    y_power_ms.clear()
    for i in range(len(ang_velocity)):
        x_gait.append(i * 5)  # % gait, assuming 20 samples -> 0..95
        y_power_ms.append(get_power_mech(nom_torq_ms, ang_velocity[i]))


def p_joint_cycle():
    """
    Compute power at joint over the gait cycle.
    """
    x_gait.clear()
    y_power_j.clear()
    for i in range(len(ang_velocity)):
        x_gait.append(i * 5)
        y_power_j.append(get_power_mech(nom_torq_j, ang_velocity[i]))


def mechanical_plots():
    """
    Plot P_motorshaft and P_joint over gait cycle.
    """
    p_motorshaft_cycle()
    p_joint_cycle()

    plt.figure(1)
    plt.plot(x_gait, y_power_ms)
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Gait Cycle %')
    plt.ylabel('Power Motorshaft (W)')
    plt.title('P_motorshaft vs Time')

    plt.figure(2)
    plt.plot(x_gait, y_power_j)
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Gait Cycle %')
    plt.ylabel('Power Joint (W)')
    plt.title('P_joint vs Time')

    plt.show()


# ============================================================
#  ELECTRICAL MODEL: CURRENT, AVG POWER, BATTERY LIFE
# ============================================================

def get_weighted_list(data):
    return [x * assumed_weight for x in data]


def get_motor_power(data):
    """
    Convert joint power data to motor power considering efficiency and weight.
    """
    return [x * ball_eff for x in get_weighted_list(data)]


def current_plot():
    """
    Plot electrical current vs time from joint power data.
    """
    current_data = [
        (-motor_voltage + math.sqrt(motor_voltage**2 + 4 * R_phase * p_motor)) / (2 * R_phase)
        for p_motor in get_motor_power(joint_power_data)
    ]
    plt.figure(3)
    plt.plot(time_data, current_data)
    plt.axhline(y=0, color="grey", linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.title('Current vs Time')
    plt.show()


def angle_plot():
    """
    Plot joint angle vs time from SitToStandAngles.csv.
    """
    plt.figure(4)
    plt.plot(temp_time, joint_angles)
    plt.axhline(y=0, color="grey", linestyle='-', linewidth=1)
    plt.axvline(x=0, color='grey', linestyle='-', linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('Angle')
    plt.title('Angle vs Time')
    plt.show()


def average_current():
    """
    Compute and print average current based on joint power data.
    """
    current_data = [
        (-motor_voltage + math.sqrt(motor_voltage**2 + 4 * R_phase * p_motor)) / (2 * R_phase)
        for p_motor in get_motor_power(joint_power_data)
    ]
    avg_current = np.mean(current_data)
    print("Average Current (A): ", avg_current)
    return avg_current


def average_power_gait():
    """
    Compute and print average motor power over the gait cycle.
    """
    motor_power = get_motor_power(joint_power_data)
    avg_power_gait = np.mean(motor_power)
    print("Average Power (W): ", avg_power_gait)
    return avg_power_gait


def braking_torque():
    """
    Estimate braking torque from minimum power in first half of gait cycle.
    """
    gait_cycle_time = time_data[-1] - time_data[0]
    # 6 degree change in 0.1 sec from heel strike to foot flat
    delta_theta = 6 * (math.pi / 180)  # radians
    delta_t     = 0.1                  # sec
    ang_velocity_braking = delta_theta / delta_t  # rad/sec

    motor_power = get_motor_power(joint_power_data)
    min_power   = min(motor_power[0:int(len(motor_power) / 2)])
    braking_t   = min_power / ang_velocity_braking
    print("Braking Torque (Nm): ", braking_t)
    return braking_t


def cum_avg_plot():
    """
    Plot weighted power input over time (walking weighted at 70%).
    """
    P_in = get_motor_power(joint_power_data)
    P_in = [x * 0.7 for x in P_in]  # walking weighted at 70%

    plt.figure(5)
    plt.plot(temp_time, P_in)
    plt.axhline(y=0, color="grey", linestyle='-', linewidth=1)
    plt.axvline(x=0, color='gray', linestyle='-', linewidth=1)
    plt.xlabel('Time (s)')
    plt.ylabel('P_in (W)')
    plt.title('Power Input vs Time')
    plt.show()
    return P_in


def battery_life_estimate():
    """
    Estimate battery life assuming no regenerative braking.
    """
    current_data = [
        (-motor_voltage + math.sqrt(motor_voltage**2 + 4 * R_phase * p_motor)) / (2 * R_phase)
        for p_motor in get_motor_power(joint_power_data)
    ]

    # set negative currents to zero
    positive_current_data = current_data.copy()
    for i in range(len(positive_current_data)):
        if positive_current_data[i] < 0:
            positive_current_data[i] = 0

    avg_current = np.mean(positive_current_data)
    print("Average Positive Current (A): ", avg_current)
    battery_life_hours = battery_capacity / avg_current
    print("Estimated Battery Life (hours): ", battery_life_hours)


# ============================================================
#  MAIN SCRIPT EXECUTION
# ============================================================

# Load joint power data from gait CSV
get_csv_data()

# Optional: load joint angles for SitToStandAngles.csv
# get_csv_joint_data()

# Core calculations
average_current()
average_power_gait()
braking_torque()
battery_life_estimate()

# Optional plotting calls
# mechanical_plots()
# current_plot()
# angle_plot()
# cum_avg_plot()
# sit_to_stand_plots()
# test_plot()
# torque_plot()
# t_and_a_plot()
angle_plots()
powerelec3_plots()
