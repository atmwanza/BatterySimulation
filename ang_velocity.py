import matplotlib.pyplot as plt

time = [0] * 20
i = 0
for x in range(0,20):
    time[x] = i
    i += 5

# print(time)
# print(len(time))
ang_velocity = [-10, -7.5, 2.5, 8, -5, -14, -16, -16, -14, -9, -1.25, 3.25, 7, 13, 14, 17, 17.5, 8, -2, -6.25 ]
# print(ang_velocity)
# print(len(ang_velocity))

plt.plot(time, ang_velocity)
plt.xlabel('time')
plt.ylabel('angular velocity')
plt.title('X vs Y')
plt.show()