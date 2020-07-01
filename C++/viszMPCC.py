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
fig2, ax2 = plt.subplots(3, 1)

ax1.plot(logs[0], logs[1])
ax1.plot(track['X_i'], track['Y_i'], 'k')
ax1.plot(track['X_o'], track['Y_o'], 'k')
ax1.set_xlabel('East in m')
ax1.set_ylabel('North in m')
ax1.grid()

ax2[0].plot(logs[2])
ax2[0].set_ylabel('Velocity in mps')
ax2[0].grid()

ax2[1].plot(logs[4])
ax2[1].set_ylabel('Steering angle in rad')
ax2[1].grid()

ax2[2].plot(logs[3])
ax2[2].set_ylabel('Drive force in kN')
ax2[2].grid()

plt.show()
