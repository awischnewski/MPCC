from PassengerVehicle import PassengerVehicle
from MPCC import MPCCWrapper

import numpy as np
import pickle

# initiale controller
mpc = MPCCWrapper("Params/config.json")

# initialize vehicle
veh = PassengerVehicle()
# set initial pose
veh.set_VehicleStartPoint(np.array([-53.2, 62.32, -2.35, 1], dtype='double'))

# get it rollin
for i in range(500):
    veh.set_DriveForce(5000)
    veh.set_SteeringAngle(0)
    veh.step()

# current vehicle inputs
DriveForce_kN = 3
SteeringAngle_rad = 0

# store guess for arc length coordinate
s_guess = 0
sv_guess = veh.get_vx_mps()

# preallocate log variables
N_steps = 2000
log_x_m = np.zeros(N_steps)
log_y_m = np.zeros(N_steps)
log_psi_rad = np.zeros(N_steps)
log_vx_mps = np.zeros(N_steps)
log_vy_mps = np.zeros(N_steps)
log_dPsi_radps = np.zeros(N_steps)
log_s_m = np.zeros(N_steps)
log_fx_kN = np.zeros(N_steps)
log_delta_rad = np.zeros(N_steps)
log_vs_mps = np.zeros(N_steps)
log_alphaF_rad = np.zeros(N_steps)
log_alphaR_rad = np.zeros(N_steps)
log_predictions = []
log_solver_status = np.zeros(N_steps)

for i in range(N_steps):
    print('Do iteration number ' + str(i))
    # get current state
    veh_state = np.array([veh.get_x_m(),
                         veh.get_y_m(),
                         veh.get_psi_rad() + np.pi/2,
                         veh.get_vx_mps(),
                         veh.get_vy_mps(),
                         veh.get_dPsi_radps(),
                         s_guess,
                         DriveForce_kN,
                         SteeringAngle_rad,
                         sv_guess])

    print('x_m: {:6.2f} | y_m: {:6.2f} | v_mps: {:6.2f}'.format(veh.get_x_m(),
                veh.get_y_m(), veh.get_vx_mps()))

    # calculate MPC
    inputs = mpc.calcMPC(veh_state)
    print('Solution to the MPC problem: ' + str(inputs))
    print('')
    print('')
    DriveForce_kN = DriveForce_kN + 0.05*inputs[0]
    SteeringAngle_rad = SteeringAngle_rad + 0.05*inputs[1]

    # apply inputs
    veh.set_DriveForce(DriveForce_kN*1000)
    veh.set_SteeringAngle(SteeringAngle_rad)

    # log data
    log_x_m[i] = veh.get_x_m()
    log_y_m[i] = veh.get_y_m()
    log_psi_rad[i] = veh.get_psi_rad() + np.pi/2
    log_vx_mps[i] = veh.get_vx_mps()
    log_vy_mps[i] = veh.get_vy_mps()
    log_dPsi_radps[i] = veh.get_dPsi_radps()
    log_fx_kN[i] = DriveForce_kN
    log_delta_rad[i] = SteeringAngle_rad
    # recalculate sideslips
    log_alphaF_rad[i] = SteeringAngle_rad - np.arctan2(veh.get_vy_mps() + veh.get_dPsi_radps()*1.6, veh.get_vx_mps())
    log_alphaR_rad[i] = -np.arctan2(veh.get_vy_mps() - veh.get_dPsi_radps()*1.8, veh.get_vx_mps())
    mpc_predictions = mpc.getPrediction()
    # recalculate sideslips
    alphaF_pred = mpc_predictions[:][8] - np.arctan2(mpc_predictions[:][4] + mpc_predictions[:][5]*1.6, mpc_predictions[:][3])
    alphaR_pred = - np.arctan2(mpc_predictions[:][4] - mpc_predictions[:][5]*1.8, mpc_predictions[:][3])
    mpc_predictions = list(mpc_predictions)
    mpc_predictions.append(alphaF_pred)
    mpc_predictions.append(alphaR_pred)
    log_predictions.append(mpc_predictions)
    log_s_m[i] = mpc_predictions[6][0]
    log_vs_mps[i] = mpc_predictions[9][0]

    # update s and sv based on predicted values
    s_guess = mpc_predictions[6][1]
    sv_guess = mpc_predictions[9][1]

    print('s_m predicted: {:6.2f} | sv_mps predicted: {:6.2f}'.format(s_guess, sv_guess))

    # simulate 20ms
    for j in range(25):
        veh.step()

# save results
with open('MPCClogs.p', 'wb') as f:
    pickle.dump([log_x_m, log_y_m, log_psi_rad, log_vx_mps, log_vy_mps,
                    log_dPsi_radps, log_s_m, log_fx_kN, log_delta_rad,
                    log_vs_mps, log_alphaF_rad, log_alphaR_rad,
                    log_predictions], f)
