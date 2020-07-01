import matplotlib.pyplot as plt
import numpy as np
import pickle
import json

# load track from json
with open('Params/track_scaled.json') as f:
    track = json.load(f)

# load logs
with open('MPCClogs.p', 'rb') as f:
    logs = pickle.load(f)

# visualize results
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots(4, 2)

# choose point where predictions are plotted
idx = 1900

ax1.plot(logs[0], logs[1])
ax1.plot(track['X_i'], track['Y_i'], 'k')
ax1.plot(track['X_o'], track['Y_o'], 'k')
ax1.plot(track['X'], track['Y'], 'k--')
ax1.axis('equal')
ax1.set_xlabel('East in m')
ax1.set_ylabel('North in m')
ax1.grid()


ax2[0][0].plot(logs[3])
ax2[0][0].set_ylabel('Velocity x in mps')
ax2[0][0].grid()

ax2[1][0].plot(logs[4])
ax2[1][0].set_ylabel('Velocity y in mps')
ax2[1][0].grid()

ax2[2][0].plot(logs[5])
ax2[2][0].set_ylabel('Yaw rate in radps')
ax2[2][0].grid()

ax2[3][0].plot(logs[2])
ax2[3][0].set_ylabel('Psi in rad')
ax2[3][0].grid()

ax2[0][1].plot(logs[6])
ax2[0][1].set_ylabel('Drive force in kN')
ax2[0][1].grid()

ax2[1][1].plot(logs[7])
ax2[1][1].set_ylabel('Steering angle in rad')
ax2[1][1].grid()


# plot predictions
ax1.plot(logs[8][idx][0], logs[8][idx][1], 'r--')
ax2[0][0].plot(range(idx, idx+150), logs[8][idx][3])
ax2[1][0].plot(range(idx, idx+150), logs[8][idx][4])
ax2[2][0].plot(range(idx, idx+150), logs[8][idx][5])
ax2[3][0].plot(range(idx, idx+150), logs[8][idx][2])
ax2[0][1].plot(range(idx, idx+150), logs[8][idx][7])
ax2[1][1].plot(range(idx, idx+150), logs[8][idx][8])
ax2[2][1].plot(range(idx, idx+150), logs[8][idx][6])
ax2[2][1].grid()
ax2[3][1].plot(range(idx, idx+150), logs[8][idx][9])
ax2[3][1].grid()

plt.show()
