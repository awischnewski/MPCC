#include "MPCCWrapperClass.h"

MPCCWrapperClass::MPCCWrapperClass(std::string paramFile)
{
    // load parameter files from json
    std::ifstream iConfig("Params/config.json");
    json jsonConfig;
    iConfig >> jsonConfig;

    PathToJson json_paths {jsonConfig["model_path"],
                               jsonConfig["cost_path"],
                               jsonConfig["bounds_path"],
                               jsonConfig["track_path"],
                               jsonConfig["normalization_path"]};

    // parse track data
    Track track = Track(json_paths.track_path);
    TrackPos track_xy = track.getTrack();

    // initialize mpc
    mpc = new MPC(jsonConfig["n_sqp"], jsonConfig["n_reset"], jsonConfig["sqp_mixing"], jsonConfig["Ts"], json_paths);
    mpc->setTrack(track_xy.X, track_xy.Y);
}

MPCCWrapperClass::~MPCCWrapperClass()
{
    // nothing to cleanup here
}

void MPCCWrapperClass::calcMPC(double* state_meas, double* input_calc)
{
    // map states to required struct
    State x0 = {
      state_meas[0], // X
      state_meas[1], // Y
      state_meas[2], // phi
      state_meas[3], // vx
      state_meas[4], // vy
      state_meas[5], // rf
      state_meas[6], // s
      state_meas[7], // D
      state_meas[8], // delta
      state_meas[9]  // vs
    };

    // solve MPC problem
    MPCReturn mpc_sol = mpc->runMPC(x0);

    // map outputs to return pointer
    input_calc[0] = mpc_sol.u0.dD;
    input_calc[1] = mpc_sol.u0.dDelta;
    input_calc[2] = mpc_sol.u0.dVs;
}
