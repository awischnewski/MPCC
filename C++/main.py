from PassengerVehicle import PassengerVehicle
from MPCC import MPCCWrapper

import numpy as np
import pickle

# initiale controller
mpc = MPCCWrapper("Params/config.json")

# initialize vehicle
veh = PassengerVehicle()
# set initial pose
veh.set_VehicleStartPoint(np.array([-33.46, 43.55, -2.35, 1], dtype='double'))

# get it rollin
for i in range(200):
    veh.set_DriveForce(2000)
    veh.set_SteeringAngle(0)
    veh.step()

# current vehicle inputs
DriveForce_kN = 0
SteeringAngle_rad = 0

# preallocate log variables
N_steps = 1000
log_x_m = np.zeros(N_steps)
log_y_m = np.zeros(N_steps)
log_v_mps = np.zeros(N_steps)
log_fx_kN = np.zeros(N_steps)
log_delta_rad = np.zeros(N_steps)
log_predictions = []

for i in range(N_steps):
    print('Do iteration number ' + str(i))
    # get current state
    veh_state = np.array([veh.get_x_m(),
                         veh.get_y_m(),
                         veh.get_psi_rad() + np.pi/2,
                         veh.get_vx_mps(),
                         veh.get_vy_mps(),
                         veh.get_dPsi_radps(),
                         0, # s is recalculated anyway
                         DriveForce_kN,
                         SteeringAngle_rad,
                         veh.get_vx_mps()])

    print('x_m: {:6.2f} | y_m: {:6.2f} | v_mps: {:6.2f}'.format(veh.get_x_m(), veh.get_y_m(), veh.get_vx_mps()))

    # calculate MPC
    inputs = mpc.calcMPC(veh_state)
    print('Solution to the MPC problem: ' + str(inputs))
    print('')
    print('')
    DriveForce_kN = DriveForce_kN + 0.02*inputs[0]
    SteeringAngle_rad = SteeringAngle_rad + 0.02*inputs[1]

    # apply inputs
    veh.set_DriveForce(DriveForce_kN*1000)
    veh.set_SteeringAngle(SteeringAngle_rad)

    # log data
    log_x_m[i] = veh.get_x_m()
    log_y_m[i] = veh.get_y_m()
    log_v_mps[i] = veh.get_vx_mps()
    log_fx_kN[i] = DriveForce_kN
    log_delta_rad[i] = SteeringAngle_rad
    log_predictions.append(mpc.getPrediction())

    # simulate 20ms
    for j in range(10):
        veh.step()

# save results
with open('MPCClogs.p', 'wb') as f:
    pickle.dump([log_x_m, log_y_m, log_v_mps, log_fx_kN, log_delta_rad, log_predictions], f)
