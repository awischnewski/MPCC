from PassengerVehicle import PassengerVehicle
from MPCC import MPCCWrapper

import numpy as np

# initiale controller
mpc = MPCCWrapper("Params/config.json")

# initialize vehicle
veh = PassengerVehicle()
# set initial pose
veh.set_VehicleStartPoint(np.array([-33.46, 43.55, -2.35, 1], dtype='double'))
# current vehicle inputs
DriveForce_N = 0
SteeringAngle_rad = 0

for i in range(1000):
    print('Do iteration number ' + str(i))
    # get current state
    veh_state = np.array([veh.get_x_m(),
                         veh.get_y_m(),
                         veh.get_psi_rad() + np.pi/2,
                         veh.get_vx_mps(),
                         veh.get_vy_mps(),
                         veh.get_dPsi_radps(),
                         0, # s is recalculated anyway
                         DriveForce_N,
                         SteeringAngle_rad,
                         veh.get_vx_mps()])

    # calculate MPC
    inputs = mpc.calcMPC(veh_state)
    DriveForce_N = DriveForce_N + inputs[0]
    SteeringAngle_rad = SteeringAngle_rad + inputs[1]

    # apply inputs
    veh.set_DriveForce(DriveForce_N)
    veh.set_SteeringAngle(SteeringAngle_rad)

    # simulate 20ms
    for j in range(10):
        veh.step()
